import time
import threading
from tkinter import *
from pynput.keyboard import Key, Listener


def thread_function():
    root = Tk()
    button = Button(text="fuck you")
    button.pack()
    root.mainloop()


x = threading.Thread(target=thread_function())
x.start()
x.join()
print("fuck")


class TimerHandler:
    def __init__(self):
        self.button_active = False
        self.start_time = 0.0
        self.end_time = 0.0
        self.total_time = 0.0

    def start_timer(self):
        self.start_time = time.time()
        print(self.start_time)

    def stop_timer(self):

        self.end_time = time.time()
        print(self.end_time - self.start_time)
        self.total_time = (self.end_time - self.start_time) + self.total_time


t = TimerHandler()


start_time = time.time()


def on_press(key):
    print('{0} pressed'.format(key))
    if not t.button_active:
        t.button_active = True
        t.start_timer()


def on_release(key):
    print('{0} released'.format(key))
    t.stop_timer()
    t.button_active = False
    print(t.total_time)
    if key == Key.esc:
        return False


with Listener(
        on_press=on_press,
        on_release=on_release

) as listener:
    listener.join()

