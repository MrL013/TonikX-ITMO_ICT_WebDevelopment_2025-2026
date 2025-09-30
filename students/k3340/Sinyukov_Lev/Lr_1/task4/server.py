import socket
import threading

def broadcast(msg, socket_sender):
    for client in clients:
        if client != socket_sender:
            try:
                client.send(msg)
            except:
                clients.remove(client)

def handle_client(client_socket, client_address):
    print(f'Подключение от {client_address}')

    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            print(f'Запрос клиента {client_address}:\n{message.decode("utf-8")}')
            broadcast(message, client_socket)
        except:
            break

    print(f'Прервано соединение с {client_address}')
    clients.remove(client_address)
    client_socket.close()

def func_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Сервер запущен на {HOST}:{PORT}...")

    while True:
        client_socket, client_address = server.accept()
        clients.append(client_socket)
        thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        thread.start()


HOST = 'localhost'
PORT = 8080

clients = []

func_server()