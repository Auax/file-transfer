import socket
import os

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


inp_hostname = input('Enter server local IP: ')
hostname = inp_hostname  # servers ip
port = 1238
s.connect((hostname, port))

# set filename
filename = input('Please, type a filename, or simply press enter to save it with name of (output.txt): ')
if not filename:
    filename = 'output.txt'

# open file and add data
with open(filename, 'wb') as f:
    print('File opened successfully!\nReceiving data')

    while True:
        data = s.recv(1024)  # buffer size -- 1024

        print(f'Data: {data[:10]}[...]')

        if not data:
            break

        # write current data slot
        f.write(data)

print('File saved successfully!')

# close connection
s.close()
print('Connection closed')
