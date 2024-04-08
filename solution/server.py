from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class Orden:
    def __init__(self, client, status, payment):
        self.client = client
        self.status = status
        self.payment = payment

class OrdenFisico(Orden):
    def __init__(self, client, status, payment, shipping, products):
        super().__init__(client, status, payment)
        self.shipping = shipping
        self.products = products

class OrdenDigital(Orden):
    def __init__(self, client, status, payment, code, expiration):
        super().__init__(client, status, payment)
        self.code = code
        self.expiration = expiration

class OrdenFactory:
    @staticmethod
    def create_orden(client, status, payment, date_one, date_two, orden_type, products=None, code=None, expiration=None):
        if orden_type == "Fisica":
            return OrdenFisico(client, status, payment, date_one, products)
        if orden_type == "Digital":
            return OrdenDigital(client, status, payment, code, expiration)

    @staticmethod
    def agregar_orden(orden):
        global identificador
        key = f"{identificador}"
        identificador += 1
        ordenes[key] = orden.__dict__

    def listar_ordenes_pendientes(ordenes):
        return {key: value for key, value in ordenes.items() if value["status"] == "Pendiente"}

identificador = 3
ordenes = {
    "1": {
        "client": "Juan Perez",
        "status": "Pendiente",
        "payment": "Tarjeta de Credito",
        "shipping": 10.0,
        "products": ["Botella", "Sueter", "Mochila"],
        "order_type": "Fisica"
    },
    "2": {
        "client": "Maria Rodriguez",
        "status": "Pendiente",
        "payment": "PayPal",
        "code": "ABC123",
        "expiration": "2022-12-31",
        "order_type": "Digital"
    }
}

class RESTRequestHandler(BaseHTTPRequestHandler):
    def handle_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))

    def read_data(self):
        content_length = int(self.headers["Content-Length"])
        data = self.rfile.read(content_length)
        data = json.loads(data.decode("utf-8"))
        return data

    def handle_error_response(self):
        self.handle_response(
            404, {"Error": "Ruta no existente"}
        )

    def do_GET(self):
        if self.path == "/ordenes":
            self.handle_response(200, ordenes)
        elif self.path == "/pending":
            pending_orders = OrdenFactory.listar_ordenes_pendientes(ordenes)
            self.handle_response(200, pending_orders)
        else:
            order_id = self.path.split("/")[-1]
            if order_id in ordenes:
                self.handle_response(200, ordenes[order_id])
            else:
                self.handle_response(404, {"Error": f"La orden {order_id} no existe"})

    def do_POST(self):
        if self.path == "/fisica":
            data = self.read_data()
            orden = OrdenFactory.create_orden(data["client"], data["status"], data["payment"], data["shipping"], None, "Fisica", products=["Licuadora", "Refrigeradora", "Lavadora"])
            OrdenFactory.agregar_orden(orden)
            self.handle_response(201, orden.__dict__)
        elif self.path == "/digital":
            data = self.read_data()
            orden = OrdenFactory.create_orden(data["client"], data["status"], data["payment"], None, None, "Digital", code="ABC123", expiration="2022-12-31")
            OrdenFactory.agregar_orden(orden)
            self.handle_response(201, orden.__dict__)
        else:
            self.handle_error_response()

    def do_PUT(self):
        if self.path.startswith("/update/"):
            order_id = self.path.split("/")[-1]
            if order_id in ordenes:
                data = self.read_data()
                ordenes[order_id]["status"] = data["status"]
                self.handle_response(200, ordenes[order_id])
            else:
                self.handle_response(404, {"Error": f"La orden {order_id} no existe"})
        else:
            self.handle_error_response()

    def do_DELETE(self):
        if self.path.startswith("/delete/"):
            order_id = self.path.split("/")[-1]
            if order_id in ordenes:
                order = ordenes[order_id]
                del ordenes[order_id]
                self.handle_response(200, order)
            else:
                self.handle_response(404, {"Error": f"La orden {order_id} no existe"})
        else:
            self.handle_error_response()

def run_server(port=8000):
    try:
        server_address = ("", port)
        httpd = HTTPServer(server_address, RESTRequestHandler)
        print(f"Iniciando servidor web en http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor web")
        httpd.socket.close()

if __name__ == "__main__":
    run_server()