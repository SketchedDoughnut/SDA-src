# Import socket module 
import socket     

# Create a socket object 
s = socket.socket()         
 
# Define the port on which you want to connect 
port = 12345               
 
# connect to the server
host = socket.gethostname()
s.connect((host, port))
 
# receive data from the server and decoding to get the string.
print(s.recv(1024).decode('utf-8'))

# close the connection 
s.close()