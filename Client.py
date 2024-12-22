import socket
import ssl

MAX_RECEIVE = 1024

class Client:
    def __init__(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            self.context.load_verify_locations('server.crt')

            self.secure_client_socket = self.context.wrap_socket(self.client_socket, server_hostname='localhost')
            self.secure_client_socket.connect(('localhost', 12345))

            file_request = "basic.txt"
            self.secure_client_socket.sendall(file_request.encode())

            try:
                with open('download.txt', 'wb') as file:
                    while True:
                        data = self.secure_client_socket.recv(MAX_RECEIVE)
                        if not data:
                            break
                        file.write(data)
            except FileExistsError as e:
                print(f"{e}")
        except ConnectionRefusedError as e:
            print(f"{e}")
        except KeyboardInterrupt as e:
            print(f"{e}")
        except Exception as e:
            print(f"{e}")
        finally:
            print("File has been received.")
            self.secure_client_socket.close()
            self.client_socket.close()

if __name__ == "__main__":
    Client()