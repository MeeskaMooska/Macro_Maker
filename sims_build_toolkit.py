import winsound as ws
import pyautogui as pag
import os


def nearest_even(room_dimensions):
    return round(float(room_dimensions) / 2) * 2


def yes_no_question(question):
    print(question)
    valid = {"Y": True, "YE": True, "YES": True, "N": False, "NO": False}
    answer = input("Y / N: ").upper()
    if answer in valid:
        if valid[answer] is True:
            return True

        else:
            return False

    else:
        print("You have entered an invalid input, please try again.")
        return yes_no_question(question)


def get_mouse_location(method):
    methods = {0: pag.position()[0], 1: pag.position()[1], 2: pag.position()}
    return methods[method]


def play_sound():
    ws.PlaySound("sound_1.wav", ws.SND_FILENAME)


def paint():
    pag.click(808, 1052)
    pag.moveTo(938, 486)
    distance = 200
    while distance > 0:
        pag.drag(distance, 0, duration=0)
        distance -= 5
        pag.drag(0, distance, duration=0)
        distance -= 5
        pag.drag(-distance, 0, duration=0)
        distance -= 5
        pag.drag(0, -distance, duration=0)
        distance -= 5


def format_data(data):
    # todo we need to get each item of data and the max_char and send it to pad_data
    #  needed
    #   max_char - check
    #   pad_data
    formatted_data = [""]
    max_char = len(str(max(data[0])))
    i = 0
    while i < len(data):
        if type(data[i]) == list:
            x = 0
            while x < len(data[i]):
                formatted_data[0] += (pad_data([str(data[i][x]), max_char]))
                x += 1

            else:
                i += 1

        else:
            formatted_data[0] += (pad_data([str(data[i]), max_char]))
            i += 1

    else:
        print("Data formatted.", "\nStoring data...")
        return formatted_data


def pad_data(data):
    char_group = data[0]
    # TODO add method and a de-pad as one of the methods.
    while len(str(char_group)) < data[1]:
        char_group += "X"

    else:
        print(char_group)
        return char_group


def is_list(data):
    if type(data) == list:
        return True

    else:
        return False
