import tkinter as tk
from tkinter import ttk

import test_area
import highscores
import submit_custom
import graphs

from matplotlib import style

style.use('ggplot')


class JustType(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        img = tk.PhotoImage(file='art/icon.ico')
        self.tk.call('wm', 'iconphoto', self._w, img)

        self.HighScores = highscores.HighScores
        self.TestArea = test_area.TestArea
        self.SubmitCustom = submit_custom.SubmitCustom
        self.GraphOverTime = graphs.GraphOverTime

        tk.Tk.wm_title(self, 'Just Type')

        container = tk.Frame(self)
        container.pack()

        self.frames = {}

        for Page in (self.TestArea, self.HighScores, self.SubmitCustom, self.GraphOverTime):
            frame = Page(container, self)
            self.frames[Page] = frame

        self.show_frame(self.TestArea)

    def show_frame(self, tab):
        for frame in self.frames.values():
            frame.grid_remove()

        frame = self.frames[tab]
        frame.grid()

        if tab == self.TestArea:
            frame.change_test()
        elif tab == self.HighScores or tab == self.GraphOverTime:
            frame.update()
