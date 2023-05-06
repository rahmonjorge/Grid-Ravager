import socket
import pickle
from _thread import *

from player import Player
import pygame

SERVER_IP = '26.52.183.15'
PORT = 6942
BUFFER_SIZE = 16384

BLOCK_SIZE = 20
players = [Player(BLOCK_SIZE, 'red'), Player(BLOCK_SIZE, 'blue'), Player(BLOCK_SIZE, 'purple'), Player(BLOCK_SIZE, 'orange')]
MAX_CLIENTS = len(players)

skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    skt.bind((SERVER_IP, PORT))
except socket.error as e:
    print(e)
    if e.winerror == 10048:
        quit('There is already a server running at {}:{}.'.format(SERVER_IP,PORT))

skt.listen(MAX_CLIENTS)

print('Server up and running, hosted at {ip}:{port} and expecting up to {clients} clients.'.format(ip=SERVER_IP, port=PORT,clients=MAX_CLIENTS))

def threaded_client(skt, player_index):

    if player_index >= MAX_CLIENTS:
        print('Error: Invalid player index: {}'.format(player_index))
        return

    skt.send(pickle.dumps(players[player_index])) # sends the newly created object to the client
    reply = ''
    exit_reason = 'Unknown'
    exit_code = -1
    global players_online
    players_online.append(player_index)
    print('Player {} connected.'.format(player_index))
    print('Players online: {}'.format(players_online))

    while True:
        try:
            bytes = skt.recv(BUFFER_SIZE)

            # DEBUG
            #print('DEBUG: ' + str(len(bytes)) + ' bytes')

            if len(bytes) >= BUFFER_SIZE:
                exit_reason = 'Client exploded the buffer size: ' + str(len(bytes)) + " >= " + str(BUFFER_SIZE)
                exit_code = 1
            data = pickle.loads(bytes) # receives the player object sent by the client
            players[player_index] = data # updates the current player
            if not data:
                print('Player {} disconnected.'.format(player_index))
                break
            else:
                reply = [players[x] for x in range(MAX_CLIENTS) if (x is not player_index) and (x in players_online)]

            skt.sendall(pickle.dumps(reply)) # sends other players objects to the client
        except socket.error as e:
            print(e)
            break
        except pickle.UnpicklingError as e:
            print('ERROR: ' + str(e))
            exit_code = 1
            break
        except EOFError as e:
            exit_reason = 'Client disconnected.'
            exit_code = 0
            break
    
    players_online.remove(player_index)

    print('Connection with player {} has ended.'.format(player_index))
    print('Reason: {} (Exit Code {})'.format(exit_reason, exit_code))
    print('Players online: {}'.format(players_online))

    if exit_code == 1:
        print('Proceeding to destroy player {} block cache...'.format(player_index))
        count = len(players[player_index].blocks)
        players[player_index].blocks.clear()
        print('Destroyed {} blocks from player {}.'.format(count, player_index))

    skt.close()

global players_online
players_online = []

while True:
    client_skt, client_addr = skt.accept()
    print('Connected to: ', client_addr)

    index = next(x for x in range(MAX_CLIENTS) if x not in players_online)

    start_new_thread(threaded_client, (client_skt, index))