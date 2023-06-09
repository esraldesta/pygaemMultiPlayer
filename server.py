import socket
from _thread import *
from player import Player
import pickle

server = "10.240.69.149"
port = 5566

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")


player1 = Player("esral",0,300,50,50,(255,0,0))
player2 = Player("desta",900,300, 50,50, (0,0,255))
players = [player1,player2]

def threaded_client(conn, player):
    conn.send(pickle.dumps(players[player]))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(4096))
            old_health = players[player].health
            players[player] = data
            players[player].health = old_health
            # print(players[player].name,players[player].health)

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    if players[0].health <=0:
                        players[0].thereisawinner = True
                        players[1].thereisawinner = True
                        players[1].winner = True
                        # print("there is a winner")
                    if players[1].health <=0:
                        players[0].thereisawinner = True
                        players[1].thereisawinner = True
                        players[0].winner = True
                        # print("there is a winner")
                    players[0].op_health = players[1].health
                    reply = players[0]
                    if players[1].hitflag == True:
                        players[0].health -=1
                        players[1].hitflag = False
                    conn.sendall(pickle.dumps(reply))
                if player == 0:
                    if players[0].health <=0:
                        players[0].thereisawinner = True
                        players[1].thereisawinner = True
                        players[1].winner = True
                        # print("there is a winner")
                    if players[1].health <=0:
                        players[0].thereisawinner = True
                        players[1].thereisawinner = True
                        players[0].winner = True
                        # print("there is a winner")
                    players[1].op_health = players[0].health
                    reply = players[1]
                    if players[0].hitflag == True:
                        players[1].health -=1
                        players[0].hitflag = False
                    conn.sendall(pickle.dumps(reply))

        except:
            break

    print("Lost connection")
    conn.close()

currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1