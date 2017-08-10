from tkinter import *
from tkinter import ttk
import random
import time
import os


class MyWindow(Frame):
    def __init__(self, parent):
        super().__init__()

        self.num_words_display = 12
        self.timer_limit = 10

        self.wordbank = ['the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'I', 'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do']
        self.cur_rand_nums = [0] * self.num_words_display
        self.nxt_rand_nums = [0] * self.num_words_display

        self.cur_char = 0
        self.cur_letter = 0
        self.wrong_letter = 0
        self.cur_word = 0
        self.right_words = 0
        self.right_chars = 0
        self.wrong_words = 0
        self.wrong_chars = 0

        self.start_count = False

        self.typing = StringVar()
        self.right_cnt = StringVar()
        self.wrong_cnt = StringVar()
        self.time_or_wpm = StringVar()

        self.text = Text(self, width=50, height=2)
        self.entry = Entry(self, textvariable=self.typing, takefocus=0)
        self.right_word_label = Label(self, foreground='green')
        self.wrong_word_label = Label(self, foreground='red')
        self.countdown_label = Label(self)

        self.right_word_label['textvariable'] = self.right_cnt
        self.wrong_word_label['textvariable'] = self.wrong_cnt
        self.countdown_label['textvariable'] = self.time_or_wpm

        self.right_cnt.set('right: {}'.format(self.right_words))
        self.wrong_cnt.set('Inright: {}'.format(self.wrong_words))
        self.time_or_wpm.set('Type to start!')

        self.entry.focus_set()

        for i in range(0, self.num_words_display):
            random_num = random.randint(0, len(self.wordbank)-1)
            self.cur_rand_nums[i] = random_num

            self.text.insert('end', self.wordbank[random_num] + ' ')

        self.text.insert('end', '\n')

        for i in range(0, self.num_words_display):
            random_num = random.randint(0, len(self.wordbank)-1)
            self.nxt_rand_nums[i] = random_num

            self.text.insert('end', self.wordbank[random_num] + ' ')

        self.addEffect('current_right')
        self.text.config(state=DISABLED)

        self.text.tag_config('current_right', background='gray')
        self.text.tag_config('current_wrong', background='red')
        self.text.tag_config('right', foreground='green')
        self.text.tag_config('wrong', foreground='red')

        self.text.pack()
        self.entry.pack()
        self.right_word_label.pack()
        self.wrong_word_label.pack()
        self.countdown_label.pack()

        root.bind('<KeyPress>', self.onKeyPress)

    def countdown(self, count):
        self.time_or_wpm.set('{}'.format(count))

        if count > 0:
            self.after(1000, self.countdown, count-1)
        else:
            wpm = int(self.right_chars // 5 * (60 / self.timer_limit))
            self.time_or_wpm.set('WPM: {}'.format(wpm))

    def onKeyPress(self, event):
        if self.entry != self.entry.focus_get():
            return

        if not self.start_count:    # if test timer hasn't started, start it
            self.start_count = True
            self.countdown(self.timer_limit)

        self.text.config(state=NORMAL)

        bank_index = self.cur_rand_nums[self.cur_word]

        try:
            if ord(event.char) == 8:  # backspace

                self.wrong_letter -= 1
                self.cur_letter -= 1

                if self.wrong_letter <= 0:
                    self.removeEffect('current_wrong')
                    self.addEffect('current_right')
                    self.wrong_letter = 0

                if self.cur_letter <= 0:
                    self.cur_letter = 0

                self.text.config(state=DISABLED)
                return

            if ord(event.char) == 32:     # space
                self.removeEffect('current_right')
                self.removeEffect('current_wrong')

                self.entry.delete(0, END)

                if (self.wrong_letter == 0 and
                    self.cur_letter >= len(self.wordbank[bank_index])):
                    self.addEffect('right')
                    self.right_words += 1
                    self.right_cnt.set('right: {}'.format(self.right_words))
                    self.right_chars += len(self.wordbank[bank_index])
                else:
                    self.addEffect('wrong')
                    self.wrong_words += 1
                    self.wrong_cnt.set('Inright: {}'.format(self.wrong_words))
                    self.wrong_chars += len(self.wordbank[bank_index])

                self.cur_letter = 0
                self.wrong_letter = 0

                self.cur_char += len(self.wordbank[bank_index]) + 1
                self.cur_word += 1

                if self.cur_word >= len(self.cur_rand_nums):
                    self.moveNextLine()

                self.text.config(state=DISABLED)
                self.addEffect('current_right')
                return

            if (self.cur_letter < len(self.wordbank[bank_index]) and
                self.wordbank[bank_index][self.cur_letter] == event.char and
                self.wrong_letter == 0):
                self.removeEffect('current_wrong')
                self.addEffect('current_right')
            else:
                self.removeEffect('current_right')
                self.addEffect('current_wrong')
                self.wrong_letter += 1

            self.cur_letter += 1
        except:
            return
        finally:
            self.text.config(state=DISABLED)

    def addEffect(self, typeOf):
        bank_index = self.cur_rand_nums[self.cur_word]
        self.text.tag_add(
            typeOf,
            '1.{}'.format(self.cur_char),
            '1.{}'.format(self.cur_char + len(self.wordbank[bank_index])))

    def removeEffect(self, typeOf):
        bank_index = self.cur_rand_nums[self.cur_word]
        self.text.tag_remove(
            typeOf,
            '1.{}'.format(self.cur_char),
            '1.{}'.format(self.cur_char + len(self.wordbank[bank_index])))

    def moveNextLine(self):
        self.cur_rand_nums = list(self.nxt_rand_nums)

        self.cur_word = 0
        self.cur_char = 0

        self.text.delete('1.0', END)

        for i in range(0, self.num_words_display):
            self.text.insert(
                'end',
                self.wordbank[self.cur_rand_nums[i]] + ' ')

        self.text.insert('end', '\n')

        for i in range(0, self.num_words_display):
            random_num = random.randint(0, len(self.wordbank)-1)
            self.nxt_rand_nums[i] = random_num

            self.text.insert(
                'end',
                self.wordbank[random_num] + ' ')

root = Tk()

MyWindow(root).pack()

root.mainloop()
