import socket
import sys

class SocketServer:

    def __init__(self, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(socket.gethostname())
        address = (socket.gethostname(), int(port))
        print("Binding")
        try:
            self.socket.bind(address)
        except:
            print(sys.exc_info())
        print("Listening")
        self.socket.listen(1)
        print("Socket listening...")
        try:
            (self.connection, self.client_address) = self.socket.accept()
            print("Connection made with %s" % str(self.client_address))
        except:
            print(sys.exc_info())

    def receive(self):
        buffer = ""
        while True:
            p = self.connection.recv(1).decode('utf-8')
            if p != "\n":
                buffer += p
            else:
                break
        return buffer

    def send(self, msg):
        self.connection.sendall((str(msg)+"\n").encode('utf-8'))

    def close(self):
        self.connection.close()

class SocketClient:

    def __init__(self, add, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        address = (add, int(port))
        self.socket.connect(address)

    def send(self, msg):
        self.socket.sendall((str(msg)+"\n").encode('utf-8'))

    def receive(self):
        buffer = ""
        while True:
            p = self.socket.recv(1).decode('utf-8')
            if p != "\n":
                buffer += p
            else:
                break
        return buffer

    def close(self):
        self.socket.close()
