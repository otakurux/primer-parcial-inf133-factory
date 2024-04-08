import requests
import json

base_url = 'http://localhost:8000'

def print_response(response):
    print(f'Status Code: {response.status_code}')
    print('Response:')
    print(json.dumps(response.json(), indent=4))

def ordenes():
    url = f'{base_url}/ordenes'
    response = requests.get(url)
    print_response(response)

def ordenes_pending():
    url = f'{base_url}/pending'
    response = requests.get(url)
    print_response(response)

def create_fisico_order(data):
    url = f'{base_url}/fisica'
    response = requests.post(url, json=data)
    print_response(response)

def create_digital_order(data):
    url = f'{base_url}/digital'
    response = requests.post(url, json=data)
    print_response(response)

def update_order_status(order_id, new_status):
    url = f'{base_url}/update/{order_id}'
    data = {"status": new_status}
    response = requests.put(url, json=data)
    print_response(response)

def delete_order(order_id):
    url = f'{base_url}/delete/{order_id}'
    response = requests.delete(url)
    print_response(response)

if __name__ == "__main__":
    data = {
        "client": "Carlos Perez",
        "status": "Pendiente",
        "payment": "Tarjeta de Credito",
        "shipping": 15.0,
        "products": ["Camiseta", "Pantalon", "Zapatos"]
    }
    print("\nCreando orden fisico:")
    create_fisico_order(data)

    data = {
        "client": "Luisa Martinez",
        "status": "Pendiente",
        "payment": "PayPal",
        "code": "XYZ789",
        "expiration": "2023-12-31"
    }
    print("\nCreando orden digital:")
    create_digital_order(data)

    print("\nOrdenes:")
    ordenes()

    print("\nOrdenes pendientes:")
    ordenes_pending()
    
    print("\nActualizando orden con id 3: ")
    update_order_status(3, "En proceso")

    print("\nEliminando orden con id 2:")
    delete_order(2)

    data = {
        "client": "Daner Perez",
        "status": "Enviado",
        "payment": "Tarjeta de Credito",
        "shipping": 100.0,
        "products": ["Licuadora", "Refrigerador", "Lavadora"]
    }
    print("\nCreando orden fisico:")
    create_fisico_order(data)

    print("\nOrdenes:")
    ordenes()
    
