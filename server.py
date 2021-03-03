import socket
import select
import threading

HEADER_LENGTH = 10
IP = socket.gethostbyname(socket.gethostname())
PORT = 5541

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((IP, PORT))

server_socket.listen()

sockets_list = [server_socket]

clients = {}


def receive_message(client_socket): #code for receiving messages
    try:
        message_header = client_socket.recv(HEADER_LENGTH)
        if not len(message_header):  #lenght of message header
            return False

        message_length = int(message_header.decode('utf-8').strip()) #strip removes space bw a string
        return {'header': message_header, 'data': client_socket.recv(message_length)}



    except:
        return False


while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list) #read write error

    for notified_socket in read_sockets:
        if notified_socket == server_socket: #someone connected and we need to accept the connection
            client_socket, client_address = server_socket.accept() #accepting the connection
            user = receive_message(client_socket)
            if user is False: #if someone disconnected
                continue

            sockets_list.append(client_socket)

            clients[client_socket] = user

            print(f"Accepted New Connection from {client_address[0]}:{client_address[1]}:username:{user ['data'].decode('utf-8')}")

        else:

            message = receive_message(notified_socket)

            if message is False:
                print(f"Closed Connection from {clients[notified_socket]['data'].decode('utf-8')}")
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue

            user = clients[notified_socket]



            print(f"Received message from {user['data'].decode('utf-8')}: {message['data'].decode('utf-8')}")

            for client_socket in clients: #share message with everyone

                if client_socket != notified_socket:
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

    for notified_socket in exception_sockets:
         sockets_list.remove(notified_socket)
         del clients[notified_socket]
