from tkinter import *
from tkinter import messagebox
import threading
import pynput.keyboard
import pynput.mouse
from pynput.keyboard import Key
import time
from functools import partial

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

    def log_key(self, method, key):
        if method == 0:
            self.keys_pressed.append(key)
        else:
            self.keys_pressed.append(f":{special_keys.index(key)}")

    def write_to_file(self):
        # below checks if self.keys_pressed == []
        file = open("test.txt", 'a')
        if not self.keys_pressed:
            return False
        else:
            times = MACRO_TIMER.times
            i = 0
            length = len(self.keys_pressed)
            if length == 1:
                file.write(f"_[{self.keys_pressed[i]}/{times[i]}]")
            else:
                while i < length:
                    # TODO optimize below
                    # this can and will be optimized eventually however that is not my main goal rn.
                    # ik its bad im not getting payed for it
                    if i != 0 and i != length - 1:
                        file.write(f"{self.keys_pressed[i]}/{times[i]}/")
                    elif i == 0:
                        file.write(f"_[{self.keys_pressed[i]}/{times[i]}/")
                    elif i == length - 1:
                        file.write(f"{self.keys_pressed[i]}/{times[i]}]")
                    i += 1
        MACRO_LOGGER.keys_pressed = []


# Timing stuff
class MacroTimer:
    def __init__(self):
        self.active_keys = []  # can have special keys too
        self.times = []
        self.start_times = []
        self.end_time = 0.0

    def start_timer(self):
        self.start_times.append(time.time())

    def stop_timer(self, index):
        self.end_time = time.time()
        self.times.append(self.end_time - self.start_times[index])
        self.start_times.pop(index)


# GUI stuff
class App(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.listener_running = False
        self.root = None
        self.label = None
        self.assign_killkey_button = None
        self.start_listener_button = None
        self.mouse_setting_button0 = None
        self.mouse_setting_button1 = None
        self.mouse_setting_button2 = None
        self.start()

    def callback(self):
        self.root.quit()

    def run(self):
        self.root = Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        # Mouse settings frame stuff
        mouse_settings_frame = Frame(self.root)
        mouse_settings_frame.pack(side=RIGHT)
        self.mouse_setting_button0 = Button(mouse_settings_frame, text="listening for mouse movement",
                                            command=partial(self.update_mouse_settings, 0), fg="green")
        self.mouse_setting_button1 = Button(mouse_settings_frame, text="listening for mouse clicks",
                                            command=partial(self.update_mouse_settings, 1), fg="green")
        self.mouse_setting_button2 = Button(mouse_settings_frame, text="listening for mouse scrolls",
                                            command=partial(self.update_mouse_settings, 2), fg="green")
        self.mouse_setting_button0.pack(side=TOP)
        self.mouse_setting_button1.pack(side=TOP)
        self.mouse_setting_button2.pack(side=TOP)
        # Main controls
        self.label = Label(self.root, text="there is no killkey", fg="red")
        self.label.pack()
        self.assign_killkey_button = Button(self.root, text="assign killkey",
                                            command=self.assign_killkey)
        self.assign_killkey_button.pack()
        self.start_listener_button = Button(self.root, text="start recording",
                                            command=self.start_listener_button_pressed)
        self.start_listener_button.pack()
        self.root.mainloop()

    def update_mouse_settings(self, index):
        MOUSE.method[index] = not MOUSE.method[index]
        print(MOUSE.method)
        fg_dict = {0: "red", 1: "green"}
        self.mouse_setting_button0.config(fg=fg_dict[MOUSE.method[0]])
        self.mouse_setting_button1.config(fg=fg_dict[MOUSE.method[1]])
        self.mouse_setting_button2.config(fg=fg_dict[MOUSE.method[2]])

    def update_label(self):
        if KEYBOARD.killkey is None:
            if self.listener_running:
                self.label.config(text="listening for killkey", fg="black")
            else:
                self.label.config(text="there is no killkey", fg="red")
        else:
            self.label.config(text=f"the killkey is {KEYBOARD.killkey}", fg="green")

    def update_button(self):
        if self.listener_running:
            self.start_listener_button.config(text="recording")
        else:
            self.start_listener_button.config(text="start recording")

    def start_listener_button_pressed(self):
        # if listener is not running
        if not self.listener_running:
            if KEYBOARD.killkey is None:
                messagebox.showerror(title="Error", message="you must assign a killkey.")
            else:
                self.listener_running = True
                self.update_button()
                Connector(1)
                Connector(0)
        else:
            self.listener_running = False
            self.update_button()
            MOUSE.mouse_listener.stop()
            KEYBOARD.keyboard_listener.stop()
            MACRO_LOGGER.write_to_file()

    def assign_killkey(self):
        # if listener is not running
        if not self.listener_running:
            self.listener_running = True
            self.update_button()
            KEYBOARD.last_killkey = KEYBOARD.killkey
            KEYBOARD.killkey = None
            self.update_label()
            Connector(4)
        else:
            if KEYBOARD.killkey is None:
                KEYBOARD.killkey = KEYBOARD.last_killkey
                self.listener_running = False
                self.update_button()
                self.update_label()
                KEYBOARD.keyboard_listener.stop()
            else:
                self.listener_running = False
                self.update_button()
                KEYBOARD.keyboard_listener.stop()


app = App()


# single use thread probable not the best way but it works ;)
class Connector(threading.Thread):
    def __init__(self, method):
        threading.Thread.__init__(self)
        self.method = method
        self.start()

    def run(self):
        if self.method == 0:
            KEYBOARD.create_listener()
        elif self.method == 1:
            MOUSE.run()
        elif self.method == 2:
            app.update_label()
        elif self.method == 3:
            app.listener_running = False
            app.update_button()
        elif self.method == 4:
            KEYBOARD.create_killkey_listener()
        return False


class Keyboard(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.killkey = None
        self.last_killkey = None
        self.keyboard_listener = None

    def create_listener(self):
        self.keyboard_listener = pynput.keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.start_listener()

    def create_killkey_listener(self):
        self.keyboard_listener = pynput.keyboard.Listener(on_press=self.on_press_killkey)
        self.start_listener()

    def start_listener(self):
        self.keyboard_listener.start()
        self.keyboard_listener.join()

    def on_press(self, key):
        try:
            if key == self.killkey:
                MACRO_LOGGER.write_to_file()
                Connector(3)
                MOUSE.mouse_listener.stop()
                self.keyboard_listener.stop()

            elif key.char not in MACRO_TIMER.active_keys:
                MACRO_LOGGER.log_key(0, key.char)
                MACRO_TIMER.active_keys.append(key.char)
                MACRO_TIMER.start_timer()

        except AttributeError:
            if key == self.killkey:
                MACRO_LOGGER.write_to_file()
                Connector(3)
                MOUSE.mouse_listener.stop()
                self.keyboard_listener.stop()

            elif key not in MACRO_TIMER.active_keys:
                MACRO_LOGGER.log_key(1, key)
                MACRO_TIMER.active_keys.append(key)
                MACRO_TIMER.start_timer()

    @staticmethod
    def on_release(key):
        try:
            if key.char in MACRO_TIMER.active_keys:
                MACRO_TIMER.stop_timer(MACRO_TIMER.active_keys.index(key.char))
                MACRO_TIMER.active_keys.remove(key.char)
        except AttributeError:
            if key in MACRO_TIMER.active_keys:
                MACRO_TIMER.stop_timer(MACRO_TIMER.active_keys.index(key))
                MACRO_TIMER.active_keys.remove(key)

    def on_press_killkey(self, key):
        self.killkey_set = True
        self.killkey = key
        self.keyboard_listener.stop()
        Connector(2)
        Connector(3)


class Mouse(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.mouse_listener = None
        self.method = [True, True, True]  # default listener method with all on

    def run(self):
        self.create_listener()
        self.start_listener()

    def create_listener(self):
        mouse_input_list = [[None, None, None], [self.on_move, self.on_click, self.on_scroll]]
        self.mouse_listener = pynput.mouse.Listener(on_move=mouse_input_list[int(self.method[0])][0],
                                                    on_click=mouse_input_list[int(self.method[1])][1],
                                                    on_scroll=mouse_input_list[int(self.method[2])][2])

    def start_listener(self):
        self.mouse_listener.start()
        self.mouse_listener.join()

    def on_move(self, x, y):
        print(f"mouse moved to:{x}, {y}")

    def on_click(self, x, y, button, pressed):
        print(f"the {button} was clicked at {x}, {y} pressed:{pressed}")

    def on_scroll(self, x, y, dx, dy):
        print(f"mouse scrolled to {x}, {y}, {dx}, {dy}")


MACRO_LOGGER = MacroLogger()
MACRO_TIMER = MacroTimer()
KEYBOARD = Keyboard()
MOUSE = Mouse()
