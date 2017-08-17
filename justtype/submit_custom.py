import tkinter as tk
from tkinter import ttk

import test_area


class SubmitCustom(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.TestArea = test_area.TestArea
        self.controller = controller

        self.new_test = tk.Text(self, font='Courier', height=10, width=60, wrap='word')
        self.submit_button = tk.Button(self, text='Submit!', font='System', padx=15, pady=5, background='green', foreground='white', borderwidth=0, command=self.submit_commands)
        self.reset_default_button = ttk.Button(self, text='Default Text', command=self.reset_default)
        self.clear_button = ttk.Button(self, text='Clear Text', command=self.empty_input)
        self.test_area_button = ttk.Button(self, text='Home', command=lambda: controller.show_frame(self.TestArea))

        self.new_test.grid(column=0, row=0, columnspan=3)
        self.submit_button.grid(column=1, row=1, pady=5)
        self.reset_default_button.grid(column=0, row=1)
        self.clear_button.grid(column=2, row=1)
        self.test_area_button.grid(column=1, row=2, pady=5)

    def submit_commands(self):
        self.update_custom()
        self.controller.show_frame(self.TestArea)

    def retrieve_input(self):
        self.input = self.new_test.get('1.0', tk.END)

    def update_custom(self):
        self.retrieve_input()
        custom_test = open('custom/custom.txt', 'w')
        custom_test.write(self.input)

    def reset_default(self):
        self.empty_input()
        string = ''
        custom_test = open('custom/custom_default.txt', 'r')
        self.new_test.insert(tk.END, custom_test.read())
        self.update_custom()

    def empty_input(self):
        self.new_test.delete('1.0', tk.END)
        self.update_custom()
