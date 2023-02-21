from tkinter import *


class EditorView:
    def __init__(self):
        self.self = self
        self.root = None
        self.logging_data = None
        self.selected_index = None
        self.running = False

        # Declaring all objects
        # Listbox
        self.regular_key_listbox = None
        self.special_key_listbox = None
        self.mouse_click_listbox = None
        self.mouse_move_listbox = None
        self.mouse_scroll_listbox = None
        self.listbox_list = None

        # Buttons and Labels
        self.selected_data_label = None
        self.edit_button = None
        self.delete_selected_button = None
        self.start_time_entry = None
        self.duration_entry = None
        self.save_button = None
        self.delete_button = None

    def setup_gui(self):
        # Root settings
        self.root = Tk()
        self.root.resizable(False, False)
        self.root.title("Editor View")
        self.root.protocol("WM_DELETE_WINDOW", self.closed)

        # Listbox settings
        self.regular_key_listbox = Listbox(self.root)
        self.special_key_listbox = Listbox(self.root)
        self.mouse_click_listbox = Listbox(self.root)
        self.mouse_move_listbox = Listbox(self.root)
        self.mouse_scroll_listbox = Listbox(self.root)
        self.listbox_list = [self.regular_key_listbox, self.special_key_listbox, self.mouse_click_listbox,
                             self.mouse_move_listbox, self.mouse_scroll_listbox]
        self.config_listbox()
        for count, title in enumerate(["Regular Keys", "Special Keys", "Mouse Click", "Mouse Move", "Mouse Scroll"]):
            Label(self.root, text=title).grid(row=0, column=count)
        for count, obj in enumerate(self.listbox_list):
            self.listbox_list[count].bind('<<ListboxSelect>>', self.selected_data)
            self.listbox_list[count].grid(row=1, column=count, padx=5)

        # Buttons and Labels
        Label(self.root, text="Selected Data:").grid(row=2, column=0)
        self.selected_data_label = Label(self.root)
        self.edit_button = Button(self.root, text="Edit Selected").grid(row=3, column=0)
        self.delete_selected_button = Button(self.root, text="Delete Selected", command=self.delete_selected).grid(
            row=4, column=0)
        Label(self.root, text="Start Time:").grid(row=3, column=1)
        Label(self.root, text="Duration:").grid(row=4, column=1)
        self.start_time_entry = Entry(self.root)
        self.duration_entry = Entry(self.root)
        self.start_time_entry.grid(row=3, column=2)
        self.duration_entry.grid(row=4, column=2)
        self.save_button = Button(self.root, text="Save Macro", command=self.save_macro).grid(row=3, column=4)
        self.delete_button = Button(self.root, text="Delete Macro").grid(row=4, column=4)

        # Starts the mainloop
        self.root.mainloop()

    def config_listbox(self):
        for count, data_list in enumerate(self.logging_data):
            for index, data in enumerate(data_list):
                self.listbox_list[count].insert(index, data)

    def selected_data(self, event):
        for count, listbox in enumerate(self.listbox_list):
            if listbox.curselection() != ():
                self.selected_index = [self.listbox_list.index(listbox), listbox.curselection()[0]]
                self.selected_data_label.config(text=str(self.logging_data[self.selected_index[0]][self.selected_index[1]]))
                break

    def delete_selected(self):
        self.listbox_list[self.selected_index[0]].delete(self.selected_index[1])
        self.logging_data[self.selected_index[0]].pop(int(self.selected_index[1]))

    def save_macro(self):
        pass

    def closed(self):
        self.root.destroy()
        self.__init__()