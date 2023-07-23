# subscriber.py
import socket

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
SUBSCRIBER = "subscriber"

subscriber = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
subscriber.connect(ADDR)

def receive_message():
        msg_length = subscriber.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = subscriber.recv(msg_length).decode(FORMAT)
            return msg

    # msg_length = subscriber.recv(HEADER).decode(FORMAT)
    # if msg_length:
    #     msg_length = int(msg_length)
    #     msg = b""
    #     while len(msg) < msg_length:
    #         chunk = subscriber.recv(msg_length - len(msg))
    #         if not chunk:
    #             break
    #         msg += chunk
    #     return msg.decode(FORMAT)
    # return None


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    
    subscriber.send(send_length)
    subscriber.send(message)
    print(subscriber.recv(2048).decode(FORMAT))

send(SUBSCRIBER)

connected = True
while connected:
    msg = receive_message()
    if msg is not None:
        if msg == DISCONNECT_MESSAGE:
            connected = False
            print("Disconnected from server.")
        else:
            print("Received message from server:", msg)

subscriber.close()
