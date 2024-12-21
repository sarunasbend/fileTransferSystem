import socket
import threading
from cryptography.fernet import Fernet

HOST = '0.0.0.0'
PORT = 12345
MAX_RECEIVE = 1024

class Server:
    def __init__(self):
        self.key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((HOST, PORT))

        print("Server Listening on port: 12345")
        print(f"Server Encrypted Key: {self.key.decode()}")
        self.server_socket.listen(100)

        try:
            while True:
                client_connection, client_address = self.server_socket.accept()
                print(f"Connected to {client_address}")
                threading.Thread(target=self.handleRequest, args=(client_connection,client_address,)).start()
        except KeyboardInterrupt as e:
            print("Shutting down Server")
        finally:
            self.server_socket.close()

    def handleRequest(self, client_connection, client_address):
        try:
            encrypted_file_request = client_connection.recv(MAX_RECEIVE)
            decrypted_file_request = self.cipher_suite.decrypt(encrypted_file_request).decode("utf-8")
            print(f"Message from {client_address}: {decrypted_file_request}")
            while True:
                try:
                    with open(decrypted_file_request, 'rb') as file:
                        data = b""
                        for data_chunk in file:
                            data += data_chunk
                        client_connection.sendall(self.cipher_suite.encrypt(data))
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
