from tkinter import *
from pynput.keyboard import Key, Listener

def on_press(key):
    print("s")

def on_release(key):
    print("d")


keyListener = Listener(on_press=on_press, on_release=on_release)


root = Tk()
button = Button(root, text="+")
button.pack()
root.mainloop()

keyListener.start()
'''def fingers_crossed():
    keyListener.join()

fingers_crossed()'''