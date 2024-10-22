import socket
import time

#---initialize stopwatch-----
msecond = 0
second = 0    
minute = 0    
hour = 0
#-----------------------------

def set_up_server():
    host = '212.90.75.143'
    #host = '192.168.206.231'
    port = 8080  # initiate port no above 1024

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # get instance
    sockaddr = socket.getaddrinfo(host, port)[0][-1]
    print(sockaddr)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(5)
    conn, address = server_socket.accept()  # accept new connection
    return conn

def player_detected(conn, stop_event):
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        if not data:
            # if data is not received break
            break
        elif str(data) == 'True':
            stop_event.set()
            break
        elif str(data)=='False':
            pass

def stop_watch():
    global msecond
    global second
    global minute
    global hour 

    time.sleep(1/100)
    msecond+=1    
    if msecond == 99:
        msecond = 0
        second +=1             
    elif second == 60:    
        second = 0    
        minute+=1    
    elif minute == 60:    
        minute = 0    
        hour+=1
    return msecond,second,minute,hour

def reset_stop_watch():
    global msecond
    global second
    global minute
    global hour

    msecond = 0
    second = 0    
    minute = 0    
    hour = 0

def current_time_stamp():
    global msecond
    global second
    global minute
    global hour
    return msecond,second,minute,hour 