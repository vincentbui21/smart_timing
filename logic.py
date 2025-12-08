import connection
import random
import time
import threading
import socket
import asyncio


def main_logic(
    stop_event: threading.Event,
    connection_error: threading.Event,
    conn_list,
    pause_queue: list,
    sequence_method,
):
    """
    This functions randomly suffle the list of all the connections made, then send the command to the client and wait for data return before moving on the the next client
    """
    # print("Main logic is running!")
    temp = conn_list

    if sequence_method == "Randomly":
        random.shuffle(temp)
    elif sequence_method == "Manually":
        pass

    while not stop_event.is_set():
        each_conn: socket.socket
        for each_conn in temp:
            try:
                connection.handle_client(each_conn)
                pause_queue.append(True)
            except (ConnectionResetError, ConnectionAbortedError, ConnectionError):
                print("Connection error")
                connection_error.set()
        stop_event.set()


""" class stop_watch:
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

    def run(self, string_format: bool):
        # time.sleep(1 / 100)
        start = time.perf_counter()

        while True:
            elapsed = time.perf_counter() - start
            if elapsed >= 1/100:
                break


        self.msecond += 1
        if self.msecond == 99:
            self.msecond = 0
            self.second += 1
        elif self.second == 60:
            self.second = 0
            self.minute += 1
        elif self.minute == 60:
            self.minute = 0
            self.hour += 1

        if string_format:
            return f"{self.hour:02}:{self.minute:02}:{self.second:02}:{self.msecond:02}"
        else:
            return self.msecond, self.second, self.minute, self.hour

    def get_current_time_stamp(self, string_format: bool):
        if string_format:
            return f"{self.hour:02}:{self.minute:02}:{self.second:02}:{self.msecond:02}"
        else:
            return self.msecond, self.second, self.minute, self.hour """

import time
import threading

class stop_watch:
    def __init__(self):
        self.msecond = 0
        self.second = 0
        self.minute = 0
        self.hour = 0
        self._lock = threading.Lock()
        self._running = False
        self._last_time = None

    def reset(self):
        with self._lock:
            self.msecond = 0
            self.second = 0
            self.minute = 0
            self.hour = 0
            self._last_time = None

    def start(self):
        with self._lock:
            if not self._running:
                self._running = True
                self._last_time = time.perf_counter()
                threading.Thread(target=self._run_thread, daemon=True).start()

    def stop(self):
        print("Stop the stop watch")
        with self._lock:
            self._running = False

    def _run_thread(self):
        while True:
            with self._lock:
                if not self._running:
                    break
                now = time.perf_counter()
                elapsed = now - self._last_time
                self._last_time = now

                total_centiseconds = int(elapsed * 100)
                self.msecond += total_centiseconds

                while self.msecond >= 100:
                    self.msecond -= 100
                    self.second += 1
                while self.second >= 60:
                    self.second -= 60
                    self.minute += 1
                while self.minute >= 60:
                    self.minute -= 60
                    self.hour += 1
            time.sleep(0.01)  # let time actually pass before the next loop

    def get_current_time_stamp(self, string_format: bool):
        with self._lock:
            if string_format:
                return f"{self.hour:02}:{self.minute:02}:{self.second:02}:{self.msecond:02}"
            else:
                return self.msecond, self.second, self.minute, self.hour



if __name__ == "__main__":
    # new_stop_watch = stop_watch()
    # while True:
    #     print(new_stop_watch.run(string_format=True))

    sw = stop_watch()
    sw.start()

    for _ in range(10):
        print(sw.get_current_time_stamp(True))
        time.sleep(1)

