from multiprocessing import *
from tkinter import *

import keyboard
import pyautogui as pag
import winsound
import time
from pynput import keyboard
from pynput import mouse


'''def on_click(x, y, button, pressed):
    print('{0} at {1}'.format('Pressed' if pressed else 'Released', (x, y)))
'''


# Starts the keyboard/mouse listener


# starts the GUI
root = Tk()
button = Button(root, text="+", command=main.test)
button.pack()
root.mainloop()

#listener.stop()
keyListener.join()
mouseListener.join()

