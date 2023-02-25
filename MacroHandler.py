import time
from pynput import mouse, keyboard
from Utils import special_keys


class MacroHandler:
    def __init__(self, data, order):
        self.self = self
        self.thread_pool = []
        self.data = data
        self.last_start_time = 0
        self.order = order
        self.event_index = 0

    def execute_macro(self):
        print(type(self.order),type(self.data))
        for i in range(len(self.order)):
            time.sleep(self.data[i][0] - self.last_start_time)
            self.last_start_time = self.data[i][0]
            if self.order[i] in (0, 1):
                # Anything longer than a .08 is no longer considered a tap.
                if self.data[self.event_index][1] > .08:
                    keyboard_input(self.data[self.event_index][-1], self.order[self.event_index],
                                   self.data[self.event_index][1] * 40)

                else:
                    keyboard_input(self.data[self.event_index][-1], self.order[self.event_index], 1)

            elif self.order[i] == 2:
                mouse_input(self.data[self.event_index][-1], self.data[self.event_index][1])

            else:
                event_input(self.data[self.event_index][-1][0], self.data[self.event_index][-1][1],
                            self.order[self.event_index])

            if i == len(self.order) - 1:
                print("finished")

            self.event_index += 1


# procedurally generate and kill threads to execute this code


def keyboard_input(key, input_type, key_end):
    keyboard_controller = keyboard.Controller()
    if input_type == 0:
        try:
            key_start = 0
            while key_start < key_end:
                time.sleep(0.025)
                keyboard_controller.press(key)
                key_start += 1
            keyboard_controller.release(key)
        except Exception as e:
            print(e)

    else:
        try:
            key_start = 0
            while key_start < key_end:
                time.sleep(0.025)
                keyboard_controller.press(special_keys[key])
                key_start += 1
            keyboard_controller.release(special_keys[key])
        except Exception as e:
            print(e)


def mouse_input(button, duration):
    mouse_controller = mouse.Controller()
    mouse_controller.press(special_keys[button])
    time.sleep(duration)
    mouse_controller.release(special_keys[button])


def event_input(x, y, event_type):
    mouse_controller = mouse.Controller()
    if event_type == 3:
        mouse_controller.move(x, y)

    else:
        mouse_controller.scroll(x, y)

