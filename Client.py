import socket
from cryptography.fernet import Fernet
MAX_RECEIVE = 1024

class Client:
    def __init__(self, key=None):
        try:
            self.cipher_suite = Fernet(key)
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect(('localhost', 12345))

            file_request = "basic.txt"
            self.client_socket.send(self.cipher_suite.encrypt(file_request.encode("utf-8")))

            try:
                with open('download.txt', 'wb') as file:
                    while True:
                        data = self.client_socket.recv(MAX_RECEIVE)
                        if not data:
                            break
                        file.write(self.cipher_suite.decrypt(data.decode("utf-8")))
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
            self.client_socket.close()

if __name__ == "__main__":
    key = input("Enter the encryption key:").encode()
    Client(key=key)