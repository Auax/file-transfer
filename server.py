import socket
import threading
import os
import time


def convert_unit(size):
    """
    Enter an int number in bytes and get it transformed.
    :param size: int
    :return list (int, str)
    """

    if size >= 1000000000:
        return round(size / 1073741824, 2), 'GB'  # return in MB

    if size >= 1000000:
        return round(size / 1048576, 1), 'MB'  # return in MB

    if size >= 1000:
        return round(size / 1000, 2), 'KB'  # return in KB

    if size <= 1000:
        return size, 'Bytes'


def wait_point(text):
    """
    Create simple dots animation with an string:
    E.g:
        Input : Hello world
        Output:
            - Hello world.
            - Hello world..
            - Hello world...
    """
    while True:

        for i in range(3):  # loop to animate each frame
            time.sleep(.5)  # frame velocity in seconds

            if terminate:  # break of for loop
                break

            os.system('cls')  # clear output

            if i == 0:
                print(f'{text}.')
            if i == 1:
                print(f'{text}..')
            if i == 2:
                print(f'{text}...')

        if terminate:  # break of while loop
            break


terminate = False  # determines if the wait_point function should stop

"""
Declaring sockets objects and configuring listening server
"""

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # defines an instance

port = 1238  # defines the actual port

s.bind(('', port))  # host by default
s.listen(5)  # up to five connections


def main():
    buffersize = 1024  # send buffer size

    while True:
        clientsocket, address = s.accept()  # accept connection
        print(f'Connection from {address} has been established!')

        global terminate
        terminate = True  # ends while loop in wait_point function

        path = input('Select file path: ')

        with open(path, 'rb') as f:  # open file to read content in binary mode

            l = f.read(buffersize)  # read

            file_size = os.stat(path).st_size
            print(file_size)
            send_size = 0
            while l:

                if buffersize > file_size:
                    buffersize = file_size

                send_size += buffersize
                if send_size > file_size:
                    send_size = file_size

                clientsocket.send(l)

                print(
                    f'{round(send_size * 100 / file_size, 2)}% | {convert_unit(send_size)[0]}{convert_unit(send_size)[1]} / {convert_unit(file_size)[0]}{convert_unit(file_size)[1]} -- Sent data: {repr(l)[:15]}...')
                l = f.read(1024)

        print('File successfully sent!')
        clientsocket.close()


x = 'Server initialized, waiting for client connection'

# Add threads
th1 = threading.Thread(target=wait_point, args=(x,)).start()  # wait_point function
th2 = threading.Thread(target=main).start()  # main function
