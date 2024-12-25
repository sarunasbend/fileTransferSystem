import socket
import ssl

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
                        # data = "upload " + filename + " "
                        data = b""
                        for data_chunk in data:
                            data += data_chunk
                        self.secure_client_socket.sendall(data)
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



if __name__ == "__main__":
    startup()
    prompt()
    client = None
    connected = False
    while True:
        userInput = input()
        if userInput == "connect" and connected == False:
            client = Client()
            connected = True
        elif userInput == "disconnect" and connected == True:
            client.closeClient()
        elif userInput.split(" ")[0] == "upload":
            client.uploadFile(userInput.split(" ")[1])
        elif userInput.split(" ")[0] == "delete":
            print("deleting")
        elif userInput == "see":
            print("seeing")
        elif userInput == "exit":
            break
        elif userInput == "help":
            prompt()
        else:
            print("invalid command")