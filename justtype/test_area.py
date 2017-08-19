import tkinter as tk
from tkinter import ttk
from dictionary import words
from operator import itemgetter

import random
import time
import sys
import os
import math
import shelve

import just_type
import highscores
import submit_custom

import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
matplotlib.use('TkAgg')

TIMER_LIMIT = 3


class TestArea(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.HighScores = highscores.HighScores
        self.SubmitCustom = submit_custom.SubmitCustom

        # start off with 'easy' wordbank
        self.wordbank = words[0]
        self.cur_rand_nums = []
        self.nxt_rand_nums = []
        self.reset_variables()
        self.init_ui()

    def init_ui(self):
        self.typing = tk.StringVar()
        self.right_cnt = tk.StringVar()
        self.wrong_cnt = tk.StringVar()
        self.time_or_wpm = tk.StringVar()
        self.live_wpm = tk.StringVar()
        self.test = tk.IntVar()

        self.figure = Figure(figsize=(5, 5), dpi=40)
        self.graph = self.figure.add_subplot(111)

        self.text = tk.Text(self, font=('Courier', 22), borderwidth=0, width=50, height=2)
        self.entry = ttk.Entry(self, textvariable=self.typing, font=('Courier', 20), takefocus=0)
        self.right_word_label = tk.Label(self, foreground='green', font=('Calibri', 15))
        self.wrong_word_label = tk.Label(self, foreground='red', font=('Calibri', 15))
        self.countdown_label = tk.Label(self, font=('Calibri', 15))
        self.live_wpm_label = tk.Label(self, width=8, font=('System', 15))
        self.reset_button = tk.Button(self, text='Reset', font='System', padx=15, pady=5, background='red', foreground='white', borderwidth=0, command=self.reset)
        self.radio_easy = ttk.Radiobutton(self, text='Easy', variable=self.test, value=0, command=self.change_test)
        self.radio_advanced = ttk.Radiobutton(self, text='Advanced', variable=self.test, value=1, command=self.change_test)
        self.radio_nums = ttk.Radiobutton(self, text='Numbers', variable=self.test, value=2, command=self.change_test)
        self.radio_custom = ttk.Radiobutton(self, text='Custom', variable=self.test, value=3, command=self.change_test)
        self.open_hs_button = ttk.Button(self, text='High Scores', command=lambda: [self.reset(), self.controller.show_frame(self.HighScores)])
        self.open_custom_button = ttk.Button(self, text='Custom Test', command=lambda: [self.reset(), self.controller.show_frame(self.SubmitCustom)])

        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.show()

        self.right_word_label['textvariable'] = self.right_cnt
        self.wrong_word_label['textvariable'] = self.wrong_cnt
        self.countdown_label['textvariable'] = self.time_or_wpm
        self.live_wpm_label['textvariable'] = self.live_wpm

        self.right_cnt.set('Correct: {}'.format(self.right_words))
        self.wrong_cnt.set('Incorrect: {}'.format(self.wrong_words))
        self.time_or_wpm.set('Type to start!')
        self.live_wpm.set('{} WPM'.format(self.cur_wpm))

        self.entry.focus_set()

        self.init_rand_gen()

        self.add_effect('current_right')
        self.text.config(state=tk.DISABLED)

        self.text.tag_config('current_right', background='gray')
        self.text.tag_config('current_wrong', background='red')
        self.text.tag_config('right', foreground='green')
        self.text.tag_config('wrong', foreground='red')

        self.text.grid(column=0, row=0, columnspan=3)
        self.entry.grid(column=1, row=1)
        self.reset_button.grid(column=2, row=1)
        self.right_word_label.grid(column=1, row=2)
        self.wrong_word_label.grid(column=1, row=3)
        self.live_wpm_label.grid(column=2, row=2)
        self.countdown_label.grid(column=1, row=4)
        self.radio_easy.grid(column=0, row=1, sticky='w')
        self.radio_advanced.grid(column=0, row=2, sticky='w')
        self.radio_nums.grid(column=0, row=3, sticky='w')
        self.radio_custom.grid(column=0, row=4, sticky='w')
        self.open_hs_button.grid(column=2, row=3)
        self.open_custom_button.grid(column=2, row=4)
        self.canvas.get_tk_widget().grid(column=3, row=0, rowspan=5)

        self.controller.bind('<KeyPress>', self.on_key_press)

    def reset(self):
        self.text.config(state=tk.NORMAL)
        self.reset_variables()

        if self.test.get() != 3:
            self.init_rand_gen()
        else:
            self.init_rand_gen_custom()

        self.text.config(state=tk.DISABLED)
        self.entry.config(state=tk.NORMAL)
        self.entry.delete(0, tk.END)
        self.entry.focus_set()

        self.right_cnt.set('Correct: {}'.format(self.right_words))
        self.wrong_cnt.set('Incorrect: {}'.format(self.wrong_words))
        self.time_or_wpm.set('Type to start!')

        if self.test.get() == 2:
            self.live_wpm.set('{} CPM'.format(self.cur_cpm))
        else:
            self.live_wpm.set('{} WPM'.format(self.cur_wpm))

        self.graph.clear()
        self.canvas.show()

    def reset_variables(self):
        self.cur_char = 0
        self.cur_letter = 0
        self.wrong_letter = 0
        self.cur_word = 0
        self.right_words = 0
        self.right_chars = 0
        self.wrong_words = 0
        self.wrong_chars = 0
        self.cur_wpm = 0
        self.cur_cpm = 0
        self.cur_index = 0

        self.start_count = False
        self.stop = False

        self.xList = []
        self.yList = []

    def change_test(self):
        if self.test.get() != 3:
            self.wordbank = words[self.test.get()]
        else:
            custom_test = open('custom/custom.txt', 'r')
            self.wordbank = custom_test.read().split()

        self.reset()

    def init_rand_gen(self):
        self.text.delete('1.0', tk.END)
        del self.cur_rand_nums[:]
        total_chars = 0

        while True:
            random_num = random.randint(0, len(self.wordbank) - 1)

            if total_chars + len(self.wordbank[random_num]) + 1 > 50:
                break

            self.cur_rand_nums.append(random_num)
            self.text.insert('end', self.wordbank[random_num] + ' ')

            total_chars += len(self.wordbank[random_num]) + 1

        self.gen_nxt_line()

    def init_rand_gen_custom(self):
        self.text.delete('1.0', tk.END)
        del self.cur_rand_nums[:]
        total_chars = 0

        for i in range(0, len(self.wordbank)):
            if total_chars + len(self.wordbank[i]) + 1 > 50:
                self.cur_index = i
                self.gen_nxt_line_custom(i)
                break

            self.cur_rand_nums.append(i)
            self.text.insert('end', self.wordbank[i] + ' ')

            total_chars += len(self.wordbank[i]) + 1

    def gen_nxt_line(self):
        del self.nxt_rand_nums[:]
        total_chars = 0

        self.text.insert('end', '\n')

        while True:
            random_num = random.randint(0, len(self.wordbank) - 1)

            if total_chars + len(self.wordbank[random_num]) + 1 > 50:
                break

            self.nxt_rand_nums.append(random_num)
            self.text.insert('end', self.wordbank[random_num] + ' ')

            total_chars += len(self.wordbank[random_num]) + 1

    def gen_nxt_line_custom(self, start):
        del self.nxt_rand_nums[:]
        total_chars = 0

        self.text.insert('end', '\n')

        for i in range(start, len(self.wordbank)):
            if total_chars + len(self.wordbank[i]) + 1 > 50:
                self.cur_index += i - start
                return

            self.nxt_rand_nums.append(i)
            self.text.insert('end', self.wordbank[i] + ' ')

            total_chars += len(self.wordbank[i]) + 1

        self.cur_index = len(self.wordbank)

    def countdown(self, count):
        # prevents two timers from running at once
        if not self.start_count:
            return

        self.time_or_wpm.set('{}'.format(math.ceil(count)))

        if count > 0:
            self.after(100, self.countdown, count - 0.1)

            # stops from dividing by zero, which would lead to first letter being marked incorrect
            if count != TIMER_LIMIT:
                self.cur_wpm = int(self.right_chars * (60 / (TIMER_LIMIT - count)) // 5)

                if self.test.get() == 2:
                    self.cur_cpm = int(self.right_chars * (60 / (TIMER_LIMIT - count)) / 2)

            if self.test.get() == 2:
                self.live_wpm.set('{} CPM'.format(self.cur_cpm))
                wpm_or_cpm = self.cur_cpm
            else:
                self.live_wpm.set('{} WPM'.format(self.cur_wpm))
                wpm_or_cpm = self.cur_wpm

            if count == TIMER_LIMIT:
                return
            elif round(count, 2).is_integer():
                self.graph.clear()
                self.xList.append(int(TIMER_LIMIT-count))
                self.yList.append(wpm_or_cpm)

                if self.test.get() == 2:
                    self.graph.set_title("Live CPM")
                else:
                    self.graph.set_title("Live WPM")

                self.graph.plot(self.xList, self.yList)
                self.canvas.show()
        else:
            wpm = int(self.right_chars * (60 / TIMER_LIMIT) / 5)
            cpm = int(self.right_chars * (60 / TIMER_LIMIT) / 2)

            total_chars = (self.right_chars + self.wrong_chars)

            if total_chars == 0:
                accuracy = 0.00
            else:
                accuracy = round((self.right_chars / total_chars) * 100, 2)

            if self.test.get() == 2:
                # divide by two here because we don't want to include skipped spaces which make up half of CPM
                self.time_or_wpm.set('CPM: {}'.format(cpm) + '   ' + 'Accuracy: {}%'.format(accuracy))
            else:
                self.time_or_wpm.set('WPM: {}'.format(wpm) + '   ' + 'Accuracy: {}%'.format(accuracy))

            # if the user types a word or two it doesn't store the score (assumes afk)
            if cpm > 15:
                highscores = shelve.open('highscores', writeback=True)
                graphs = shelve.open('graphs', writeback=True) 

                test_id = ''
                if(self.test.get() == 0):
                    test_id = 'easy'
                elif(self.test.get() == 1):
                    test_id = 'advanced'
                elif(self.test.get() == 2):
                    test_id = 'nums'

                self.new_highscores = []
                self.retrieve_data(highscores, graphs, test_id)

                if(test_id != 'nums'):
                    self.new_highscores.append([wpm, '{}%'.format(accuracy), time.strftime('%d/%m/%Y')])
                    graphs[test_id].append(wpm)
                else:
                    self.new_highscores.append([cpm, '{}%'.format(accuracy), time.strftime('%d/%m/%Y')])
                    graphs[test_id].append(cpm)

                highscores[test_id] = sorted(self.new_highscores, reverse=True)[:10]

                graphs.close()
                highscores.close()

            self.entry.delete(0, tk.END)
            self.entry.config(state=tk.DISABLED)
            self.stop = True

    def retrieve_data(self, data_h, data_g, test_id):
        try:
            self.new_highscores = data_h[test_id]
            check_graph = data_g[test_id]
        except:
            data_h['easy'] = [[0, '0.00%', time.strftime('%d/%m/%Y')]] * 10
            data_h['advanced'] = [[0, '0.00%', time.strftime('%d/%m/%Y')]] * 10
            data_h['nums'] = [[0, '0.00%', time.strftime('%d/%m/%Y')]] * 10
            data_g['easy'] = []
            data_g['advanced'] = []
            data_g['highscores'] = []
            self.retrieve_data(data_h, data_g, test_id)

    def countup(self, count):
        if not self.start_count:
            return

        if not self.stop:
            self.time_or_wpm.set('{}'.format(math.ceil(count)))

            self.after(100, self.countup, count + 0.1)

            if count != 0:
                self.cur_wpm = int(self.right_chars * (60 / (count)) // 5)

                self.live_wpm.set('{} WPM'.format(self.cur_wpm))

                if round(count, 2).is_integer():
                    self.graph.clear()
                    self.xList.append(count)
                    self.yList.append(self.cur_wpm)

                    self.graph.set_title("Live WPM")

                    self.graph.plot(self.xList, self.yList)
                    self.canvas.show()

        if self.right_words + self.wrong_words >= len(self.wordbank):
            wpm = int(self.right_chars * (60 / count) // 5)
            total_chars = (self.right_chars + self.wrong_chars)

            if total_chars == 0:
                accuracy = 0.00
            else:
                accuracy = round((self.right_chars / total_chars) * 100, 2)

            self.time_or_wpm.set('WPM: {}'.format(wpm) + '   ' + 'Accuracy: {}%'.format(accuracy))

            self.entry.delete(0, tk.END)
            self.entry.config(state=tk.DISABLED)
            self.stop = True

    def on_key_press(self, event):
        if self.entry != self.entry.focus_get() or self.stop:
            return

        try:
            self.text.config(state=tk.NORMAL)

            # backspace
            if ord(event.char) == 8:
                self.remove_char()

            # space
            elif ord(event.char) == 32:
                # stops quick skipping over words while holding space
                if self.cur_letter == 0:
                    self.entry.delete(0, tk.END)
                else:
                    self.move_next_word()

            else:
                # if test timer hasn't started, start it
                if not self.start_count:
                    self.start_count = True
                    if self.test.get() != 3:
                        self.countdown(TIMER_LIMIT)
                    else:
                        self.countup(0)
                self.add_char(event.char)

                # if doing the num pad test, automatically move to next number
                if self.test.get() == 2:
                    self.move_next_word()

            self.text.config(state=tk.DISABLED)
        except:
            return

    def add_effect(self, typeOf):
        bank_index = self.cur_rand_nums[self.cur_word]
        self.text.tag_add(typeOf, '1.{}'.format(self.cur_char), '1.{}'.format(self.cur_char + len(self.wordbank[bank_index])))

    def remove_effect(self, typeOf):
        bank_index = self.cur_rand_nums[self.cur_word]
        self.text.tag_remove(typeOf, '1.{}'.format(self.cur_char), '1.{}'.format(self.cur_char + len(self.wordbank[bank_index])))

    def add_char(self, key):
        bank_index = self.cur_rand_nums[self.cur_word]

        if self.cur_letter < len(self.wordbank[bank_index]) and self.wordbank[bank_index][self.cur_letter] == key and self.wrong_letter == 0:
            self.remove_effect('current_wrong')
            self.add_effect('current_right')
        else:
            self.remove_effect('current_right')
            self.add_effect('current_wrong')
            self.wrong_letter += 1

        self.cur_letter += 1

    def remove_char(self):
        self.wrong_letter -= 1
        self.cur_letter -= 1

        if self.wrong_letter <= 0:
            self.remove_effect('current_wrong')
            self.add_effect('current_right')
            self.wrong_letter = 0

        if self.cur_letter <= 0:
            self.cur_letter = 0

    def move_next_word(self):
        bank_index = self.cur_rand_nums[self.cur_word]

        self.remove_effect('current_right')
        self.remove_effect('current_wrong')

        self.typing.set('')

        if self.wrong_letter == 0 and self.cur_letter >= len(self.wordbank[bank_index]):
            self.add_effect('right')
            self.right_words += 1
            self.right_cnt.set('Correct: {}'.format(self.right_words))
            self.right_chars += len(self.wordbank[bank_index]) + 1

            for letter in self.wordbank[bank_index]:
                # counts upper-case letters as two characters
                if letter.istitle():
                    self.right_chars += 1
        else:
            self.add_effect('wrong')
            self.wrong_words += 1

            # prevents spamming
            # this is especially true in the number test, as holding down any key would lead to 400+ CPM
            if self.wrong_words > TIMER_LIMIT * 5:
                self.entry.config(state=tk.DISABLED)
                self.stop = True

            self.wrong_cnt.set('Incorrect: {}'.format(self.wrong_words))
            self.wrong_chars += len(self.wordbank[bank_index]) + 1

            for letter in self.wordbank[bank_index]:
                if letter.istitle():
                    self.wrong_chars += 1

        self.cur_letter = 0
        self.wrong_letter = 0
        self.cur_char += len(self.wordbank[bank_index]) + 1
        self.cur_word += 1

        if self.cur_word >= len(self.cur_rand_nums):
            self.move_next_line()

        self.add_effect('current_right')

    def move_next_line(self):
        self.cur_rand_nums = list(self.nxt_rand_nums)

        self.cur_word = 0
        self.cur_char = 0

        self.text.delete('1.0', tk.END)

        for i in range(0, len(self.cur_rand_nums)):
            self.text.insert('end', self.wordbank[self.cur_rand_nums[i]] + ' ')

        if self.test.get() != 3:
            self.gen_nxt_line()
        elif self.cur_index < len(self.wordbank)-1:

            self.gen_nxt_line_custom(self.cur_index)
