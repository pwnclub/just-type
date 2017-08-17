import tkinter as tk
from tkinter import ttk

import shelve

import highscores
import test_area

import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

matplotlib.use('TkAgg')


class GraphOverTime(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        TestArea = test_area.TestArea
        HighScores = highscores.HighScores

        self.highscores_list = tk.StringVar()
        self.test = tk.IntVar()

        self.test_area_button = ttk.Button(self, text='Back to Testing Area', command=lambda: controller.show_frame(TestArea))
        self.graph_button = ttk.Button(self, text='Highscores', command=lambda: controller.show_frame(HighScores))
        self.reset_scores_button = tk.Button(self, font='System', padx=15, pady=5, background='red', foreground='white', text='Reset', borderwidth=0, command=self.reset_graphs)
        self.radio_easy = ttk.Radiobutton(self, text='Easy', command=self.update, variable=self.test, value=0)
        self.radio_advanced = ttk.Radiobutton(self, text='Advanced', command=self.update, variable=self.test, value=1)
        self.radio_nums = ttk.Radiobutton(self, text='Numbers', command=self.update, variable=self.test, value=2)

        self.figure = Figure(figsize=(5, 5), dpi=75)
        self.graph = self.figure.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.show()
        self.canvas.get_tk_widget().grid(column=1, row=0, columnspan=5, rowspan=10)

        self.test_area_button.grid(column=0, row=10)
        self.graph_button.grid(column=0, row=11)
        self.reset_scores_button.grid(column=3, row=10)
        self.radio_easy.grid(column=0, row=0, sticky='w')
        self.radio_advanced.grid(column=0, row=1, sticky='w')
        self.radio_nums.grid(column=0, row=2, sticky='w')

    def update(self):
        if self.test.get() == 0:
            test_id = 'easy'
        elif self.test.get() == 1:
            test_id = 'advanced'
        elif self.test.get() == 2:
            test_id = 'nums'

        self.graph.clear()

        test_count = []
        wpm = []

        graphs = shelve.open('data/graphs')

        for i in range(0, len(graphs[test_id])):
            test_count.append(i)
            wpm.append(graphs[test_id][i])

        self.graph.plot(test_count, wpm)
        self.canvas.show()

        graphs.close()

    def reset_graphs(self):
        if self.test.get() == 0:
            test_id = 'easy'
        elif self.test.get() == 1:
            test_id = 'advanced'
        elif self.test.get() == 2:
            test_id = 'nums'

        if messagebox.askokcancel('Reset', 'Are you sure you want to reset this leaderboard?'):
            graphs = shelve.open('data/graphs')
            graphs[test_id] = []
            graphs.close()
            self.update()
