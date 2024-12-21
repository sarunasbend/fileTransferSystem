import socket
import threading

MAX_RECEIVE = 1024

if __name__ == "__main__":
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 12345))
    server_socket.listen(5)

    print("Server Listening on port 12345")

    while True:
        client_connection, client_address = server_socket.accept()
        print(f"Connected to {client_address}")
        file_request = client_connection.recv(MAX_RECEIVE)

        try:
            with open(file_request, 'rb') as file:
                for data_chunk in file:
                    client_connection.sendall(data_chunk)
        except FileNotFoundError:
            print(b"File not Found.")

        client_connection.close()

