# publisher.py
import socket

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
PUBLISHER = "publisher"

publisher = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
publisher.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    
    publisher.send(send_length)
    publisher.send(message)
    print(publisher.recv(2048).decode(FORMAT))

if __name__ == "__main__":
    send(PUBLISHER)

    terminal_connected = True
    while terminal_connected:
        print("Enter the message (or type '!DISCONNECT' to exit): ", end=' ')
        input_string = input()
        if input_string == DISCONNECT_MESSAGE:
            send(DISCONNECT_MESSAGE)
            terminal_connected = False
        else:
            send(input_string)

publisher.close()
