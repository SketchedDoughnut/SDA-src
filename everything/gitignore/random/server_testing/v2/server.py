# first, make the recieving end
import socket


def listening_init():
    msg = 'Connection to server established.'.encode('utf-8')
    client.send(msg)
    print('Message sent!')

def send_message(msg: str):
    msg = msg.encode('utf-8')
    client.send(msg)
    print('Message sent!')

port = 12345  
host = socket.gethostname()

# set up local server
local_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
local_server.bind((host, port))

# set up out client
#out_client = socket.socket()
#out_client.connect(host, port)

# set up in client
print('Listening for a connection...')
local_server.listen(5)
client, address = local_server.accept()
local_server.close()
print('Got connection from', address)

listening_init()

while True:
    print('-------------')
    ins = input('Msg: ')
    if ins == 'exit':
        send_message('exit')
        break
    send_message(ins)

client.close()