import tkinter as tk
from dictionary import words
from operator import itemgetter
import random
import time
import os
import math
import shelve

class JustType(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack()

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for Page in (TestArea, HighScores):
            frame = Page(container, self)
            frame.grid(row=0, column=0, sticky="nsew")

            self.frames[Page] = frame

        self.show_frame(TestArea)

    def show_frame(self, tab):

        for frame in self.frames.values():
            frame.grid_remove()
        frame = self.frames[tab]
        frame.grid()
        if tab == HighScores:
            frame.update()
        
class TestArea(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)  

        self.timer_limit = 30

        self.wordbank = words[0]
        self.cur_rand_nums = []
        self.nxt_rand_nums = []

        self.reset_variables()

        self.init_ui(parent, controller)

    def init_ui(self, parent, controller):
        self.typing = tk.StringVar()
        self.right_cnt = tk.StringVar()
        self.wrong_cnt = tk.StringVar()
        self.time_or_wpm = tk.StringVar()
        self.live_wpm = tk.StringVar()
        self.test = tk.IntVar()

        self.text = tk.Text(self, font=("Courier", 20), width=50, height=2)
        self.entry = tk.Entry(self, textvariable=self.typing, font=("Courier", 20), takefocus=0)
        self.right_word_label = tk.Label(self, foreground='green', font=("Calibri", 15))
        self.wrong_word_label = tk.Label(self, foreground='red', font=("Calibri", 15))
        self.countdown_label = tk.Label(self, font=("Calibri", 15))
        self.live_wpm_label = tk.Label(self, width=8, font=("System", 15))
        self.reset_button = tk.Button(self, text='Reset', font='System', padx=15, pady=5, background='red', foreground='white', command=self.reset)
        self.radio_easy = tk.Radiobutton(self, text='Easy', font='System', variable=self.test, value=0, command=self.change_test)
        self.radio_advanced = tk.Radiobutton(self, text='Advanced', font='System', variable=self.test, value=1, command=self.change_test)
        self.radio_nums = tk.Radiobutton(self, text='Numbers', font='System', variable=self.test, value=2, command=self.change_test)
        self.open_hs_button = tk.Button(self, text='High Scores', command=lambda: [self.reset(), controller.show_frame(HighScores)])

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
        self.entry.grid(column=1 , row=1)
        self.reset_button.grid(column=2 , row=1, pady=5)
        self.right_word_label.grid(column=1 , row=2, pady=5)
        self.wrong_word_label.grid(column=1 , row=3, pady=5)
        self.live_wpm_label.grid(column=2, row=3)
        self.countdown_label.grid(column=1 , row=4)
        self.radio_easy.grid(column=0 , row=1, sticky='w')
        self.radio_advanced.grid(column=0, row=2, sticky='w')
        self.radio_nums.grid(column=0, row=3, sticky='w')
        self.open_hs_button.grid(column=0, row=4)

        controller.bind('<KeyPress>', self.on_key_press)

    def reset(self):
        self.text.config(state=tk.NORMAL)
        self.reset_variables()
        self.init_rand_gen()
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

        self.start_count = False
        self.stop = False

    def change_test(self):
        self.wordbank = words[self.test.get()]
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

                if self.test.get() == 2:
                    self.cur_cpm =  int(self.right_chars * (60/ (self.timer_limit - count)))

            if self.test.get() == 2: 
                self.live_wpm.set('{} CPM'.format(self.cur_cpm))
            else:
                self.live_wpm.set('{} WPM'.format(self.cur_wpm))
        else:
            wpm = int(self.right_chars * (60 / self.timer_limit) // 5)
            cpm = int(self.right_chars * (60 / self.timer_limit))

            total_chars = (self.right_chars + self.wrong_chars)

            if total_chars == 0:
                accuracy = 0.00
            else:
                accuracy = round((self.right_chars / total_chars) * 100, 2)

            if self.test.get() == 2:
                self.time_or_wpm.set('CPM: {}'.format(cpm) + '   ' + 'Accuracy: {}%'.format(accuracy))
            else:
                self.time_or_wpm.set('WPM: {}'.format(wpm) + '   ' + 'Accuracy: {}%'.format(accuracy))

            highscores = shelve.open('highscores', writeback=True)

            test_id = ''

            if(self.test.get() == 0):
                test_id = 'easy'
            elif(self.test.get() == 1):
                test_id = 'advanced'
            elif(self.test.get() == 2):
                test_id = 'nums'

            if(test_id != 'nums'):
                highscores[test_id].append([wpm, '{}%'.format(accuracy), time.strftime("%d/%m/%Y")])
            else:
                highscores[test_id].append([cpm, '{}%'.format(accuracy), time.strftime("%d/%m/%Y")])

            highscores[test_id] = sorted(highscores[test_id], reverse=True)[:10]
            highscores.sync()
            highscores.close()

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

            elif (event.char).isalpha() or (event.char).isdigit():
                # if test timer hasn't started, start it
                if not self.start_count:
                    self.start_count = True
                    self.countdown(self.timer_limit)
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
            if self.wrong_words > self.timer_limit * 5:
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
        self.gen_nxt_line()


class HighScores(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.highscores_list = tk.StringVar()
        self.test = tk.IntVar()

        self.highscores_label = tk.Label(self, justify="left", width=50)
        self.return_button = tk.Button(self, text="Back to Testing Area", command=lambda: controller.show_frame(TestArea))
        self.reset_scores_button = tk.Button(self, font='System', padx=15, pady=5, background='red', foreground='white', text="RESET", command=self.reset_scores)
        self.radio_easy = tk.Radiobutton(self, text='Easy', font='System', command=self.update, variable=self.test, value=0)
        self.radio_advanced = tk.Radiobutton(self, text='Advanced', font='System', command=self.update, variable=self.test, value=1)
        self.radio_nums = tk.Radiobutton(self, text='Numbers', font='System', command=self.update, variable=self.test, value=2)

        self.highscores_label['textvariable'] = self.highscores_list

        self.highscores_label.grid(column=1, row=0, columnspan=2, rowspan=4)
        self.return_button.grid(column=0, row=4)
        self.reset_scores_button.grid(column=1, row=4, sticky="e")
        self.radio_easy.grid(column=0 , row=0, sticky='w')
        self.radio_advanced.grid(column=0, row=1, sticky='w')
        self.radio_nums.grid(column=0, row=2, sticky='w')

    def update(self):
        highscores = shelve.open('highscores')
        string = ''

        if(self.test.get() == 0):
            test_id = 'easy'
        elif(self.test.get() == 1):
            test_id = 'advanced'
        elif(self.test.get() == 2):
            test_id = 'nums'

        for i in range (1, 11):
            string += str(i) + '. ' + str(highscores[test_id][i-1][0])
            if(test_id != 'nums'):
                string += ' WPM '
            else:
                string += ' CPM '
            string += '\t' + str(highscores[test_id][i-1][1]) + '\t' + str(highscores[test_id][i-1][2]) + '\n'

        self.highscores_list.set(string)

        highscores.close()

    def reset_scores(self):
        highscores = shelve.open('highscores')

        if(self.test.get() == 0):
            test_id = 'easy'
        elif(self.test.get() == 1):
            test_id = 'advanced'
        elif(self.test.get() == 2):
            test_id = 'nums'

        highscores[test_id] = [[0, '0.00%', time.strftime("%d/%m/%Y")]] * 10
        highscores.sync()
        highscores.close()
        self.update()

if __name__ == "__main__":      
    root = JustType()
    root.resizable(width=False, height=False)
    root.mainloop()
