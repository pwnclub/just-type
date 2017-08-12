from tkinter import *
from tkinter import ttk
from dictionary import words
import random
import time
import os
import math


class JustType(Frame):
    def __init__(self, parent):
        super().__init__()

        self.timer_limit = 30

        self.wordbank = words[0]
        self.cur_rand_nums = []
        self.nxt_rand_nums = []

        self.reset_variables()

        self.init_ui()

    def init_ui(self):
        self.typing = StringVar()
        self.right_cnt = StringVar()
        self.wrong_cnt = StringVar()
        self.time_or_wpm = StringVar()
        self.live_wpm = StringVar()
        self.test = IntVar()

        self.text = Text(self, font=("Courier", 20), width=50, height=2)
        self.entry = Entry(self, textvariable=self.typing, font=("Courier", 20), takefocus=0)
        self.right_word_label = Label(self, foreground='green', font=("Calibri", 15))
        self.wrong_word_label = Label(self, foreground='red', font=("Calibri", 15))
        self.countdown_label = Label(self, font=("Calibri", 15))
        self.live_wpm_label = Label(self, font=("Calibri", 15))
        self.reset_button = Button(self, text='Reset', command=self.reset)
        self.radio_easy = Radiobutton(self, text='Easy', variable=self.test, value=0, command=self.change_test)
        self.radio_advanced = Radiobutton(self, text='Advanced', variable=self.test, value=1, command=self.change_test)

        self.right_word_label['textvariable'] = self.right_cnt
        self.wrong_word_label['textvariable'] = self.wrong_cnt
        self.countdown_label['textvariable'] = self.time_or_wpm
        self.live_wpm_label['textvariable'] = self.live_wpm

        self.right_cnt.set('Correct: {}'.format(self.right_words))
        self.wrong_cnt.set('Incorrect: {}'.format(self.wrong_words))
        self.time_or_wpm.set('Type to start!')
        # TODO: fix live_wpm to not mess with the grid when it changes number of digits
        self.live_wpm.set('{} WPM'.format(self.cur_wpm))

        self.entry.focus_set()

        self.init_rand_gen()

        self.add_effect('current_right')
        self.text.config(state=DISABLED)

        self.text.tag_config('current_right', background='gray')
        self.text.tag_config('current_wrong', background='red')
        self.text.tag_config('right', foreground='green')
        self.text.tag_config('wrong', foreground='red')

        self.text.grid(column=0, row=0, columnspan=3)
        self.entry.grid(column=1 , row=1)
        self.reset_button.grid(column=2 , row=1)
        self.right_word_label.grid(column=1 , row=2)
        self.wrong_word_label.grid(column=1 , row=3)
        self.live_wpm_label.grid(column=2, row=3)
        self.countdown_label.grid(column=1 , row=4)
        self.radio_easy.grid(column=0 , row=1)
        self.radio_advanced.grid(column=0 , row=2)

        root.bind('<KeyPress>', self.on_key_press)

    def reset(self):
        self.text.config(state=NORMAL)
        self.reset_variables()
        self.init_rand_gen()
        self.text.config(state=DISABLED)
        self.entry.config(state=NORMAL)
        self.entry.delete(0, END)
        self.entry.focus_set()

        self.right_cnt.set('Correct: {}'.format(self.right_words))
        self.wrong_cnt.set('Incorrect: {}'.format(self.wrong_words))
        self.time_or_wpm.set('Type to start!')
        self.live_wpm.set('{} WPM'.format(self.cur_wpm))

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

        self.start_count = False
        self.stop = False

    def change_test(self):
        self.wordbank = words[self.test.get()]
        self.reset()

    def init_rand_gen(self):
        self.text.delete('1.0', END)
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

    def countdown(self, count):
        # prevents two timers from running at once
        if not self.start_count:
            return

        self.time_or_wpm.set('{}'.format(math.ceil(count)))

        if count > 0:
            self.after(100, self.countdown, count - 0.1)

            # stops from dividing by zero, which would lead to first letter being marked incorrect
            if count != self.timer_limit:
                self.cur_wpm = int(self.right_chars * (60 / (self.timer_limit - count)) // 5)

            self.live_wpm.set('{} WPM'.format(self.cur_wpm))
        else:
            wpm = int(self.right_chars * (60 / self.timer_limit) // 5)

            total_chars = (self.right_chars + self.wrong_chars)

            if total_chars == 0:
                accuracy = 0.00
            else:
                accuracy = round((self.right_chars / total_chars) * 100, 2)

            self.time_or_wpm.set('WPM: {}'.format(wpm) + '   ' + 'Accuracy: {}%'.format(accuracy))
            self.entry.delete(0, END)
            self.entry.config(state=DISABLED)
            self.stop = True

    def on_key_press(self, event):
        if self.entry != self.entry.focus_get() or self.stop:
            return

        try:
            self.text.config(state=NORMAL)

            # backspace
            if ord(event.char) == 8:
                self.remove_char()

            # space
            elif ord(event.char) == 32:
                if self.cur_letter == 0:
                    self.entry.delete(0, END)
                else:
                    self.move_next_word()

            elif (event.char).isalpha():
                # if test timer hasn't started, start it
                if not self.start_count:
                    self.start_count = True
                    self.countdown(self.timer_limit)
                self.add_char(event.char)

            self.text.config(state=DISABLED)
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

        self.entry.delete(0, END)

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

        self.text.delete('1.0', END)

        for i in range(0, len(self.cur_rand_nums)):
            self.text.insert('end', self.wordbank[self.cur_rand_nums[i]] + ' ')
        self.gen_nxt_line()

if __name__ == "__main__":
    root = Tk()
    JustType(root).pack()
    root.mainloop()
