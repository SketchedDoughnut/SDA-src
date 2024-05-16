# Import socket module 
import socket     

port = 12345 
host = socket.gethostname()                 

while True:
    # connect to the server
    print('Searching for connection...')
    messenger = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   
    while True:
        try:
            messenger.connect((host, port))
            break
        except:
            pass
    
    # receive data from the server and decoding to get the string.
    while True:
        try:
            msg = (messenger.recv(1024).decode('utf-8'))
        except:
            print('Connection to server lost.')
            messenger.close()
            break

        if msg == 'exit':
            print('Recieved message:', msg)
            break
        else:
            print('Recieved message:', msg)

    if msg == 'exit':
        break

# close the connection 
messenger.close()