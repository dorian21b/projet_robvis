import socket
import sys

HOST = ""
PORT = 6666

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

try:
    s.bind(HOST,PORT)
except:
    print('fail')
    sys.exit()

s.listen(1)

conn,adr = s.accept()

print('conn')
conn.send(bytes(55))