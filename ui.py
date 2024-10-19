import streamlit as st
import time
import asyncio
import socket,sys
import threading

if 'title' not in st.session_state:
    st.session_state.title = '00:00:00:00'
if 'conn' not in st.session_state:
    with st.spinner('Waiting for connection from ESP32...'):
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

        st.session_state.conn = conn
    st.success('Socket connection established!')

stop_event = threading.Event()


def player_detected(conn):
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        if not data:
            # if data is not received break
            break
        elif str(data) == 'True':
            stop_event.set()
        elif str(data)=='False':
            pass


def start():
    for i in range (1,4):
        st.session_state.title = 4-i
        title_placeholder.title(st.session_state.title)
        time.sleep(1)
    
    myThread = threading.Thread(target=player_detected, daemon=True, args=(st.session_state.conn,))
    myThread.start()

    msecond = 0
    second = 0    
    minute = 0    
    hour = 0
    while not stop_event.is_set():       
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
        title_placeholder.title(f'{hour:02} : {minute:02} : {second:02} : {msecond:02}')
        

st.title('TimeStamp')
title_placeholder = st.empty()
title_placeholder.title(st.session_state.title)

if st.button('Start'):
    start()