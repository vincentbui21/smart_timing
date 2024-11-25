import socket
import threading
import random
import ngrok

# IP = socket.gethostbyname(socket.gethostname())
# IP = '10.214.33.15'
IP = 'localhost'
PORT = 8080
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"
temp :list[socket.socket] = []
CONN_LIST = {}

def handle_client(conn:socket.socket) -> None:
    connected = True
    while connected:
        msg = 'Start'
        conn.send(msg.encode(FORMAT))

        msg = conn.recv(SIZE).decode(FORMAT)
        if msg == 'True':
            print(f'From client: {msg}')
            msg = 'Stop'
            conn.send(msg.encode(FORMAT))
            connected = False
        else:
            pass  

def stop(conn:socket.socket):
    msg = DISCONNECT_MSG
    conn.send(msg.encode(FORMAT))
    conn.close()

def start(max_conn=2):
    """ Open a socket connection, return that connection.
    The 'max_conn' parameter is by default 2. It is the number of connection the server will listen to.
    """
    CURR_CONN = 0
    print("[STARTING] Server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(ADDR)
    server.listen(5)
    print(f"[LISTENING] Server is listening on {IP}:{PORT}")

    while CURR_CONN < max_conn:
        conn, addr = server.accept()
        print(f'New connection from: {addr}')
        CURR_CONN+=1
        CONN_LIST.update({CURR_CONN:conn})
        yield {CURR_CONN:conn}
    # return CONN_LIST

def main(stop_event: threading.Event = None) -> None:
    global temp
    temp = list(CONN_LIST.keys())
    random.shuffle(temp)

    for each_conn in temp:
        handle_client(CONN_LIST.get(each_conn))
    
    if stop_event is not None:
        stop_event.set()

    print('Done')

if __name__ == "__main__":
    a = start()
    next(a)
    while True:
        main()
        continueq = input('Do you want to continue: ')
        if continueq == 'no':
            for each_conn in temp:
                stop(CONN_LIST.get(each_conn))
            break
        else:
            pass
