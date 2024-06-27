# https://www.geeksforgeeks.org/socket-programming-python/
import socket
import base64

print('----------------------------------')

domain  = 'www.google.com'
#ip = socket.gethostbyname(domain)
ip = '192.168.68.1'
port  = 80

# example connecting to google server
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Socket: socket created!')
except Exception as e:
    print(f'Socket: error creating socket:', e)
    exit()

try:
    s.connect((ip, port))
    print('Socket: connected to server!')
except Exception as e:
    print('Socket: connection error:', e)
    exit()

print(f"""----------------------------------
Data:
- domain: {domain}
- ip: {ip}
- port: {port}
- socket name: {s.getsockname()}
----------------------------------""")

#s.send(bytes('echo', 'utf-8'))
# https://stackoverflow.com/questions/26768213/python-sockets-sending-a-packet-to-a-server-and-waiting-for-a-response

print('Socket: encoding message...')
encoded = base64.b64encode(b'Test from a random person using Python')
print('Socket: sending message...')
s.send(encoded)
print('Socket: awaiting reply...')
s.settimeout(10)
try:
    reply = s.recv(131072)
    print('Socket: reply:', end="")
    print(reply)
except Exception as e:
    print('Socket: reply error:', e)

print('Socket: closing socket...')
s.close()