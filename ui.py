import streamlit as st
import time, sys
import threading
import connection
import logic
import sys

st.set_page_config(
    page_title="Traning",
    page_icon="🏃‍♂️",
)

if 'runner' not in st.session_state:
    st.session_state.runner = 'None'
if 'Connection_List' not in st.session_state:
    with st.spinner('Waiting for esp32 connections'):
        st.session_state.Connection_List = connection.start(1)

stop_event = threading.Event()
conn_error_event = threading.Event()

def saving_data(button_placeholder, timestamp:str):
    from pages.database import update_new_timestamp

    col1, col2 = button_placeholder.columns(2)
    col1.button('Save this record', on_click= update_new_timestamp(timestamp=timestamp, runner=runner_option))
    if col2.button('Delete this record', type='secondary'):
        pass
        
def start():
    logic.reset_stop_watch()
    for i in range (3,0,-1):
        title_placeholder.title(i)
        time.sleep(1)
    
    logic_thread = threading.Thread(target=logic.main_logic, args=(stop_event, conn_error_event, st.session_state.Connection_List,), daemon=True)
    logic_thread.start()

    while not stop_event.is_set():
        msecond, second, minute,hour = logic.run_stop_watch()
        title_placeholder.title(f'{hour:02} : {minute:02} : {second:02} : {msecond:02}')

#---------------main UI code ---------------------
st.title('TimeStamp')

runner_option = st.selectbox(
            'Choose runner name to save this new timestamp',
            ('VINCENT', 'ERIC', 'KELVIN'),
            index= None,
        )

title_placeholder = st.empty()
title_placeholder.title('00:00:00:00')

button_placeholder = st.empty()
button_start = button_placeholder.button('Start', type='primary')

if button_start:
    if runner_option == None:
        st.warning('Please choose a runner name first!')
        st.stop()
    else:
        button_placeholder.button('Running', disabled = True)
        start()

        if conn_error_event.is_set():
            st.error('Connection Error - Stop-watch stopped')
            st.warning("Please recheck all the ESP32 then delete page's cache before trying again")
            button_placeholder.button('OK',type='primary')
        else:
            saving_data(button_placeholder,timestamp = logic.current_time_stamp(True))

if runner_option != None:
    st.toast(f'New runner selected: f{runner_option}')