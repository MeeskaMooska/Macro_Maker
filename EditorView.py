from tkinter import *
import threading



class EditorView(threading.Thread):
    def __init__(self, logging_data):
        self.self = self
        threading.Thread.__init__(self)
        self.logging_data = logging_data
        self.selected_index = []

        self.root = Tk()
        self.root.resizable(False, False)
        self.root.title("Editor View")

        # Listboxes that contain the macro data
        self.regular_key_listbox = Listbox(self.root)
        self.special_key_listbox = Listbox(self.root)
        self.mouse_click_listbox = Listbox(self.root)
        self.mouse_move_listbox = Listbox(self.root)
        self.mouse_scroll_listbox = Listbox(self.root)
        # A list of those listboxes that I can enumerate through
        self.listbox_list = [self.regular_key_listbox, self.special_key_listbox, self.mouse_click_listbox,
                             self.mouse_move_listbox, self.mouse_scroll_listbox]

        # Buttons at the bottom
        Label(self.root, text="Selected Data:").grid(row=2, column=0)
        self.selected_data_label = Label(self.root)
        self.selected_data_label.grid(row=2, column=1)
        self.selected_data_label.grid(row=2, column=1)
        self.edit_button = Button(self.root, text="Edit Selected").grid(row=3, column=0)
        self.delete_selected_button = Button(self.root, text="Delete Selected", command=self.delete_selected).grid(row=4, column=0)
        Label(self.root, text="Start Time:").grid(row=3, column=1)
        Label(self.root, text="Duration:").grid(row=4, column=1)
        self.start_time_entry = Entry(self.root).grid(row=3, column=2)
        self.duration_entry = Entry(self.root).grid(row=4, column=2)
        # Save opens dialog to get name of macro
        self.save_button = Button(self.root, text="Save Macro", command=self.save_macro).grid(row=3, column=4)
        self.delete_button = Button(self.root, text="Delete Macro").grid(row=4, column=4)

        self.config_listbox()

    def config_listbox(self):
        for count, data_list in enumerate(self.logging_data):
            for index, data in enumerate(data_list):
                self.listbox_list[count].insert(index, data)

    def selected_data(self, evt):
        for count, listbox in enumerate(self.listbox_list):
            if listbox.curselection() != ():
                self.selected_index = [self.listbox_list.index(listbox), listbox.curselection()[0]]
                self.update_selected_data_label()
                break

    def update_selected_data_label(self):
        self.selected_data_label.config(text=str(self.logging_data[self.selected_index[0]][self.selected_index[1]]))

    def delete_selected(self):
        self.listbox_list[self.selected_index[0]].delete(self.selected_index[1])
        self.logging_data[self.selected_index[0]].pop(int(self.selected_index[1]))

    def start(self):
        for count, title in enumerate(["Regular Keys", "Special Keys", "Mouse Click", "Mouse Move", "Mouse Scroll"]):
            Label(self.root, text=title).grid(row=0, column=count)
        for count, obj in enumerate(self.listbox_list):
            self.listbox_list[count].bind('<<ListboxSelect>>', self.selected_data)
            self.listbox_list[count].grid(row=1, column=count, padx=5)
        self.root.mainloop()

    def save_macro(self):
        print("afd")



editorView = EditorView([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14], [15, 16, 17, 18, 19],
                           [20, 21, 22, 23, 24]])
editorView.start()