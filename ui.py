import streamlit as st
import time
import asyncio
import socket,sys

if 'title' not in st.session_state:
    st.session_state.title = '00:00:00:00'


# get the hostname
host = '212.90.75.100'
port = 8080  # initiate port no above 1024

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # get instance
sockaddr = socket.getaddrinfo(host, port)[0][-1]
print(sockaddr)

server_socket.bind((host, port))  # bind host address and port together

# configure how many client the server can listen simultaneously
server_socket.listen(5)
conn, address = server_socket.accept()  # accept new connection
print("Connection from: " + str(address))
st.write("Connection from: " + str(address))

def start():
    for i in range (1,4):
        st.session_state.title = i
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
        if player_detected():
            pass
        title_placeholder.title(f'{hour:02} : {minute:02} : {second:02} : {msecond:02}')

st.title('TimeStamp')
title_placeholder = st.empty()
title_placeholder.title(st.session_state.title)

if st.button('Start'):
    start()