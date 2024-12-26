import socket
import threading
import ssl
import os

HOST = '0.0.0.0'
PORT = 12345
MAX_RECEIVE = 1024
UPLOAD = 6

class Server:
    def __init__(self):
        self.excludedFiles = ['Client.py', '.idea', 'Server.py', '.git', '.gitignore', 'server.crt', 'README.md', 'server.key']

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
                threading.Thread(target=self.handleRequest, args=(client_connection, client_address,)).start()
            print("finished")
        except KeyboardInterrupt as e:
            print("Shutting down Server")
        finally:
            self.secure_server_socket.close()
            self.server_socket.close()

    def handleRequest2(self, client_connection, client_address):
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

    def handleRequest(self, client_connection, client_address):
        try:
            request = client_connection.recv(MAX_RECEIVE).decode()
            if request.split(" ")[0] == "upload":
                filename = request.split(" ")[1] + "2"
                filedata = request[UPLOAD + len(filename) + 1:]
                self.upload(filename, filedata)
            elif request.split(" ")[0] == "delete":
                pass
            elif request.split(" ")[0] == "download":
                pass
            elif request == "see":
                self.see(client_connection)
        except Exception as e:
            print(f"{e}")

    def upload(self, filename, data=None):
        try:
            with open(filename, 'wb') as file:
                data = data.encode()
                file.write(data)
        except FileExistsError as e:
            print(f"{e}")
        except KeyboardInterrupt as e:
            print(f"{e}")
        except Exception as e:
            print(f"{e}")

    def delete(self, filename):
        pass

    def download(self, filename):
        pass

    def see(self, client_connection):
        try:
            filesStored = os.listdir()
            for file in self.excludedFiles:
                filesStored.remove(file)

            data = ""
            for file in filesStored:
                data += file + " "
            print(data)
            try:
                client_connection.sendall(data.encode())
            except Exception as e:
                pass
        except OSError as e:
            print(f"{e}")


if __name__ == "__main__":
    Server()
