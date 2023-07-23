import socket
import threading

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
SUBSCRIBER = "subscriber"
PUBLISHER = "publisher"

# print(SERVER)

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDR)

subscribers_set = set()
publishers_set = set()

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr}")

    STATUS = ""

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            
            if(msg == DISCONNECT_MESSAGE):
                connected = False

            if(msg == SUBSCRIBER):
                subscribers_set.add(addr)
            
            if(msg == PUBLISHER):
                STATUS = PUBLISHER
            elif(STATUS == PUBLISHER):
                STATUS = ""
                for subscriber_addr in subscribers_set:
                    subscriber_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    try:
                        subscriber_conn.connect(subscriber_addr)
                        messeage = msg.encode(FORMAT)
                        msg_length = len(messeage)
                        msg_length = str(msg_length).encode(FORMAT)
                        msg_length = b' ' * (HEADER - len(msg_length))

                        subscriber_conn.send(msg_length)
                        subscriber_conn.send(msg.encode(FORMAT))
                    except:
                        # Handle connection errors if necessary
                        pass
                    finally:
                        subscriber_conn.close()

            print(f"[{addr}] {msg}")
            conn.send("recived...msg".encode(FORMAT))

    conn.close()

def start():
    server.listen()
    print(f"[LISTINING] Server is listening on {SERVER}")
    conn, addr = server.accept()
    thread = threading.Thread(target=handle_client, args=(conn,addr))
    thread.start()
    print(f"[ACTIVE CONNECTIONS] {threading.active_count()-1}")


print("[SERVER] started...!")
start()


