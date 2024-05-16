from cryptography.fernet import Fernet
import time

# working decryption example
# key = Fernet.generate_key()
# f = Fernet(key)
# base_string = (b'Hello World!')
# encrypted = f.encrypt(base_string)
# decrypted = f.decrypt(encrypted)

# print(f"""DATA:
# - {key}
# - {f}
# - {base_string}
# - {encrypted}
# - {decrypted}""")

# attempt to open a file, and encrypt its contents. Use a previous established key
path = 'everything/main/top/starter.py'
key = b'5VsQ04U13bSDhhbv8Uk9nFbPfPY1VGoVhkA87JDyYdA='
f = Fernet(key)
print('Reading...')
file = open(path, 'rb')
#file_content = bytes(file.read(), 'utf-8')
file_content = file.read()
file.close()

print('Encrypting...')
encrypted = f.encrypt(file_content)

print('Writing...')
file = open(path, 'wb')
file.write(encrypted)
file.close()

input('Enter anything to proceed to decryption: ')

print('Reading...')
file = open(path, 'rb')
#file_content = bytes(file.read(), 'utf-8')
file_content = file.read()
file.close()

print('Decrypting...')
key = b'5VsQ04U13bSDhhbv8Uk9nFbPfPY1VGoVhkA87JDyYdA='
f = Fernet(key)
decrypted = f.decrypt(file_content)

# print('Writing...')
# file = open(path, 'wb')
# file.write(encrypted)
# file.close()

# print('Running...')
# exec(decrypted)