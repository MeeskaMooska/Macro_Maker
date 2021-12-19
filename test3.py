# Known issues
#  #1: we cant record things like ctrl + x yet so that fucking sucks. if you read this and you have any idea
#   Lemme know - Discord: Meeska#1311;

import time
from tkinter import *
from pynput import mouse
from pynput.keyboard import Key, Listener
# I really did try to find a better way to do the shit that's below, maybe im stupid maybe im not if theres a better way
# pls lemme know
special_keys = [Key.space, Key.esc, Key.alt, Key.alt_l, Key.alt_r,
                Key.alt_gr, Key.backspace, Key.caps_lock, Key.cmd, Key.cmd_l,
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


# Logging stuff
class MacroLogger:
    def __init__(self):
        self.keys_pressed = []
        self.file = open("test.txt", 'a')  # this will need work eventually(moved)

    def log_key(self, key):
        self.keys_pressed.append(key)

    def write_to_file(self):
        # below checks if self.keys_pressed == []
        if not self.keys_pressed:
            print("here 1")
            return False
        else:
            print("here 2")
            times = macroTimer.times
            i = 0
            length = len(self.keys_pressed)
            while i < length:
                # TODO optimize below
                # this can and will be optimized eventually however that is not my main goal rn.
                # ik its bad im not getting payed for it
                if i != 0 and i != length-1:
                    try:
                        self.file.write(f":{special_keys.index(self.keys_pressed[i])}/{times[i]}/")
                    except (AttributeError, ValueError):
                        self.file.write(f"{self.keys_pressed[i]}/{times[i]}/")
                elif i == 0:
                    try:
                        self.file.write(f"_[:{special_keys.index(self.keys_pressed[i])}/{times[i]}/")
                    except (AttributeError, ValueError):
                        self.file.write(f"_[{self.keys_pressed[i]}/{times[i]}/")
                elif i == length-1:
                    try:
                        self.file.write(f":{special_keys.index(self.keys_pressed[i])}/{times[i]}]")
                    except (AttributeError, ValueError):
                        self.file.write(f"{self.keys_pressed[i]}/{times[i]}]")
                i += 1


class MacroTimer:
    def __init__(self):
        self.active_keys = [] # can have special keys too
        self.times = []
        self.start_times = []
        self.end_time = 0.0

    def start_timer(self):
        self.start_times.append(time.time())

    def stop_timer(self, index):
        self.end_time = time.time()
        self.times.append(self.end_time - self.start_times[index])
        self.start_times.pop(index)


def on_press(key):
    print(key)
    try:
        if key.char not in macroTimer.active_keys:
            macroLogger.log_key(key.char)
            macroTimer.active_keys.append(key.char)
            macroTimer.start_timer()
    except AttributeError:
        if key == Key.esc:
            macroLogger.write_to_file()
            return False

        elif key not in macroTimer.active_keys:
            macroLogger.log_key(key)
            macroTimer.active_keys.append(key)
            macroTimer.start_timer()


def on_release(key):
    try:
        if key.char in macroTimer.active_keys:
            macroTimer.stop_timer(macroTimer.active_keys.index(key.char))
            macroTimer.active_keys.remove(key.char)
    except AttributeError:
        if key in macroTimer.active_keys:
            macroTimer.stop_timer(macroTimer.active_keys.index(key))
            macroTimer.active_keys.remove(key)


macroLogger = MacroLogger()
macroTimer = MacroTimer()
keyListener = Listener(on_press=on_press, on_release=on_release)
#mouseListener = mouse.Listener(on_click=on_click)
keyListener.start()
#mouseListener.start()

# GUI stuff
root = Tk()
button = Button(root, text="+")
button.pack()
root.mainloop()

keyListener.join()
#mouseListener.join()

# Reading/Executing stuff
