import threading
import time
import json
from pynput.keyboard import Key
from pynput.mouse import Button


special_keys = [Button.left, Button.right, Button.middle, Button.x1, Button.x2, Key.space, Key.esc, Key.alt, Key.alt_l,
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


class Reader:
    def __init__(self):
        self.self = self


class Logger:
    def __init__(self):
        self.self = self

    def convert_data_to_JSON(self):
        pass




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
            self.logging_data[0].append([self.start_times[index], duration, key])
        elif key > 4:
            self.logging_data[1].append([self.start_times[index], duration, key])
        else:
            self.logging_data[2].append([self.start_times[index], duration, key])
        self.active_keys.pop(index)
        self.start_times.pop(index)

    # This records singular events such as scrolls and movements.
    def record_event_time(self, event, event_type):
        if event_type == 0:
            self.event_order.append(3)
            self.logging_data[3].append([time.time(), event])
        else:
            self.event_order.append(4)
            self.logging_data[4].append([time.time(), event])

    def killkey_force_log(self, settings):
        end_time = time.time()
        for key in self.active_keys:
            index = self.active_keys.index(key)
            duration = end_time - self.start_times[index]
            if type(key) == str:
                self.logging_data[0].append([self.start_times[index], duration, key])
            elif key > 4:
                self.logging_data[1].append([self.start_times[index], duration, key])
            else:
                self.logging_data[2].append([self.start_times[index], duration, key])
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

    def sort_for_editor(self):
        pass

    def sort_for_file(self):
        pass

    def sort_for_controller(self):
        order_index = [0, 0, 0, 0, 0]
        chronological_data = []

        self.sort_chronologically_individually()

        for count, arr in enumerate(self.event_order):
            chronological_data.append(self.data[self.event_order[count]][order_index[self.event_order[count]]])
            order_index[self.event_order[count]] += 1


