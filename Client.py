import threading
import socket

MAX_RECEIVE = 1024

class Client:
    def __init__(self):
        try:

            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect(('localhost', 12345))

            file_request = "basic.txt"
            self.client_socket.send(file_request.encode())
            try:

                with open('basic_downloaded.txt', 'wb') as file:
                    while True:
                        data = self.client_socket.recv(MAX_RECEIVE)
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
            self.client_socket.close()

if __name__ == "__main__":
    Client()