import socket

#IP = socket.gethostbyname(socket.gethostname())
#IP = '192.168.63.135'
PORT = 17736
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    print(f"[CONNECTED] Client connected to server at {IP}:{PORT}")

    connected = True
    while connected:
        msg = client.recv(SIZE).decode(FORMAT)
        print(f"[SERVER] {msg}")
        
        if msg == DISCONNECT_MSG:
            connected = False
        elif msg == 'Start':
            msg = input("> ")
            client.send(msg.encode(FORMAT))

if __name__ == "__main__":
    main()