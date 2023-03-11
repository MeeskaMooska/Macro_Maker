import tkinter.messagebox
from tkinter import *
from threading import *
from pynput import keyboard, mouse
import time
import Listener
import os
import Utils
import EditorView

# Utility variables (don't want to initialize everytime a function is called)
foreground_dict = {True: "green", False: "red"}


class TempData:
    def __init__(self):
        self.self = self
        self.macros = []
        self.bindings = []
        self.settings_data = [True, True, True, True, True]
        self.killkey = None
        self.thread_listener = None

    def mouse_settings(self):
        return self.settings_data[2:5]

    def keyboard_settings(self):
        return self.settings_data[0:2]


# Initializes classes for use
temporary_data = TempData()
editor_view = EditorView.EditorView()


# Special input refers to Bindings and Killkeys
def record_special_input_pressed(special_type):
    # Prevents the listener from running while the editor view is running.
    if editor_view.running:
        Utils.show_messagebox("EditorViewRunning")

    # Prevents the listener from running while any other listener is running.
    elif Listener.keyboard_listener.listener is None and Listener.mouse_listener.listener is None:
        Listener.temporary_data.special_listener_type = special_type
        if special_type in (0, 1):
            if tkinter.messagebox.askyesno("Question.", "Will a mouse entry be your killkey?") == 0:
                Listener.keyboard_listener.listener = keyboard.Listener(on_press=Listener.special_on_press,
                                                                        on_release=None)
                Listener.keyboard_listener.listener.start()

            else:
                Listener.mouse_listener.listener = mouse.Listener(on_move=Listener.special_on_move,
                                                                  on_click=Listener.special_on_click,
                                                                  on_scroll=Listener.special_on_scroll)
                Listener.mouse_listener.listener.start()

        else:
            activate_bindings_button.config(text="Deactivate Bindings")
            Listener.temporary_data.macros = temporary_data.macros
            Listener.temporary_data.bindings.clear()
            for file in temporary_data.macros:
                Listener.temporary_data.bindings.append(Utils.get_binding_from_file(os.path.abspath(f"Macros/{file}")))
            print(Listener.temporary_data.bindings)
            Listener.keyboard_listener.listener = keyboard.Listener(on_press=Listener.special_on_press, on_release=None)
            Listener.mouse_listener.listener = mouse.Listener(on_move=Listener.special_on_move,
                                                              on_click=Listener.special_on_click,
                                                              on_scroll=Listener.special_on_scroll)
            Listener.keyboard_listener.listener.start()
            Listener.mouse_listener.listener.start()

    # If another listener was running we alert the user.
    else:
        if Listener.temporary_data.special_listener_type == 2:
            Listener.temporary_data.special_listener_type = None
            Listener.mouse_listener.stop_listener()
            Listener.keyboard_listener.stop_listener()
            activate_bindings_button.config(text = "Activate Bindings")

        else:
            Utils.show_messagebox("ListenerAlreadyRunning")


def start_editor_view(from_button_press):
    # Prevents multiple instances of the editor view from running.
    if editor_view.running:
        Utils.show_messagebox("EditorViewRunning")

    # Runs when the edit button is pressed.
    elif from_button_press:
        try:
            # here well pass temp data established on the start of the program
            data = Utils.get_macro_from_file(f"Macros/{temporary_data.macros[macro_listbox.curselection()[0]]}")
            editor_view.logging_data = Utils.Interpreter(data[0], data[1]).sort_chronologically_individually()
            editor_view.event_order = data[1]
            editor_view.running = True
            editor_view.setup_gui()
            temporary_data.thread_listener = Thread(target=listen_for_editor_view)
            temporary_data.thread_listener.start()

        except IndexError:
            Utils.show_messagebox("NoSelectedListItem")

    # Runs when the macro listener is broken using a killkey.
    else:
        editor_view.logging_data = Utils.Interpreter(Listener.temporary_data.logging_data,
                                                     Listener.temporary_data.event_order).sort_chronologically_individually()
        editor_view.event_order = Listener.temporary_data.event_order
        editor_view.running = True
        editor_view.setup_gui()
        temporary_data.thread_listener = Thread(target=listen_for_editor_view)
        temporary_data.thread_listener.start()


def listen_for_editor_view():
    while editor_view.running:
        time.sleep(.5)
        print("running")

    else:
        print("editor view killed")
        temporary_data.thread_listener = None
        config_macro_listbox()


def listen_for_macro():
    while Listener.keyboard_listener.listener is not None or Listener.mouse_listener.listener is not None:
        time.sleep(.5)

    else:
        print(Listener.temporary_data.logging_data)
        temporary_data.thread_listener = None
        new_macro_button.config(fg="black", text="New Macro")
        # Checks if the macro has any data
        if any(Listener.temporary_data.logging_data):
            start_editor_view(False)

        # Macro had no data
        else:
            Utils.show_messagebox("NoMacroRecorded")


# Called when the new macro button is pressed
def new_macro_pressed():
    # Prevents the macro listener from running while the editor view is running.
    if editor_view.running:
        Utils.show_messagebox("EditorViewRunning")

    # Prevents multiple macro listeners from running.
    elif Listener.keyboard_listener.listener is not None or Listener.mouse_listener.listener is not None:
        Utils.show_messagebox("ListenerAlreadyRunning")

    # Prevents the macro listener from running without a killkey.
    elif Listener.temporary_data.killkey is None:
        Utils.show_messagebox("NoKillkey")

    # Prevents the macro listener from running with a settings configuration that mutes the killkey.
    elif temporary_data.settings_data[Listener.temporary_data.killkey_type] is False:
        Utils.show_messagebox("MutedKillkey")

    # Listener conditions were met.
    else:
        # Starts the mouse and keyboard listeners.
        Listener.mouse_listener.configure_listener(temporary_data.mouse_settings())
        Listener.keyboard_listener.configure_listener(temporary_data.keyboard_settings())

        # Configures new macro button to represent the current state of the listener
        new_macro_button.config(fg="green", text="Running")

        # Starts thread that waits for the macro listener to finish
        temporary_data.thread_listener = Thread(target=listen_for_macro)
        temporary_data.thread_listener.start()


# Handles the press of settings buttons.
def settings_button_handler(e):
    # Changes setting.
    temporary_data.settings_data[e] = not temporary_data.settings_data[e]
    Listener.temporary_data.settings = temporary_data.settings_data

    # Sets color of button to indicate setting.
    settings_buttons[e].config(fg=foreground_dict[temporary_data.settings_data[e]])


# Called on program start and on editor view close.
def config_macro_listbox():
    # Clears the listbox to prevent duplicates(Not graceful but works).
    macro_listbox.delete(0, END)

    # Loops through the absolute path of the macros directory.
    for file in os.listdir(os.path.abspath("Macros")):
        # Configures macros list, bindings list, and the listbox.
        temporary_data.macros.append(file)
        temporary_data.bindings.append(Utils.get_binding_from_file(os.path.abspath(f"Macros/{file}")))
        macro_listbox.insert(END, os.path.splitext(file)[0])


def delete_button_pressed():
    if macro_listbox.curselection() == ():
        Utils.show_messagebox("NoSelectedMacro")

    else:
        os.remove(os.path.abspath(f"Macros/{temporary_data.macros[macro_listbox.curselection()[0]]}"))
        temporary_data.macros.pop(macro_listbox.curselection()[0])
        macro_listbox.delete(macro_listbox.curselection()[0])


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
new_macro_button = Button(root, text="New Macro", command=new_macro_pressed, width="12", borderwidth=1)
assign_killkey_button = Button(root, text="Assign Killkey", command=lambda: record_special_input_pressed(0),
                               width="12", borderwidth=1)
delete_selected_button = Button(root, text="Delete", command=delete_button_pressed, width="12", borderwidth=1)
edit_selected_button = Button(root, text="Edit", command=lambda: start_editor_view(True), width="12", borderwidth=1)
macro_listbox = Listbox(root)
config_macro_listbox()

# Settings buttons/frame
settings_buttons_frame = LabelFrame(root, borderwidth=0, highlightthickness=0)
settings_button_0 = Button(settings_buttons_frame, text="Listening For Regular Keys",
                           command=lambda: settings_button_handler(0), fg="green", borderwidth=1, width=25)
settings_button_1 = Button(settings_buttons_frame, text="Listening For Special Keys",
                           command=lambda: settings_button_handler(1), fg="green", borderwidth=1, width=25)
settings_button_2 = Button(settings_buttons_frame, text="Listening For Mouse Clicks",
                           command=lambda: settings_button_handler(2), fg="green", borderwidth=1, width=25)
settings_button_3 = Button(settings_buttons_frame, text="Listening For Mouse Movement",
                           command=lambda: settings_button_handler(3), fg="green", borderwidth=1, width=25)
settings_button_4 = Button(settings_buttons_frame, text="Listening For Mouse Scrolls",
                           command=lambda: settings_button_handler(4), fg="green", borderwidth=1, width=25)
settings_buttons = {0: settings_button_0, 1: settings_button_1,
                    2: settings_button_2, 3: settings_button_3, 4: settings_button_4}

# Binding buttons
activate_bindings_button = Button(root, text="Activate Bindings", command=lambda: record_special_input_pressed(2),
                                  width="16", borderwidth=1)

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
settings_button_0.grid(row=0, column=0, pady=(0, 8))
settings_button_1.grid(row=1, column=0, pady=(0, 8))
settings_button_2.grid(row=2, column=0, pady=(0, 8))
settings_button_3.grid(row=3, column=0, pady=(0, 8))
settings_button_4.grid(row=4, column=0)

# Binding Button
activate_bindings_button.grid(row=2, column=0, columnspan=2, padx=(5, 5), pady=(0, 10))

# Calls root mainloop function
root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
