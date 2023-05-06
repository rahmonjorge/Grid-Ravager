import socket
import pickle

BUFFER_SIZE = 16384

# class used by the client to connect to the server
class Network:
    def __init__(self):
        self.skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "26.52.183.15"
        self.port = 6942
        self.address = (self.server, self.port)
        self.player = self.connect()

    def get_player(self):
        return self.player

    def connect(self):
        try:
            self.skt.connect(self.address) # establish connection with the server
            return pickle.loads(self.skt.recv(BUFFER_SIZE)) # gets the player object from server
        except:
            pass

    def send(self, data):
        try:
            self.skt.send(pickle.dumps(data))
            return pickle.loads(self.skt.recv(BUFFER_SIZE))
        except socket.error as e:
            print(e)
            if e.winerror == 10054:
                quit('Disconnected by server.')