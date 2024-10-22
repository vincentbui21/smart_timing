import streamlit as st
import time, sys
import threading
import server_code

st.set_page_config(
    page_title="Traning",
    page_icon="🏃‍♂️",
)

if 'title' not in st.session_state:
    st.session_state.title = '00:00:00:00'
if 'conn' not in st.session_state: #Establish socket connection
    with st.spinner('Waiting for connection from ESP32...'):
        conn = server_code.set_up_server()
        st.session_state.conn = conn
    st.success('Socket establish successfully') #This will be return no matter the result 
if 'runner' not in st.session_state:
    st.session_state.runner = 'None'



stop_event = threading.Event()

def start(button_placeholder):
    server_code.reset_stop_watch()

    button_placeholder.button('Running', disabled = True)

    for i in range (3,0,-1):
        st.session_state.title = i
        title_placeholder.title(st.session_state.title)
        time.sleep(1)
    
    player_detect_Thread = threading.Thread(target=server_code.player_detected, daemon=True, args=(st.session_state.conn, stop_event, ))
    player_detect_Thread.start()
    
    while not stop_event.is_set():
        msecond, second, minute,hour = server_code.stop_watch()
        title_placeholder.title(f'{hour:02} : {minute:02} : {second:02} : {msecond:02}')

    st.session_state.title='00:00:00:00' #reset cache to 0

#---------------main UI code ---------------------
st.title('TimeStamp')
option = st.selectbox(
"Runner session",
("VINCENT", "ERIC", "KELVIN"),
index=None,
placeholder ="Select runner here"
)

title_placeholder = st.empty()
title_placeholder.title(st.session_state.title)

button_placeholder = st.empty()

if button_placeholder.button('Start'):
    start(button_placeholder)

    msecond, second, minute,hour = server_code.current_time_stamp()
    title_placeholder.title(f'{hour:02} : {minute:02} : {second:02} : {msecond:02}')

    timestamp = f'{hour:02} : {minute:02} : {second:02} : {msecond:02}'

    col1, col2 = button_placeholder.columns(2)
    if col1.button('Save this record',type='primary'):
        st.session_state.ws_conn.update(spreadsheet=st.session_state.ws_url, worksheet= st.session_state.ws_id.get('vincent_ws_id'), data=timestamp)
    if col2.button('delete this record', type='primary'):
        pass



if option == 'VINCENT':
    st.session_state.runner = option
elif option =='ERIC':
    st.session_state.runner = option
elif option =='KELVIN':
    st.session_state.runner = option
