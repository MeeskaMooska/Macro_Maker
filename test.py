import time
import os
import pyautogui as pag
import sims_build_toolkit as sbt
# todo change METHODS to methods in terminal control


# TODO Testing HouseMeasurements with BuildHouse with test variables
class BuildHouse:
    def __init__(self):
        # Todo Needed variables for house:
        #  Basic Info:
        #   screen_info: [[1920, 1080], [515, 487], 74]
        #  some indexing variable
        #  screen-details:
        #   screen_info, block_size, sim_location
        #  house-details:
        #   room_x, room_y
        #  possibly reformat matrix below
        #  [screen_info, sim_location, block_size, room_x, room_y]
        #  i += 1
        #  the block size, screen_info and sims_location are all static and can take up the space of variables
        self.plan_matrix = [[[1920, 1080], [515, 487], 75, [12, 14]], [[[1920, 1080], [515, 487], 75, [12, 14]]]]
        self.screen_info = 1
        self.plan_matrix = [[12, 14], [10, 14]]
        self.build_room()
        '''self.plan_matrix = plan_matrix
        self.matrix_length = len(self.plan_matrix)
        self.room_index = 0
        self.nested_matrix_length = len(self.plan_matrix[self.room_index])
        self.attribute_index = 0
        self.room_x = 0
        self.room_y = 0
        self.build_room()'''

    def build_room(self):
        '''convert_block_size = lambda house_measurements, block_size: house_measurements * block_size
               convert_block_size(self.plan_matrix[0][3], self.plan_matrix[0][2])'''
        ''' x = self.plan_matrix
        self.room_x, self.room_y = x[self.room_index][0], x[self.room_index][1]
        print(self.room_x, self.room_y)'''
        # required info to build room:
        #  room_x&y converted to block size
        #  while loop to run through plan_matrix with i += 1
        #  after all info can be used and applied in the correct way we use pag
        i = 0
        while i < len(self.plan_matrix):
            converted_measurements = [self.plan_matrix[3][0] * self.plan_matrix[2],
                                      self.plan_matrix[3][1] * self.plan_matrix[2]]
            print(converted_measurements)
            i += 1

        else:
            print("stop")


# TODO Testing HouseMeasurements with BuildHouse with test variables
class HouseMeasurements:
    def __init__(self):
        self.plan_matrix = []
        self.get_house_measurements()

    def get_house_measurements(self):
        room_x, room_y = input("Enter room measurements in feet with a space separating the values: ").split()
        question = "You entered " + room_x + " " + room_y + " as the measurements for this room, is that correct?"
        if sbt.yes_no_question(question):
            print("these plans were correct")
            self.plan_matrix.append([sbt.nearest_even(room_x), sbt.nearest_even(room_y)])
            if sbt.yes_no_question("Amazing, do you have more room measurements to input?"):
                self.get_house_measurements()

            else:
                BuildHouse(self.plan_matrix)

        else:
            print("Please re-enter correct plans...")
            self.get_house_measurements()


class OneUseFuncs:
    def __init__(self, method):
        self.method = method
        self.methods = {0: self.help_command, 1: self.list_commands}
        self.methods[method]()

    def help_command(self):
        # TODO help commands
        print("helping.")

    def list_commands(self):
        print("listing commands...")


class Test:
    def __init__(self, data):
        self.data = data
        self.methods = {0: self.test_sim_location, 1: self.test_block_size}
        if type(self.data) == list:
            self.methods[data[0]]()

        else:
            print("Im not sure if ill ever actually get non list data")

    def test_sim_location(self):
        pag.moveTo(self.data[1][0], self.data[1][1], 2)
        if sbt.yes_no_question("Would you like to retest it?"):
            self.test_sim_location()

        else:
            if sbt.yes_no_question("Was that measurement correct?"):
                print("Getting block size...")
                time.sleep(1)
                self.data = [1, self.data[1], [0]]
                GetScreenDetails(self.data)

            else:
                print("You may re-enter the location of your sims now.")
                time.sleep(1)
                self.data = None
                GetScreenDetails(self.data)

    def test_block_size(self):
        pag.move(self.data[2], self.data[3], self.data[4])
        if sbt.yes_no_question("Would you like to retest it?"):
            self.test_block_size()

        else:
            if sbt.yes_no_question("Was that measurement correct?"):
                self.data = [2, self.data[1], self.data[2]]
                time.sleep(1)
                GetScreenDetails(self.data)

            else:
                print("You may re-enter the size of a block now.")
                time.sleep(1)
                self.data = [1, self.data[1], [0]]
                GetScreenDetails(self.data)


# todo get real required screen details.
#  Testing: printing variables
#  Function to return screen details
class GetScreenDetails:
    def __init__(self, data=None):
        if data is None:
            data = [0, [0], [0]]
        self.data = data
        self.methods = {0: self.get_sims_location, 1: self.get_block_size, 2: self.store_screen_details}
        #todo place this where its used below
        self.screen_measurements = [(pag.size())[0], (pag.size())[1]]
        self.sims_location = self.data[1]
        self.block_size = self.data[2]
        self.char_group = ""
        self.generic_string = "A beep will sound at the start of the first 5 seconds and then the next beep" \
                              " will represent the end of the first measurement and the start of the second," \
                              " the third beep is the end of the final measurement."
        self.methods[self.data[0]]()
        # todo function to check for available data

    # todo add test for sims location
    def get_sims_location(self):
        print("There is some information needed before you can get to making houses, we will get that now.")
        generic_string_1 = "First we need to get the location of the sims on your taskbar, I recommend clicking " \
                           "and dragging the sims to the front of your taskbar so that closing " \
                           "applications wont affect the location of the sims"
        print(generic_string_1 + "\n" + self.generic_string)
        if sbt.yes_no_question("Are you ready to input your sims location?"):
            sbt.play_sound()
            time.sleep(2)
            self.sims_location = [pag.position()[0], pag.position()[1]]
            sbt.play_sound()
            if sbt.yes_no_question("Would you like to test these measurements?"):
                Test([0, self.sims_location, 0.4])

            else:
                self.get_block_size()
        else:
            tc = TerminalCon()
            tc.get_command()

    def get_block_size(self):
        generic_string_1 = "Now we need to get the size of one sim block on your computer, so when this command" \
                           " runs the program will open the sims for you, all you have to do is place your cursor"
        generic_strings = ["onto the left or right edge of a 2x2 block in the then after the beep"
                           "Move it to the other edge and hold until the next beep"]
        print(generic_string_1 + generic_strings[0] + "\n" + self.generic_string)
        if sbt.yes_no_question("Are you ready to input your block measurements?"):
            mouse_locations = []
            pag.click(self.sims_location[0], self.sims_location[1], 0.0)
            sbt.play_sound()
            time.sleep(2)
            mouse_locations.append(sbt.get_mouse_location(0))
            sbt.play_sound()
            time.sleep(2)
            mouse_locations.append(sbt.get_mouse_location(0))
            sbt.play_sound()
            # todo make convert block size a function in sbt
            convert_block_size = lambda x1, x2: x1 - x2
            self.block_size = convert_block_size(max(mouse_locations), min(mouse_locations))
            if sbt.yes_no_question("Would you like to test to see if the block size is correct?"):
                Test([1, self.sims_location, self.block_size, 0, 1,])

            else:
                print("Formatting data...")
                self.store_screen_details()

    def store_screen_details(self):
        print([self.screen_measurements, self.sims_location, self.block_size])
        data = sbt.format_data([self.screen_measurements, self.sims_location, self.block_size])
        with open("screen_measurements.txt", "w") as file:
            file.write(data[0])
            print("Data stored.")
            HouseMeasurements()

    def read_screen_details(self):
        screen_info = []
        with open("screen_measurements.txt", "r") as file:
            is_end = True
            i = 0
            while is_end:
                char = file.read(1)
                is_end = self.is_valid_char([i, char])

    def is_valid_char(self, data):
        if data[1] == "X" or len(self.char_group) >= 4:
            return False

        elif data[0] < os.stat("screen_measurements.txt").st_size:
            self.char_group += data[1]
            return False

        else:
            self.char_group += data[1]
            return True

        # todo:
        #  read screen_measurements.txt


# todo testing: build_house
class TerminalCon:
    def __init__(self):
        self.command = ""
        self.COMMANDS = {"HELP": [OneUseFuncs, 0], "COMMANDS": [OneUseFuncs, 1],
                         "NEW_HOUSE": HouseMeasurements, "SCREEN_INFO": GetScreenDetails,
                         "BUILD_HOUSE": BuildHouse}

        print("Welcome to the sims autobuilder.", "\nNote: that houses will not be built exactly to scale."
                                                  "Note: this program may bug out with multiple screens.",
              "\nThe house measurements will be built to the measurements provided and rounded up to"
              " The nearest even number, so give or take up to 1 inch")
        print("For help type ""help"" for a list of commands type ""commands"" nothing is case sensitive.")
        self.get_command()

    def get_command(self):
        self.command = input("Enter a command: ").upper()
        if self.command in self.COMMANDS:
            self.run_command(self.command)

        else:
            print("Error: invalid command.")
            self.get_command()

    def run_command(self, command):
        if type(self.COMMANDS[command]) == list:
            func = self.COMMANDS[command][0]
            func(self.COMMANDS[command][1])

        else:
            self.COMMANDS[command]()



TerminalCon()


'''            with open("screen_measurements.txt", "w") as file:
                file.seek(x)
                file.write(data[s])'''