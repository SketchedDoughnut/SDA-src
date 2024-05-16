import socket
import os
import time

port = 12345
host = socket.gethostname()
host = socket.gethostbyname('www.google.com')
host = "8.8.8.8"

targetAddr = str(input('Enter other players IP: '))
print('--------------------')
print('Searching for connection...')
outbound = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
inbound = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
inbound.bind((host, port))
inbound.listen(5)
client, address = inbound.accept()


# while True:
#     try:
#         outbound.connect((host, port))
#         break
#     except KeyboardInterrupt:
#         print('\nKeyboard intterupt: Cancelling by user request.')
#         exit()
#     except:
#         print('Failed. Exiting.')
#         exit()