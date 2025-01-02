import socket
import threading
import ssl
import os
import time

HOST = '0.0.0.0'
PORT = 12345
MAX_RECEIVE = 1024
UPLOAD = 6

class Server:
    def __init__(self):
        # files that I want to exclude the client seeing
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
        except KeyboardInterrupt as e:
            print("Shutting down Server")
            self.secure_server_socket.close()
            self.server_socket.close()
        finally:
            self.secure_server_socket.close()
            self.server_socket.close()

    # constantly waits to accept more requests from the client
    def handleRequest(self, client_connection, client_address):
        try:
            while True:
                request = client_connection.recv(MAX_RECEIVE).decode()
                if request.split(" ")[0] == "upload":
                    filename = request.split(" ")[1]
                    filedata = request[UPLOAD + len(filename) + 1:]
                    self.upload(filename, filedata)
                elif request.split(" ")[0] == "delete":
                    filename = request.split(" ")[1]
                    self.delete(filename)
                elif request.split(" ")[0] == "download":
                    filename = request.split(" ")[1]
                    self.download(filename, client_connection)
                elif request == "see":
                    self.see(client_connection)
        except Exception as e:
            print(f"{e}")
        finally:
            client_connection.close()

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
        try:
            if filename not in self.excludedFiles:
                if os.path.exists(filename):
                    os.remove(filename)
                else:
                    raise FileNotFoundError
        except FileNotFoundError as e:
            print(f"{e}")

    def download(self, filename, client_connection):
        try:
            while True:
                try:
                    with open(filename, 'rb') as file:
                        client_connection.sendall("okay".encode())
                        data = b""
                        for data_chunk in file:
                            data += data_chunk
                        client_connection.sendall(data)
                        client_connection.sendall("EOF".encode())
                        break
                except FileNotFoundError:
                    print(b"File not Found.")
                    client_connection.sendall("File not Found".encode())
                    break
        except Exception as e:
            print(f"{e}")

    # sends the client all the available files on the server
    def see(self, client_connection):
        try:
            filesStored = os.listdir()
            for file in self.excludedFiles:
                filesStored.remove(file)

            size_of_files = []
            last_modified = []
            creation_date = []

            for file in filesStored:
                size_of_files.append(os.path.getsize(file))
                last_modified.append(os.path.getmtime(file))
                # creation_date.append(time.ctime(os.path.getctime(file)))

            sending_data = ""
            file_padding = 11
            size_padding = 6
            last_padding = 15

            for x in range(0, len(filesStored)):
                sending_data += filesStored[x] + " " + str(size_of_files[x]) + " " + str(last_modified[x])  + "\n"
                if len(filesStored[x]) > file_padding: file_padding = len(filesStored[x])
                if len(str(size_of_files[x])) > file_padding: file_padding = len(str(size_of_files[x]))
                if len(str(last_modified[x])) > file_padding: file_padding = len(str(last_modified[x]))

            sending_data += str(file_padding) + " " + str(size_padding) + " " + str(last_padding)

            try:
                client_connection.sendall(sending_data.encode())
            except Exception as e:
                print(f"{e}")
        except OSError as e:
            print(f"{e}")

if __name__ == "__main__":
    Server()
