import socket
import pickle
from _thread import *

from player import Player

# consts
DISPLAY_WIDTH = 1280
DISPLAY_HEIGHT = 720
BLOCK_SIZE = 20
MOVE_DISTANCE = 20

SERVER_IP = "26.52.183.15"
PORT = 6942
MAX_CLIENTS = 3

player1 = Player(DISPLAY_WIDTH / 2 + (BLOCK_SIZE * 1), DISPLAY_HEIGHT / 2, BLOCK_SIZE, "red")
player2 = Player(DISPLAY_WIDTH / 2 + (BLOCK_SIZE * 2), DISPLAY_HEIGHT / 2, BLOCK_SIZE, "blue")
player3 = Player(DISPLAY_WIDTH / 2 + (BLOCK_SIZE * 3), DISPLAY_HEIGHT / 2, BLOCK_SIZE, "purple")

players = [player1, player2, player3]

def main():
    skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        skt.bind((SERVER_IP, PORT))
    except socket.error as e:
        print(str(e))

    skt.listen(MAX_CLIENTS)
    print("Server up and running, hosted at {ip}:{port} and expecting up to {clients} clients."
          .format(ip=SERVER_IP, port=PORT,clients=MAX_CLIENTS))
    
    current_player_number = 0

    while True:
        client_skt, client_addr = skt.accept()
        print("Connected to: ", client_addr)

        start_new_thread(threaded_client, (client_skt, current_player_number))
        current_player_number += 1

def threaded_client(skt, player):

    # player = Player(DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2, BLOCK_SIZE, colors[player])

    skt.send(pickle.dumps(players[player])) # sends the newly created player object to the client

    reply = []

    print("Player {} connected.".format(player))

    while True:
        try:
            data = pickle.loads(skt.recv(2048)) # receives the player object sent by the client

            if player < MAX_CLIENTS:
                players[player] = data # updates the current player
            else:
                print("Error: Invalid player index: {}".format(player))
                break

            if not data:
                print("Player {} disconnected.".format(player))
                break
            else:
                if player == 0:
                    reply = [players[1], players[2]]
                elif player == 1:
                    reply = [players[0], players[2]]
                elif player == 2:
                    reply = [players[0], players[1]]
                else:
                    print("Error: Invalid player index: {}".format(player))
            skt.sendall(pickle.dumps(reply)) # sends other players objects to the client
        except:
            break

    print("Lost connection with player {}.".format(player))
    skt.close()

main()