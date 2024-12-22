import socket
import ssl

MAX_RECEIVE = 1024

class Client:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        self.context.load_verify_locations('server.crt')

        self.secure_client_socket = self.context.wrap_socket(self.client_socket, server_hostname='localhost')
        self.secure_client_socket.connect(('localhost', 12345))

    # will send username and password to server to check if they have access
    # server will send back OKAY message which will then allow it permissions to make requests, with server then allowing it permissions to access the information
    # username and password will be sent over in plaintext as TLS will have it encrypted
    def authenticate(self):
        username = input("Enter Username: ")
        password = input("Enter Password: ")

        try:
            self.secure_client_socket.send((username + " " + password).encode())

            received_message = self.secure_client_socket.recv(MAX_RECEIVE).decode()
            print(received_message)

            if received_message != "OK":
                self.secure_client_socket.close()
                self.client_socket.close()

        except KeyboardInterrupt as e:
            print(f"{e}")
            self.secure_client_socket.close()
            self.client_socket.close()

    def uploadFile(self):
        pass

    def downloadFile(self):
        try:
            file_request = input("Enter Filename: ")
            self.secure_client_socket.sendall(file_request.encode())

            try:
                with open(file_request + "2", 'wb') as file:
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
    user = Client()
    user.authenticate()
    user.downloadFile()