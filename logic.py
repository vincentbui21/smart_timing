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

class stop_watch():
    def __init__(self):
        self.msecond = 0
        self.second = 0
        self.minute = 0
        self.hour = 0
    
    def reset(self):
        self.msecond = 0
        self.second = 0
        self.minute = 0
        self.hour = 0

    def run(self, string_format : bool):
        time.sleep(1/100)
        self.msecond+=1    
        if self.msecond == 99:
            self.msecond = 0
            self.second +=1             
        elif self.second == 60:    
            self.second = 0    
            self.minute+=1    
        elif self.minute == 60:    
            self.minute = 0    
            self.hour+=1
        
        if string_format:
            return f'{self.hour:02}:{self.minute:02}:{self.second:02}:{self.msecond:02}'
        else:
            return self.msecond, self.second, self.minute, self.hour

    def get_current_time_stamp(self, string_format:bool):
        if string_format:
            return f'{self.hour:02}:{self.minute:02}:{self.second:02}:{self.msecond:02}'
        else:
            return self.msecond, self.second, self.minute, self.hour
    
if __name__ == '__main__':
    new_stop_watch = stop_watch()
    while True:
        print(new_stop_watch.run(string_format=True))