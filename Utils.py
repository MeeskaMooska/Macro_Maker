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
        # regular key, special key, click, move, scroll
        self.logging_data = [[], [], [], [], [], []]

    def record_start_time(self, key):
        self.active_keys.append(key)
        self.start_times.append(time.time())
        if type(key) == str:
            self.logging_data[5].append(0)
        elif key > 4:
            self.logging_data[5].append(1)
        else:
            self.logging_data[5].append(2)

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
            self.logging_data[5].append(3)
            self.logging_data[3].append([time.time(), event])
        else:
            self.logging_data[5].append(4)
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
            self.logging_data[5] = list(filter((0).__ne__, self.logging_data[5]))
        if not settings[1]:
            self.logging_data[1].clear()
            self.logging_data[5] = list(filter((1).__ne__, self.logging_data[5]))
        print(self.logging_data)

    def reset(self):
        self.active_keys = []
        self.start_times = []
        self.logging_data = [[], [], [], [], [], []]


class Interpreter:
    '''
    % is the time identifier
    : is special key identifier
    / is regular key identifier
    | is untimed key identifier
    $ is macro name identifier ex. _[$macro name$ if index -1 == [ is_name = True; else is_name = False
    '''
    def __init__(self):
        self.name_builder = ""
        self.is_name = False

    def file_data(self):
        file = open("test.txt", "r")
        content = file.readlines()

        i = 0
        while i < len(content):
            for byte in content[i]:
                if byte == '$':
                    self.is_name = not self.is_name
                    byte += 1
                if self.is_name is True:
                    print(byte)
                    self.name_builder = self.name_builder + byte
            i += 1
        print(self.name_builder)

    def raw_data(self):
        print("the intepreter is starting")