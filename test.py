from tkinter import *
import test2
import threading
import time

class TemporaryData:
    def __init__(self):
        self.self = self
        self.thread_listener = None

temporary_data = TemporaryData()
test_data = [[0, 1, 2, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14], [15, 16, 17, 18, 19],
                           [20, 21, 22, 23, 24]]
editor_view = test2.EditorView()


def editor_view_listener():
    print("sdf")
    while editor_view.running == True:
        time.sleep(1)
        print(editor_view.running)
    else:
        print(editor_view.running)


def start_new_gui():
    if editor_view.running:
        print("there is already an instance of editor view running, close that before continuing.")
    else:
        editor_view.logging_data = test_data
        editor_view.running = True
        temporary_data.thread_listener = threading.Thread(target=editor_view_listener)
        temporary_data.thread_listener.start()
        editor_view.setup_gui()



root = Tk()

open_nw_button = Button(root, text="open new window", command=start_new_gui)
open_nw_button.pack()

root.mainloop()