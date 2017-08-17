import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import shelve
import time

import test_area
import graphs


class HighScores(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        TestArea = test_area.TestArea
        GraphOverTime = graphs.GraphOverTime

        self.highscores_list = tk.StringVar()
        self.test = tk.IntVar()

        self.highscores_label = tk.Label(self, justify='left', font=('Calibri', 12), width=50)
        self.test_area_button = ttk.Button(self, text='Home', command=lambda: controller.show_frame(TestArea))
        self.graph_button = ttk.Button(self, text='Graphs', command=lambda: controller.show_frame(GraphOverTime))
        self.reset_scores_button = tk.Button(self, font='System', padx=15, pady=5, background='red', foreground='white', text='Reset', borderwidth=0, command=self.reset_scores)
        self.radio_easy = ttk.Radiobutton(self, text='Easy', command=self.update, variable=self.test, value=0)
        self.radio_advanced = ttk.Radiobutton(self, text='Advanced', command=self.update, variable=self.test, value=1)
        self.radio_nums = ttk.Radiobutton(self, text='Numbers', command=self.update, variable=self.test, value=2)

        self.highscores_label['textvariable'] = self.highscores_list

        self.highscores_label.grid(column=1, row=0, columnspan=2, rowspan=10, sticky='w')
        self.radio_easy.grid(column=0, row=0, sticky='w')
        self.radio_advanced.grid(column=0, row=1, sticky='w')
        self.radio_nums.grid(column=0, row=2, sticky='w')
        self.reset_scores_button.grid(column=0, row=5, padx=5)
        self.test_area_button.grid(column=0, row=8)
        self.graph_button.grid(column=0, row=9)

    def update(self):
        if self.test.get() == 0:
            test_id = 'easy'
        elif self.test.get() == 1:
            test_id = 'advanced'
        elif self.test.get() == 2:
            test_id = 'nums'

        string = ''

        highscores = shelve.open('data/highscores')

        for i in range(1, 11):
            string += str(i) + '.  ' + str(highscores[test_id][i-1][0])
            if test_id != 'nums':
                string += ' WPM '
            else:
                string += ' CPM '
            string += '\t' + str(highscores[test_id][i-1][1]) + '\t' + str(highscores[test_id][i-1][2]) + '\n'

        self.highscores_list.set(string)

        highscores.close()

    def reset_scores(self):
        if self.test.get() == 0:
            test_id = 'easy'
        elif self.test.get() == 1:
            test_id = 'advanced'
        elif self.test.get() == 2:
            test_id = 'nums'

        if messagebox.askokcancel('Reset', 'Are you sure you want to reset this leaderboard?'):
            highscores = shelve.open('data/highscores')
            highscores[test_id] = [[0, '0.00%', time.strftime('%d/%m/%Y')]] * 10
            highscores.sync()
            highscores.close()
            self.update()
