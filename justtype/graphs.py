import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

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

        self.test_area_button = ttk.Button(self, text='Home', command=lambda: controller.show_frame(TestArea))
        self.graph_button = ttk.Button(self, text='Highscores', command=lambda: controller.show_frame(HighScores))
        self.reset_scores_button = tk.Button(self, font='System', padx=15, pady=5, background='red', foreground='white', text='Reset', borderwidth=0, command=self.reset_graphs)
        self.radio_easy = ttk.Radiobutton(self, text='Easy', command=self.update, variable=self.test, value=0)
        self.radio_advanced = ttk.Radiobutton(self, text='Advanced', command=self.update, variable=self.test, value=1)
        self.radio_nums = ttk.Radiobutton(self, text='Numbers', command=self.update, variable=self.test, value=2)

        self.figure = Figure(figsize=(6, 4), dpi=75)
        self.graph = self.figure.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.show()
        self.canvas.get_tk_widget().grid(column=1, row=0, columnspan=5, rowspan=10)

        self.radio_easy.grid(column=0, row=0, sticky='w')
        self.radio_advanced.grid(column=0, row=1, sticky='w')
        self.radio_nums.grid(column=0, row=2, sticky='w')
        self.reset_scores_button.grid(column=0, row=5, padx=5)
        self.test_area_button.grid(column=0, row=8)
        self.graph_button.grid(column=0, row=9)

    def update(self):
        test_id = self.get_id()

        self.graph.clear()

        self.test_count = []
        self.wpm = []
        title = test_id.capitalize() + " test "

        if test_id == 'nums':
            title += "CPM"
        else:
            title += "WPM"

        graphs = shelve.open('graphs')

        self.build_graphs(graphs, test_id)

        self.graph.set_title(title)
        self.graph.plot(self.test_count, self.wpm)
        self.canvas.show()

        graphs.close()

    def build_graphs(self, data, test_id):
        try:
            for i in range(0, len(data[test_id])):
                self.test_count.append(i)
                self.wpm.append(data[test_id][i])
        except:
            data['easy'] = []
            data['advanced'] = []
            data['nums'] = []
            self.build_graphs(data, test_id)

    def reset_graphs(self):
        test_id = self.get_id()

        if messagebox.askokcancel('Reset', 'Are you sure you want to reset this leaderboard?'):
            graphs = shelve.open('graphs')
            graphs[test_id] = []
            graphs.close()
            self.update()

    def get_id(self):
        if self.test.get() == 0:
            return 'easy'
        elif self.test.get() == 1:
            return 'advanced'
        elif self.test.get() == 2:
            return 'nums'
