import threading
import socket

MAX_RECEIVE = 1024

if __name__ == "__main__":
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))

    file_request = "basic.txt"
    client_socket.send(file_request.encode())

    with open ('basic_downloaded.txt', 'wb') as file:
        while True:
            data = client_socket.recv(MAX_RECEIVE)
            if not data:
                break
            file.write(data)
    print("File has been received.")

