from tkinter import *
import pynput.keyboard
from pynput import keyboard, mouse
import threading
import Utils
timer = Utils.Timer()
logger = Utils.Logger()


class TempData:
    def __init__(self):
        self.self = self
        self.logging_data = None
        self.event_order = None
        self.settings = [True, True, True, True, True]
        self.killkey_type = int
        self.killkey = None
        self.mouse_movement_buffer = 100
        self.mouse_movement_i = 1


# This is the listener class, we utilize 2 instances of this one as for keyboard and one for mouse
class Listener(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.listener = None

    def configure_listener(self, settings):
        if len(settings) == 3:
            self.listener = pynput.mouse.Listener(on_move=settings_dict[settings[1]][0],
                                                  on_click=settings_dict[settings[0]][1],
                                                  on_scroll=settings_dict[settings[2]][2])
        else:
            self.listener = pynput.keyboard.Listener(on_press=on_press, on_release=on_release)
        self.listener.start()
        print("Listeners have been started.")

    def stop_listener(self):
        self.listener.stop()
        self.listener = None


temp_data = TempData()
keyboard_listener = Listener()
mouse_listener = Listener()


# Killkey Listeners
# Killkey Mouse
def killkey_on_move(x, y):
    mouse_listener.stop_listener()
    temp_data.killkey = 67
    temp_data.killkey_type = 3


def killkey_on_click(x, y, button, pressed):
    mouse_listener.stop_listener()
    temp_data.killkey = Utils.special_keys.index(button)
    temp_data.killkey_type = 2


def killkey_on_scroll(x, y, dx, dy):
    mouse_listener.stop_listener()
    temp_data.killkey = [dx, dy]
    temp_data.killkey_type = 4


# Killkey Keyboard
def killkey_on_press(key):
    keyboard_listener.stop_listener()
    temp_data.killkey = key
    if key in Utils.special_keys:
        temp_data.killkey_type = 0

    else:
        temp_data.killkey_type = 1


# Regular Listeners
# Mouse Listeners
def on_move(x, y):
    if temp_data.killkey == 67:
        kill_listeners()

    elif temp_data.mouse_movement_i <= temp_data.mouse_movement_buffer:
        temp_data.mouse_movement_i += 1

    else:
        temp_data.mouse_movement_i = 1
        timer.record_event_time([x,y], 0)


def on_click(x, y, button, pressed):
    special_key_index = Utils.special_keys.index(button)
    if special_key_index == temp_data.killkey:
        kill_listeners()

    elif pressed:
        timer.record_start_time(special_key_index)

    else:
        timer.record_end_time(special_key_index)


def on_scroll(x, y, dx, dy):
    if type(temp_data.killkey) == list:
        pass

    else:
        timer.record_event_time([dx, dy], 1)


# Keyboard Listeners
def on_press(key):
    try:
        if key == temp_data.killkey:
            kill_listeners()

        elif key.char not in timer.active_keys:
            timer.record_start_time(key.char)

    except AttributeError:
        special_key_index = Utils.special_keys.index(key)
        if special_key_index not in timer.active_keys:
            timer.record_start_time(special_key_index)


def on_release(key):
    try:
        if key.char in timer.active_keys:
            timer.record_end_time(key.char)

    except AttributeError:
        special_key_index = Utils.special_keys.index(key)
        if special_key_index in timer.active_keys:
            timer.record_end_time(special_key_index)


# This function is used to kill both listeners at the command of one function
def kill_listeners():
    temp_data.mouse_movement_i = 1
    timer.killkey_force_log(temp_data.settings)
    temp_data.logging_data = timer.logging_data
    temp_data.event_order = timer.event_order
    timer.reset()
    keyboard_listener.stop_listener()
    mouse_listener.stop_listener()
    print("Listeners have been killed.")


settings_dict = {1: [on_move, on_click, on_scroll], 0: [None, None, None]}
