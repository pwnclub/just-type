from tkinter import *
from tkinter import ttk
from dictionary import easy_words
import random
import time
import os


class just_type(Frame):
    def __init__(self, parent):
        super().__init__()

        self.num_words_display = 12
        self.timer_limit = 60

        self.wordbank = easy_words
        self.cur_rand_nums = []
        self.nxt_rand_nums = []

        self.cur_char = 0
        self.cur_letter = 0
        self.wrong_letter = 0
        self.cur_word = 0
        self.right_words = 0
        self.right_chars = 0
        self.wrong_words = 0
        self.wrong_chars = 0

        self.start_count = False

        self.init_ui()

    def init_ui(self):
        self.typing = StringVar()
        self.right_cnt = StringVar()
        self.wrong_cnt = StringVar()
        self.time_or_wpm = StringVar()

        self.text = Text(self, width=90, height=2)
        self.entry = Entry(self, textvariable=self.typing, takefocus=0)
        self.right_word_label = Label(self, foreground='green')
        self.wrong_word_label = Label(self, foreground='red')
        self.countdown_label = Label(self)

        self.right_word_label['textvariable'] = self.right_cnt
        self.wrong_word_label['textvariable'] = self.wrong_cnt
        self.countdown_label['textvariable'] = self.time_or_wpm

        self.right_cnt.set('Correct: {}'.format(self.right_words))
        self.wrong_cnt.set('Incorrect: {}'.format(self.wrong_words))
        self.time_or_wpm.set('Type to start!')

        self.entry.focus_set()

        self.init_rand_gen()

        self.add_effect('current_right')
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

        root.bind('<KeyPress>', self.on_key_press)

    def init_rand_gen(self):
        for i in range(0, self.num_words_display):
            random_num = random.randint(0, len(self.wordbank) - 1)
            self.cur_rand_nums.append(random_num)

            self.text.insert('end', self.wordbank[random_num] + ' ')

        self.gen_nxt_line()

    def gen_nxt_line(self):
        del self.nxt_rand_nums[:]

        self.text.insert('end', '\n')

        for i in range(0, self.num_words_display):
            random_num = random.randint(0, len(self.wordbank) - 1)
            self.nxt_rand_nums.append(random_num)

            self.text.insert('end', self.wordbank[random_num] + ' ')

    def countdown(self, count):
        self.time_or_wpm.set('{}'.format(count))

        if count > 0:
            self.after(1000, self.countdown, count-1)
        else:
            wpm = int(self.right_chars // 5 * (60 / self.timer_limit))
            self.time_or_wpm.set('WPM: {}'.format(wpm))

    def on_key_press(self, event):
        if self.entry != self.entry.focus_get():
            return

        try:
            self.text.config(state=NORMAL)

            if ord(event.char) == 8:        # backspace
                self.remove_char()

            elif ord(event.char) == 32:     # space
                self.move_next_word()

            elif (event.char).isalpha():
                if not self.start_count:    # if test timer hasn't started, start it
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
            self.right_chars += len(self.wordbank[bank_index])
        else:
            self.add_effect('wrong')
            self.wrong_words += 1
            self.wrong_cnt.set('Incorrect: {}'.format(self.wrong_words))
            self.wrong_chars += len(self.wordbank[bank_index])

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

root = Tk()

just_type(root).pack()

root.mainloop()
