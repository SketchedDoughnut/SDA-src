# first of all import the socket library 
import socket     

import threading
 
def get_incoming():
    while True:
        incoming = server.recv(1024)
        incoming = base64.b64decode(incoming)
        incoming = incoming.decode('utf-8')
        print('Recieved message:', incoming)
        if incoming == 'exit':
            break

# next create a socket object 
server = socket.socket()         
print("Socket successfully created!")
 
# reserve a port on your computer -> can be anything
port = 12345               

# empty first means wait for ip
server.bind(('', port))         
print("socket binded to %s" %(port)) 
 
# put the socket into listening mode 
server.listen(5)     
print("socket is listening...")            

# Establish connection with client. 
client, addr = server.accept()
print('Got connection from', addr)

# send a thank you message to the client. encoding to send byte type. 
#client.send('Thank you for connecting'.encode()) 
import base64
client.send(base64.b64encode('Thank your connecting!'.encode('utf-8'))) # alternatively, use "b" prefix to string
print('Message sent!')

# Close the connection with the client 
print('Closing...')
client.close()

# https://stackoverflow.com/questions/12993276/errno-10061-no-connection-could-be-made-because-the-target-machine-actively-re
# https://stackoverflow.com/questions/55302927/what-ip-address-should-be-used-in-a-client-server-program