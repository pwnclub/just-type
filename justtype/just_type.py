import tkinter as tk
from tkinter import ttk

import test_area
import highscores
import submit_custom
import graphs

from matplotlib import style

style.use("ggplot")

class JustType(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.HighScores = highscores.HighScores
        self.TestArea = test_area.TestArea
        self.SubmitCustom = submit_custom.SubmitCustom
        self.GraphOverTime = graphs.GraphOverTime

        tk.Tk.wm_title(self, "Just Type")

        container = tk.Frame(self)
        container.pack()

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for Page in (self.TestArea, self.HighScores, self.SubmitCustom, self.GraphOverTime):
            frame = Page(container, self)
            frame.grid(row=0, column=0, sticky="nsew")

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

if __name__ == "__main__":      
    root = JustType()
    img = tk.PhotoImage(file='art/icon.ico')
    root.tk.call('wm', 'iconphoto', root._w, img)
    root.resizable(width=False, height=False)
    root.mainloop()
