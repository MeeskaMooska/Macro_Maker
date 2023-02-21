import tkinter.messagebox
from tkinter import *
from threading import *
from pynput import keyboard, mouse
import time
import Listener
from Utils import Interpreter
import EditorView

# Utility variables (don't want to initialize everytime a function is called)
foreground_dict = {True: "green", False: "red"}


class TempData:
    def __init__(self):
        self.self = self
        self.settings_data = [True, True, True, True, True]
        self.killkey = None
        self.thread_listener = None


# Initializes classes for use
temporary_data = TempData()
editor_view = EditorView.EditorView()


def assign_killkey_pressed():
    Listener.temporary_data.killkey = keyboard.Key.esc
    Listener.temporary_data.killkey_type = 1
    '''if tkinter.messagebox.askyesno("Question.", "Will a mouse entry be your killkey?") == 0:
        Listener.keyboard_listener.listener = keyboard.Listener(on_press=Listener.killkey_on_press, on_release=None)
        Listener.keyboard_listener.listener.start()
    else:
        Listener.mouse_listener.listener = mouse.Listener(on_move=Listener.killkey_on_move,
                                                          on_click=Listener.killkey_on_click,
                                                          on_scroll=Listener.killkey_on_scroll)
        Listener.mouse_listener.listener.start()'''


def start_editor_view():
    if editor_view.running:
        tkinter.messagebox.showwarning("Error.", "An instance of Editor View is already running.")
    else:
        editor_view.logging_data = Interpreter(Listener.temporary_data.logging_data,
                                               Listener.temporary_data.event_order).sort_chronologically_individually()
        editor_view.running = True
        editor_view.setup_gui()


def listen_for_macro():
    while Listener.keyboard_listener.listener is not None or Listener.mouse_listener.listener is not None:
        time.sleep(.5)
    else:
        temporary_data.thread_listener = None
        new_macro_button.config(fg="black", text="New Macro")
        start_editor_view()


def new_macro_pressed():
    if editor_view.running:
        tkinter.messagebox.showwarning("Error.", "Editor View is currently running, please close.")

    elif Listener.keyboard_listener.listener is not None or Listener.mouse_listener.listener is not None:
        tkinter.messagebox.showwarning("Error.", "A macro is already being recorded\n please finish recording before "
                                                 "starting another listener.")

    elif Listener.temporary_data.killkey is None:
        tkinter.messagebox.showwarning("Error.", "There is no assigned killkey.")

    elif temporary_data.settings_data[Listener.temporary_data.killkey_type] is False:
        print(temporary_data.settings_data[Listener.temporary_data.killkey_type])
        print(temporary_data.settings_data)
        print(Listener.temporary_data.killkey_type)
        tkinter.messagebox.showwarning("Error.", "The assigned killkey is muted by your settings\n"
                                                 "please adjust your settings or killkey accordingly.")

    else:
        Listener.mouse_listener.configure_listener(temporary_data.settings_data[2:5])
        Listener.keyboard_listener.configure_listener(temporary_data.settings_data[0:2])
        new_macro_button.config(fg="green", text="Running")
        temporary_data.thread_listener = Thread(target=listen_for_macro)
        temporary_data.thread_listener.start()


# Handles the press of settings buttons
def settings_button_handler(e):
    # Changes setting
    temporary_data.settings_data[e] = not temporary_data.settings_data[e]
    Listener.temporary_data.settings = temporary_data.settings_data
    # Sets color of button to indicate setting
    settings_buttons[e].config(fg=foreground_dict[temporary_data.settings_data[e]])


def on_closing():
    try:
        Listener.mouse_listener.stop_listener()
        Listener.keyboard_listener.stop_listener()
        temporary_data.thread_listener = None
        root.destroy()
    except (NameError, AttributeError):
        root.destroy()


"""<<<<<--- Start of GUI code directly below, don't place functions that will be called by GUI below --->>>>>"""
# Initializes root
root = Tk()
root.title("Macro Maker")
root.resizable(False, False)

# Initializes all of the elements
new_macro_button = Button(root, text="New Macro", command=new_macro_pressed)
assign_killkey_button = Button(root, text="Assign Killkey", command=assign_killkey_pressed)
delete_selected_button = Button(root, text="Delete Selected")
edit_selected_button = Button(root, text="Edit Selected")
macro_listbox = Listbox(root)

# Settings buttons/frame
settings_buttons_frame = LabelFrame(root, borderwidth=0, highlightthickness=0)
settings_button_0 = Button(settings_buttons_frame, text="Listening For Regular Keys",
                           command=lambda: settings_button_handler(0), fg="green")
settings_button_1 = Button(settings_buttons_frame, text="Listening For Special Keys",
                           command=lambda: settings_button_handler(1), fg="green")
settings_button_2 = Button(settings_buttons_frame, text="Listening For Mouse Clicks",
                           command=lambda: settings_button_handler(2), fg="green")
settings_button_3 = Button(settings_buttons_frame, text="Listening For Mouse Movement",
                           command=lambda: settings_button_handler(3), fg="green")
settings_button_4 = Button(settings_buttons_frame, text="Listening For Mouse Scrolls",
                           command=lambda: settings_button_handler(4), fg="green")
settings_buttons = {0: settings_button_0, 1: settings_button_1,
                    2: settings_button_2, 3: settings_button_3, 4: settings_button_4}
# Places all elements onto the GUI
# Top Buttons
new_macro_button.grid(row=0, column=0, columnspan=1, padx=(10, 5), pady=(10, 0))
assign_killkey_button.grid(row=0, column=1, columnspan=1, padx=(5, 5), pady=(10, 0))
delete_selected_button.grid(row=0, column=2, columnspan=1, padx=(5, 5), pady=(10, 0))
edit_selected_button.grid(row=0, column=3, columnspan=1, padx=(5, 10), pady=(10, 0))

# Listbox
macro_listbox.grid(row=1, column=0, columnspan=2, pady=10)

# Settings buttons container
settings_buttons_frame.grid(row=1, column=2, columnspan=2)
settings_button_0.grid(row=0, column=0)
settings_button_1.grid(row=1, column=0)
settings_button_2.grid(row=2, column=0)
settings_button_3.grid(row=3, column=0)
settings_button_4.grid(row=4, column=0)

# Calls root mainloop function
root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
