import threading
import time
import json
import os.path
import tkinter.messagebox
from tkinter import messagebox
from pynput.keyboard import Key
from pynput.mouse import Button

special_keys = [Button.left, Button.right, Button.middle, Button.x1, Button.x2,
                Key.space, Key.esc, Key.alt, Key.alt_l,
                Key.alt_r, Key.alt_gr, Key.backspace, Key.caps_lock, Key.cmd, Key.cmd_l,
                Key.cmd_r, Key.ctrl, Key.ctrl_l, Key.ctrl_r, Key.delete,
                Key.down, Key.end, Key.enter, Key.esc, Key.f1,
                Key.f2, Key.f3, Key.f4, Key.f5, Key.f6,
                Key.f7, Key.f8, Key.f9, Key.f10, Key.f11,
                Key.f12, Key.f13, Key.f14, Key.f15, Key.f16,
                Key.f17, Key.f18, Key.f19, Key.f20, Key.home,
                Key.left, Key.page_down, Key.page_up, Key.right, Key.shift,
                Key.shift_l, Key.shift_r, Key.space, Key.tab, Key.up,
                Key.media_play_pause, Key.media_volume_mute, Key.media_volume_down, Key.media_volume_up,
                Key.media_previous, Key.media_next, Key.insert, Key.menu, Key.num_lock, Key.pause,
                Key.print_screen, Key.scroll_lock]


def log_data_to_file(macro_name, data):
    path = f"Macros/{macro_name}.json"
    data = json.dumps(data, separators=(',', ':'), indent=5)
    if os.path.exists(path):
        open(f"Macros/{macro_name}.json", "w").write(data)

    else:
        open(f"Macros/{macro_name}.json", "x")
        open(f"Macros/{macro_name}.json", "w").write(data)


def get_macro_from_file(path):
    data = json.loads(open(path, 'r').read())
    macro = [data['regular_keys'], data['special_keys'], data['mouse_clicks'],
             data['mouse_moves'], data['mouse_scrolls']]
    event_order = data['event_order']
    binding = data['binding']
    return [macro, event_order, binding]


def get_binding_from_file(path):
    with open(path, 'r') as f:
        data = json.load(f)
        return data['binding']


# Designed to find the x occurrence of a value in the event order list
def find_x_occurrence(value, x, event_order):
    count = 0
    # Enumerates through event_order
    for index, item in enumerate(event_order):
        # Evaluates value of item
        if item == value:
            count += 1
            if count == x:
                event_order.pop(index)
    return event_order


def show_messagebox(message):
    if message == "ListenerAlreadyRunning":
        tkinter.messagebox.showerror("Error.",
                                     "A macro is already being recorded\n please finish recording before "
                                     "starting another listener.")

    elif message == "EditorViewRunning":
        tkinter.messagebox.showerror("Error.", "Editor View is currently running, please close.")

    elif message == "NewKillkey":
        tkinter.messagebox.showinfo("New Killkey.", "Your killkey has been assigned successfully.")
    elif message == "NewBinding":
        tkinter.messagebox.showinfo("New Binding.", "Your binding has been assigned successfully.")

    elif message == "NoKillkey":
        tkinter.messagebox.showerror("Error.", "There is no assigned killkey.")

    elif message == "MutedKillkey":
        tkinter.messagebox.showerror("Error.", "The assigned killkey is muted by your settings\n"
                                               "please adjust your settings or killkey accordingly.")

    elif message == "NoSelectedMacro":
        tkinter.messagebox.showerror("Error.", "You must select a macro before deleting.")

    elif message == "NoSelectedListItem":
        tkinter.messagebox.showerror("Error.", "You must select a macro before you can edit.")

    elif message == "NoMacroRecorded":
        tkinter.messagebox.showerror("Error.", "No macro was recorded.")


class Timer:
    def __init__(self):
        self.active_keys = []
        self.start_times = []
        self.event_order = []
        # regular key, special key, click, move, scroll
        self.logging_data = [[], [], [], [], []]

    def record_start_time(self, key):
        self.active_keys.append(key)
        self.start_times.append(time.time())
        if type(key) == str:
            self.event_order.append(0)
        elif key > 4:
            self.event_order.append(1)
        else:
            self.event_order.append(2)

    def record_end_time(self, key):
        index = self.active_keys.index(key)
        duration = time.time() - self.start_times[index]
        if type(key) == str:
            self.logging_data[0].append([round(self.start_times[index], 3), round(duration, 3), key])
        elif key > 4:
            self.logging_data[1].append([round(self.start_times[index], 3), round(duration, 3), key])
        else:
            self.logging_data[2].append([round(self.start_times[index], 3), round(duration, 3), key])
        self.active_keys.pop(index)
        self.start_times.pop(index)

    # This records singular events such as scrolls and movements.
    def record_event_time(self, event, event_type):
        if event_type == 0:
            self.event_order.append(3)
            self.logging_data[3].append([round(time.time(), 3), event])
        else:
            self.event_order.append(4)
            self.logging_data[4].append([round(time.time(), 3), event])

    def killkey_force_log(self, settings):
        end_time = time.time()
        for key in self.active_keys:
            index = self.active_keys.index(key)
            duration = end_time - self.start_times[index]
            if type(key) == str:
                self.logging_data[0].append([round(self.start_times[index], 3), round(duration, 3), key])
            elif key > 4:
                self.logging_data[1].append([round(self.start_times[index], 3), round(duration, 3), key])
            else:
                self.logging_data[2].append([round(self.start_times[index], 3), round(duration, 3), key])

        if not settings[0]:
            self.logging_data[0].clear()
            self.event_order = list(filter((0).__ne__, self.event_order))
        if not settings[1]:
            self.logging_data[1].clear()
            self.event_order = list(filter((1).__ne__, self.event_order))

    def reset(self):
        self.active_keys = []
        self.start_times = []
        self.logging_data = [[], [], [], [], []]
        self.event_order = []


# Todo change this stuff up, its doesnt need to be done this way.
class Interpreter:
    def __init__(self, data, event_order):
        self.self = self
        self.data = data
        self.event_order = event_order
        self.sorted_list = []

    def sort_chronologically_individually(self):
        self.data[0] = sorted(self.data[0], key=lambda x: x[0])
        self.data[1] = sorted(self.data[1], key=lambda x: x[0])
        self.data[2] = sorted(self.data[2], key=lambda x: x[0])
        return self.data

    def sort_for_controller(self):
        order_index = [0, 0, 0, 0, 0]
        chronological_data = []

        self.sort_chronologically_individually()

        for count, arr in enumerate(self.event_order):
            chronological_data.append(self.data[self.event_order[count]][order_index[self.event_order[count]]])
            order_index[self.event_order[count]] += 1

        start_time = chronological_data[0][0]
        for count, arr in enumerate(chronological_data):
            arr[0] = round(arr[0] - start_time, 3)

        return chronological_data
