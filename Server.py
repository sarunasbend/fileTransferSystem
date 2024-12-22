import socket
import threading
import ssl

HOST = '0.0.0.0'
PORT = 12345
MAX_RECEIVE = 1024

class Server:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((HOST, PORT))

        self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        self.context.load_cert_chain(certfile='server.crt', keyfile='server.key')

        self.secure_server_socket = self.context.wrap_socket(self.server_socket, server_side=True)

        print("Server Listening on port: 12345")
        self.secure_server_socket.listen(100)

        try:
            while True:
                client_connection, client_address = self.secure_server_socket.accept()
                print(f"Connected to {client_address}")
                threading.Thread(target=self.handleRequest, args=(client_connection,client_address,)).start()
        except KeyboardInterrupt as e:
            print("Shutting down Server")
        finally:
            self.secure_server_socket.close()
            self.server_socket.close()

    def handleRequest(self, client_connection, client_address):
        try:
            file_request = client_connection.recv(MAX_RECEIVE).decode()
            print(f"Message from {client_address}: {file_request}")
            while True:
                try:
                    with open(file_request, 'rb') as file:
                        data = b""
                        for data_chunk in file:
                            data += data_chunk
                        client_connection.sendall(data)
                        break
                except FileNotFoundError:
                    print(b"File not Found.")
                    client_connection.sendall("File not Found".encode())
                    break
        except Exception as e:
            print(f"{e}")
        finally:
            client_connection.close()


if __name__ == "__main__":
    Server()
