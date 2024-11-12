import streamlit as st
import time, sys
import threading
import connection
import logic
import sys
from pages import database_mysql

st.set_page_config(
    page_title="Traning",
    page_icon="🏃‍♂️",
)

if 'conn_est_bool' not in st.session_state:
    st.session_state.conn_est_bool = False
if 'Connection_List' not in st.session_state:
    conn_list = {}
    def func(option):
        if option == None:
            st.toast('Please choose a number!')
            return

        holder2.button(f'Please wait! Seeking for {option} connections', disabled=True)
        with st.spinner('Waiting for esp32 connections'):
            generator = connection.start(option)
            for conn in generator:
                conn_list.update(conn)
                holder3.subheader(f':green[{ len(conn_list) }] new connection(s) made!')
        holder2.title('')
        time.sleep(2)
        st.session_state.Connection_List = conn_list
        st.session_state.conn_est_bool = True
    

    option = st.selectbox(
    'How many connections do you want to set up?',
    (1,2,3),
    index=None,
    )

    holder2 = st.empty()
    holder2.button('OK', on_click=func, args=(option,))

    holder3 = st.empty()

    while not st.session_state.conn_est_bool:
        pass

stop_event = threading.Event()
conn_error_event = threading.Event()
new_stop_watch = logic.stop_watch()
runner_info = database_mysql.get_runner_name(devide=True)
pause_queue = []

def saving_data(button_placeholder, timestamp:str, runner:int):
    col1, col2 = button_placeholder.columns(2)
    with col1:
        btn1 = st.button('Save this record', type='secondary', on_click=database_mysql.add_new_timestamp, args=(timestamp, runner))
    with col2:
        btn2 = st.button('Delete this record', type='secondary')

def start():
    new_stop_watch.reset()
    for i in range (3,0,-1):
        title_placeholder.title(f':red[{i}]')
        time.sleep(1)
    
    logic_thread = threading.Thread(target=logic.main_logic, args=(stop_event, conn_error_event, st.session_state.Connection_List, pause_queue, ), daemon=True)
    logic_thread.start()

    while not stop_event.is_set():
        try:
            if pause_queue.pop():
                msecond, second, minute,hour = new_stop_watch.get_current_time_stamp(string_format=False)
                stop_holder.subheader(f'{hour:02} : {minute:02} : {second:02} : {msecond:02}')
        except IndexError:
            pass

        msecond, second, minute,hour = new_stop_watch.run(string_format=False)
        title_placeholder.title(f'{hour:02} : {minute:02} : {second:02} : {msecond:02}')

    msecond, second, minute,hour = new_stop_watch.get_current_time_stamp(string_format=False)
    stop_holder.subheader(f'{hour:02} : {minute:02} : {second:02} : {msecond:02}')

#---------------main UI code ---------------------
st.title('TimeStamp')

runner_option = st.selectbox(
            'Choose runner name to save this new timestamp',
            runner_info[2],
            index= None,
        )

title_placeholder = st.empty()
title_placeholder.title('00:00:00:00')

button_placeholder = st.empty()
button_start = button_placeholder.button('Start', type='primary')

stop_holder = st.container()

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
            runner_id = int(runner_option[-3:])
            saving_data(button_placeholder,timestamp = new_stop_watch.get_current_time_stamp(string_format=True), runner = runner_id)
            
if runner_option != None:
    st.toast(f'New runner selected: {runner_option}')
