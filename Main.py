from tkinter import *

import keyboard
import pyautogui as pag
import winsound
import time

from pynput.keyboard import *


def playsound():
    winsound.PlaySound("sound_1.wav", winsound.SND_FILENAME)


class Main:
    # initializes main
    def __init__(self):
        self.testPlan = [4, 6]
        self.sims_location = []
        self.start_point = []
        self.block_size = int
        self.screen_measurements = pag.size()  # gets screen measurements
        print(self.screen_measurements)
        self.root = Tk()  # initializes gui?
        self.build_gui()

    # builds gui
    # possibly cleanable
    def build_gui(self):
        sims_location_button = Button(self.root, text="get sims location", command=self.get_sims_location)
        sims_location_button.pack()
        block_size_button = Button(self.root, text="get block size", command=self.get_block_size)
        block_size_button.pack()
        start_point_button = Button(self.root, text="get start point", command=self.get_start_point)
        start_point_button.pack()
        build_button = Button(self.root, text="start building", command=self.test)
        build_button.pack()
        self.root.mainloop()

    # gets and gets sims location
    # needs cleaned
    def get_sims_location(self):
        playsound()
        time.sleep(2)
        self.sims_location = pag.position()
        playsound()

    # gets block size
    # possibly cleanable
    def get_block_size(self):
        pag.click(self.sims_location[0], self.sims_location[1])
        pag.moveTo(self.start_point[0], self.start_point[1], 1.0)
        playsound()
        time.sleep(2)
        x1 = pag.position()
        playsound()
        time.sleep(2)
        x2 = pag.position()
        playsound()
        if x1[0] > x2[0]:
            self.block_size = x1[0] - x2[0]

        else:
            self.block_size = x2[0] - x1[0]

    # gets the start point of the building
    def get_start_point(self):
        pag.click(self.sims_location[0], self.sims_location[1])
        playsound()
        time.sleep(4)
        self.start_point = pag.position()
        playsound()

    def build(self):
        time.sleep(.5)
        pag.click(self.sims_location[0], self.sims_location[1])
        pag.moveTo(self.start_point[0], self.start_point[1])
        pag.click()
        pag.mouseDown()
        pag.move(100, 100)
        pag.mouseUp()
        # pag.drag((self.block_size * self.testPlan[0]), (self.block_size * self.testPlan[1]), 1.0)

    def test(self):
        pag.click(self.sims_location[0], self.sims_location[1])
        pag.moveTo(self.start_point[0], self.start_point[1])
        pag.mouseDown()
        keyboard.press('d')
        time.sleep(1)
        keyboard.release('d')
        pag.move(1,1)
        pag.mouseUp()


Main()
