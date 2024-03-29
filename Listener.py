from tkinter import *
import pynput.keyboard
from pynput import keyboard, mouse
import threading
import os
from MacroHandler import MacroHandler
import Utils
timer = Utils.Timer()


class TemporaryData:
    def __init__(self):
        self.self = self
        self.logging_data = None
        self.event_order = None
        self.special_listener_type = None
        self.bindings = []
        self.macros = []
        self.new_binding = None
        self.settings = [True, True, True, True, True]
        self.killkey_type = int
        self.killkey = None
        self.mouse_movement_buffer = 101
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


temporary_data = TemporaryData()
keyboard_listener = Listener()
mouse_listener = Listener()


# Special Listeners, listens for killkeys and bindings
# Special Mouse
def special_on_move(x, y):
    if temporary_data.special_listener_type == 0:
        mouse_listener.stop_listener()
        temporary_data.killkey = 67
        temporary_data.killkey_type = 3
        Utils.show_messagebox("NewKillkey")

    elif temporary_data.special_listener_type == 1:
        kill_special_listeners()
        temporary_data.new_binding = 67
        Utils.show_messagebox("NewBinding")

    elif 67 in temporary_data.bindings:
        # bindings are active
        print("executing macro")


def special_on_click(x, y, button, pressed):
    if temporary_data.special_listener_type == 0:
        mouse_listener.stop_listener()
        temporary_data.killkey = Utils.special_keys.index(button)
        temporary_data.killkey_type = 2
        Utils.show_messagebox("NewKillkey")

    elif temporary_data.special_listener_type == 1:
        kill_special_listeners()
        temporary_data.new_binding = Utils.special_keys.index(button)
        Utils.show_messagebox("NewBinding")

    elif Utils.special_keys.index(button) in temporary_data.bindings:
        print("executing macro")


def special_on_scroll(x, y, dx, dy):
    if temporary_data.special_listener_type == 0:
        mouse_listener.stop_listener()
        temporary_data.killkey = [dx, dy]
        temporary_data.killkey_type = 4
        Utils.show_messagebox("NewKillkey")

    elif temporary_data.special_listener_type == 1:
        kill_special_listeners()
        temporary_data.new_binding = [dx, dy]
        Utils.show_messagebox("NewBinding")

    elif [dx, dy] in temporary_data.bindings:
        print("executing macro")


# Killkey Keyboard
def special_on_press(key):
    if temporary_data.special_listener_type == 0:
        keyboard_listener.stop_listener()
        temporary_data.killkey = key
        if key in Utils.special_keys:
            temporary_data.killkey_type = 0

        else:
            temporary_data.killkey_type = 1
        Utils.show_messagebox("NewKillkey")

    elif temporary_data.special_listener_type == 1:
        kill_special_listeners()
        if key in Utils.special_keys:
            temporary_data.new_binding = Utils.special_keys.index(key)

        else:
            temporary_data.new_binding = key.char
        Utils.show_messagebox("NewBinding")

    try:
        if key.char in temporary_data.bindings:
            print("dsfsadfadsfasdfasd")
            data = Utils.get_macro_from_file()
            MacroHandler(Utils.Interpreter(data[0], data[1]).sort_for_controller, data[1]).execute_macro()

    except AttributeError:
        print("it got here")
        if Utils.special_keys.index(key) in temporary_data.bindings:
            data = Utils.get_macro_from_file(os.path.abspath(f"Macros/{temporary_data.macros[temporary_data.bindings.index(Utils.special_keys.index(key))]}"))
            print(Utils.Interpreter(data[0], data[1]).sort_for_controller(), data[1])
            MacroHandler(Utils.Interpreter(data[0], data[1]).sort_for_controller(), data[1]).execute_macro()


# Regular Listeners
# Mouse Listeners
def on_move(x, y):
    if temporary_data.killkey == 67:
        kill_listeners()

    elif temporary_data.mouse_movement_i <= temporary_data.mouse_movement_buffer:
        temporary_data.mouse_movement_i += 1

    else:
        temporary_data.mouse_movement_i = 1
        timer.record_event_time([x,y], 0)


def on_click(x, y, button, pressed):
    special_key_index = Utils.special_keys.index(button)
    if special_key_index == temporary_data.killkey:
        kill_listeners()

    elif pressed:
        timer.record_start_time(special_key_index)

    else:
        timer.record_end_time(special_key_index)


def on_scroll(x, y, dx, dy):
    if temporary_data.killkey == [dx, dy]:
        kill_listeners()

    else:
        timer.record_event_time([dx, dy], 1)


# Keyboard Listeners
def on_press(key):
    try:
        if key == temporary_data.killkey:
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


# This function is used to kill both special listeners
def kill_special_listeners():
    keyboard_listener.stop_listener()
    mouse_listener.stop_listener()


# This function is used to kill both macro listeners
def kill_listeners():
    temporary_data.mouse_movement_i = 1
    timer.killkey_force_log(temporary_data.settings)
    temporary_data.logging_data = timer.logging_data
    temporary_data.event_order = timer.event_order
    timer.reset()
    keyboard_listener.stop_listener()
    mouse_listener.stop_listener()
    print("Listeners have been killed.")


settings_dict = {1: [on_move, on_click, on_scroll], 0: [None, None, None]}
