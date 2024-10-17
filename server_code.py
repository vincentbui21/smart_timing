import socket,sys

# get the hostname
host = '212.90.75.100'
port = 8080  # initiate port no above 1024

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # get instance
# look closely. The bind() function takes tuple as argument
sockaddr = socket.getaddrinfo(host, port)[0][-1]
print(sockaddr)

#server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
#server_socket.bind(sockaddr)  # bind host address and port together
server_socket.bind((host, port))  # bind host address and port together

# configure how many client the server can listen simultaneously
server_socket.listen(1)
conn, address = server_socket.accept()  # accept new connection
print("Connection from: " + str(address))

def player_detected():
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        if not data:
            # if data is not received break
            pass
        else:
            print("from connected user: " + str(data))
            return str(data)
        #data = input(' -> ')
        #conn.send(data.encode())  # send data to the client

    conn.close()  # close the connection


if __name__ == '__main__':
    player_detected()
    