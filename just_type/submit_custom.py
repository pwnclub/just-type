import tkinter as tk
from tkinter import ttk

import shelve

import test_area

class SubmitCustom(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.TestArea = test_area.TestArea
        self.controller = controller
        self.new_test = tk.Text(self, height=8, width=50)

        submit_button = ttk.Button(self, text="Submit!", command=self.submit_commands)
        reset_default_button = ttk.Button(self, text="Default Text", command=self.reset_default)
        clear_button = ttk.Button(self, text="Clear Text", command=self.empty_input)
        test_area_button = ttk.Button(self, text="Back to Testing Area", command=lambda: controller.show_frame(self.TestArea))

        self.new_test.grid(column=0, row=0, columnspan=3)

        submit_button.grid(column=1, row=1)
        reset_default_button.grid(column=0, row=1)
        clear_button.grid(column=2, row=1)
        test_area_button.grid(column=1, row=2)

    def submit_commands(self):
        self.update_custom()
        self.controller.show_frame(self.TestArea)

    def retrieve_input(self):
        self.input = self.new_test.get("1.0", tk.END)

    def update_custom(self):
        self.retrieve_input()
        custom_test = shelve.open('custom', flag='n')
        custom_test = shelve.open('custom', writeback=True)
        custom_test['sample'] = self.input.split()
        custom_test.sync()
        custom_test.close()

    def reset_default(self):
        self.empty_input()
        string = ''
        with open('custom_default.txt', 'r') as file:
            for line in file:
                for word in line.split():
                    string += word + ' '
        self.new_test.insert('end', string)
        self.update_custom()

    def empty_input(self):
        self.new_test.delete('1.0', tk.END)
        self.update_custom()