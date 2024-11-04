import connection
import random
import time
import threading
import socket

def main_logic(stop_event: threading.Event, connection_error: threading.Event, conn_list:list[socket.socket]):
    """
    This functions randomly suffle the list of all the connections made, then send the command to the client and wait for data return before moving on the the next client 
    """
    print('Main logic is running!')
    temp = list(conn_list.keys())
    random.shuffle(temp)
    while not stop_event.is_set():
        each_conn:socket.socket
        for each_conn in temp:
            try:
                connection.handle_client(conn_list.get(each_conn))
            except (ConnectionResetError, ConnectionAbortedError, ConnectionError):
                print('Connection error')
                connection_error.set()
        stop_event.set()

msecond = 0
second = 0    
minute = 0    
hour = 0

def run_stop_watch():
    '''
    This functions run the stop-watch then return back the stop-watch digits: milisecond, second, minute, hour
    '''
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
    '''This function delete the cache of the previous stopwatch. This functions should be called before running a new one'''
    global msecond
    global second
    global minute
    global hour

    msecond = 0
    second = 0    
    minute = 0    
    hour = 0

def current_time_stamp(string_format:bool):
    '''This function return current digits of stop-watch: msecond, second, minute, hour. The "string-format parameter is a boolean type, if it's set to True, then it will return a string, if not then a tuple is of int digits "'''
    global msecond
    global second
    global minute
    global hour
    if string_format:
        return f'{hour:02}:{minute:02}:{second:02}:{msecond:02}'
    else:
       return msecond, second, minute, hour 


if __name__ == '__main__':
    while True:
        run_stop_watch()
        print(current_time_stamp(string_format=True))