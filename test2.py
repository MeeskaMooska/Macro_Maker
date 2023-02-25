from pynput import keyboard
import time
x = []
def on_press(key):
    try:
        x.append(time.time())
    except AttributeError:
        print('special key {0} pressed'.format(
            key))

def on_release(key):
    x.append(time.time())
    if key == keyboard.Key.esc:
        # Stop listener
        print(x)
        return False

# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()

# ...or, in a non-blocking fashion:
listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()

fs