import socket
import select
import errno
import sys

HEADER_LENGTH = 10

IP = "10.147.19.220"
PORT = 5541

my_username = input("Enter Username: ")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
client_socket.setblocking(False)

username = my_username.encode("utf-8")
username_header = f"{len(username):<{HEADER_LENGTH}}".encode("utf-8")
client_socket.send(username_header + username )

while True:
    message = input(f"{my_username} >>> ")

    if message:
        message = message.encode("utf-8")
        message_header = (f"{len(message):<{HEADER_LENGTH}}".encode("utf-8"))
        client_socket.send(message_header + message)
    try:
        while True: #receive things
           username_header = client_socket.recv(HEADER_LENGTH)
           if not len(username_header):
               print("Error!")
               print("Connection Closed By The Server")
               print("Please Login Again")
               sys.exit()
           username_length= int(username_header.decode('utf-8').strip())
           username = client_socket.recv(username_length).decode('utf-8') #receiving the message header of same as message header in server

           message_header = client_socket.recv(HEADER_LENGTH)
           message_length = int(message_header.decode('utf-8').strip())
           message =  client_socket.recv(message_length).decode('utf-8')

           print(f"{username} >>> {message} ")

    except IOError as e:  #IF THERES AN ERROR IN RUNNING THE PROGRAM
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading Error, Please try again', str(e))
            sys.exit()
        continue

    except Exception as e:
        print("error",str(e))
        print("Error Type : General Error")
        sys.exit()
