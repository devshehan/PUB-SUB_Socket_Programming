# server.py
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

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

subscribers = set()

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr}")

    is_publisher = False
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)

            if msg == DISCONNECT_MESSAGE:
                connected = False
            elif msg == PUBLISHER:
                is_publisher = True
            else:
                if is_publisher:
                    # Forward message to all subscribers
                    for subscriber_conn in subscribers:
                        try:
                            # subscriber_conn.send(str(msg_length).encode(FORMAT))
                            # subscriber_conn.send(msg.encode(FORMAT))
                            message = msg.encode(FORMAT)
                            msg_length = len(message)
                            send_length = str(msg_length).encode(FORMAT)
                            send_length += b' ' * (HEADER - len(send_length))
                            
                            subscriber_conn.send(send_length)
                            subscriber_conn.send(message)


                            print("Message sent to subscriber:", msg)
                        except socket.error as e:
                            print(f"Error sending message to subscriber: {e}")
                            subscribers.remove(subscriber_conn)
                            subscriber_conn.close()
                else:
                    # Subscriber connected, add to the subscribers set
                    subscribers.add(conn)
            
            print(f"[{addr}] {msg}")
            conn.send("received...msg".encode(FORMAT))

    conn.close()
    if is_publisher:
        print("[PUBLISHER DISCONNECTED]")
    else:
        print(f"[DISCONNECTED] {addr}")
        subscribers.remove(conn)

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {len(subscribers) + 1}")

print("[SERVER] started...!")
start()
