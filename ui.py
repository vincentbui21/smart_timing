import streamlit as st
import time
import asyncio
import socket,sys


if 'title' not in st.session_state:
    st.session_state.title = '00:00:00:00'


# get the hostname
def player_detected(conn):
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        if not data:
            # if data is not received break
            break
        elif str(data) == 'True':
            return 'True'
        elif str(data)=='False':
            return False

def start():
    host = '212.90.75.100'
    port = 8080  # initiate port no above 1024

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # get instance
    sockaddr = socket.getaddrinfo(host, port)[0][-1]
    print(sockaddr)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(5)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    st.write("Connection from: " + str(address))

    for i in range (1,4):
        st.session_state.title = 4-i
        title_placeholder.title(st.session_state.title)
        time.sleep(1)
    
    msecond = 0
    second = 0    
    minute = 0    
    hour = 0
    while(True):       
        time.sleep(1/1000)        
        msecond+=1    
        if msecond == 99:
            msecond = 0
            second +=1             
        if second == 60:    
            second = 0    
            minute+=1    
        if minute == 60:    
            minute = 0    
            hour+=1
        if player_detected(conn) == 'True':
            break
        title_placeholder.title(f'{hour:02} : {minute:02} : {second:02} : {msecond:02}')
        

st.title('TimeStamp')
title_placeholder = st.empty()
title_placeholder.title(st.session_state.title)

if st.button('Start'):
    start()