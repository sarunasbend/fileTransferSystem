import socket
import ssl
import time

MAX_RECEIVE = 1024

def startup():
    print("===========================================================================================")
    print("______ _ _        _____                    __            _____           _")
    print("|  ___(_) |      |_   _|                  / _|          /  ___|         | |")
    print("| |_   _| | ___    | |_ __ __ _ _ __  ___| |_ ___ _ __  \ `--. _   _ ___| |_ ___ _ __ ___")
    print("|  _| | | |/ _ \   | | '__/ _` | '_ \/ __|  _/ _ \ '__|  `--. \ | | / __| __/ _ \ '_ ` _ \"")
    print("| |   | | |  __/   | | | | (_| | | | \__ \ ||  __/ |    /\__/ / |_| \__ \ ||  __/ | | | | |")
    print("\_|   |_|_|\___|   \_/_|  \__,_|_| |_|___/_| \___|_|    \____/ \__, |___/\__\___|_| |_| |_|")
    print("                                                                __/ |                      ")
    print("                                                               |___/                       ")
    print("")
    print("❈ This is a client-server application that runs on localhost, and uses TLS to communicate")
    print("  over TCP/IP.")
    print("❈ Here are the features it allows for:")
    print("     ❶ Upload Files to Server")
    print("     ❷ Download Files from Server")
    print("     ❸ Delete Files from Server")
    print("     ❹ Share Files with other Clients")
    print("❈ Press Enter to Start using the System")
    print("")
    print("===========================================================================================")
    input()

def prompt():
    print("Available Commands:")
    print("     ❶ connect (connects the client to the server)")
    print("     ❷ disconnect (disconnects the client from the server)")
    print("     ❸ upload (uploads a file to the Server, specify the name of the file within current")
    print("       working directory after command)")
    print("     ❹ download (specifying the file on the server)")
    print("     ❺ delete (deletes specified file from server)")
    print("     ❻ see (lists all files within server)")
    print("     ❼ exit (close the client)")
    print("     ❽ help (for this prompt again)")
    print("")

class Client:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        self.context.load_verify_locations('server.crt')

        self.secure_client_socket = self.context.wrap_socket(self.client_socket, server_hostname='localhost')
        self.secure_client_socket.connect(('localhost', 12345))

    def closeClient(self):
        self.secure_client_socket.close()
        self.client_socket.close()

    def uploadFile(self, filename):
        try:
            while True:
                try:
                    with open(filename, 'r') as file:
                        data = "upload " + filename + " "
                        line = file.readline()
                        while line:
                            data += line
                            line = file.readline()
                        self.secure_client_socket.sendall(data.encode())
                        break
                except FileNotFoundError:
                    print("File not Found")
        except Exception as e:
            print(f"{e}")

    def downloadFile(self):
        try:
            file_request = input("Enter Filename: ")
            self.secure_client_socket.sendall(file_request.encode())
            try:
                with open(file_request, 'wb') as file:
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

    def deleteFile(self):
        pass

    def see(self):
        try:
            self.secure_client_socket.sendall("see".encode())
        except Exception as e:
            print(f"{e}")
        try:
            files_received = self.secure_client_socket.recv(MAX_RECEIVE).decode()
            separate_files = files_received.split("\n")[0:-1]
            files_received = files_received.split("\n")

            parsed_files_received = []

            for file in separate_files:
                file = file.split(" ")
                parsed_files_received.append(file[0])
                parsed_files_received.append(file[1])
                parsed_files_received.append(time.ctime(float(file[2])))


            padding = files_received[-1].split(" ")

            print(" File Name " + ((int(padding[0]) - 11) * " ") + " Size " + (int(padding[1]) - 6) * " "  + " Last Accessed " + ((int(padding[2]) - 15)) * " ")
            print("=" * (int(padding[0]) + int(padding[1]) + int(padding[2])))

            for x in range(0, len(parsed_files_received), 3):
                file_padding = int(padding[0]) - len(parsed_files_received[x])
                size_padding = int(padding[1]) - len(parsed_files_received[x + 1])
                last_padding = int(padding[2]) - len(parsed_files_received[x + 2])
                print(" " + parsed_files_received[x] + (file_padding * " ") + " " + parsed_files_received[x + 1] + (size_padding * " ") + parsed_files_received[x + 2] + (last_padding * " "))

        except Exception as e:
            print(f"{e}")

if __name__ == "__main__":
    startup()
    prompt()
    client = None
    connected = False
    while True:
        userInput = input("$ ")
        if userInput == "connect" and connected == False:
            client = Client()
            connected = True
        elif userInput == "disconnect" and connected == True:
            client.closeClient()
            connected = False
        elif userInput.split(" ")[0] == "upload":
            client.uploadFile(userInput.split(" ")[1])
        elif userInput.split(" ")[0] == "delete":
            print("deleting")
        elif userInput == "see":
            client.see()
        elif userInput == "exit":
            break
        elif userInput == "help":
            prompt()
        else:
            print("invalid command")