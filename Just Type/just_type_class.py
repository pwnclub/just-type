from tkinter import *
from tkinter import ttk
import random
import time
import os

class MyWindow(Frame):

    def __init__(self, parent):
        
        Frame.__init__(self, parent)

        self.num_words_display = 12     # each line displays this many words TODO: replace this with num of chars
        self.timer_limit = 10           # duration of test

        self.wordbank = ['the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'I', 'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do']
        self.cur_random_nums = [0]*self.num_words_display   # first line displayed
        self.next_random_nums = [0]*self.num_words_display  # second line

        self.cur_char = 0
        self.cur_letter = 0
        self.wrong_letter = 0
        self.cur_word = 0
        self.correct_words = 0
        self.correct_chars = 0
        self.wrong_words = 0
        self.wrong_chars = 0

        self.startCount = False

        self.typing = StringVar()
        self.correct_word_amount = StringVar()
        self.wrong_word_amount = StringVar()
        self.time_or_wpm = StringVar()

        self.text = Text(self, width=50, height=2)
        self.entry = Entry(self, textvariable=self.typing, takefocus=0)
        self.correct_word_label = Label(self, foreground='green')
        self.wrong_word_label = Label(self, foreground='red')
        self.countdown_label = Label(self)

        self.correct_word_label['textvariable'] = self.correct_word_amount
        self.wrong_word_label['textvariable'] = self.wrong_word_amount
        self.countdown_label['textvariable'] = self.time_or_wpm

        self.correct_word_amount.set('Correct: {}'.format(self.correct_words))
        self.wrong_word_amount.set('Incorrect: {}'.format(self.wrong_words))
        self.time_or_wpm.set('Type to start!')

        self.entry.focus_set()

        for i in range(0, self.num_words_display):
            random_num = random.randint(0, len(self.wordbank)-1)
            self.cur_random_nums[i] = random_num
            
            self.text.insert('end', self.wordbank[random_num] + ' ')
            
        self.text.insert('end', '\n')

        for i in range(0, self.num_words_display): 
            random_num = random.randint(0, len(self.wordbank)-1)
            self.next_random_nums[i] = random_num
            
            self.text.insert('end', self.wordbank[random_num] + ' ')

        self.addEffect('current_correct')
        self.text.config(state=DISABLED)

        self.text.tag_config('current_correct', background='gray')
        self.text.tag_config('current_wrong', background='red')
        self.text.tag_config('correct', foreground='green')
        self.text.tag_config('wrong', foreground='red')

        self.text.pack()
        self.entry.pack()
        self.correct_word_label.pack()
        self.wrong_word_label.pack()
        self.countdown_label.pack()
        
        root.bind('<KeyPress>', self.onKeyPress)

    def countdown(self, count):

        self.time_or_wpm.set('{}'.format(count))

        if count > 0:
            self.after(1000, self.countdown, count-1)
        else:
            wpm = int(self.correct_chars // 5 * (60 / self.timer_limit))
            self.time_or_wpm.set('WPM: {}'.format(wpm))
            #os.execl(sys.executable, sys.executable, *sys.argv)

    def onKeyPress(self, event):

        if self.entry != self.entry.focus_get():
            return

        if self.startCount == False:    # if test timer hasn't started, start it
            self.startCount = True
            self.countdown(self.timer_limit)
            
        self.text.config(state=NORMAL)

        bank_index = self.cur_random_nums[self.cur_word]

        try:
            if (ord(event.char) == 8):  # backspace

                self.wrong_letter -= 1
                self.cur_letter -= 1
                
                if (self.wrong_letter <= 0):
                    self.removeEffect('current_wrong')
                    self.addEffect('current_correct')
                    self.wrong_letter = 0
                    
                if (self.cur_letter <= 0):
                    self.cur_letter = 0
                    
                self.text.config(state=DISABLED)
                return
            
            if (ord(event.char) == 32): # space
                self.removeEffect('current_correct')
                self.removeEffect('current_wrong')

                self.entry.delete(0, END)
                
                if self.wrong_letter == 0 and self.cur_letter >= len(self.wordbank[bank_index]):
                    self.addEffect('correct')
                    self.correct_words += 1
                    self.correct_word_amount.set('Correct: {}'.format(self.correct_words))
                    self.correct_chars += len(self.wordbank[bank_index])
                else:
                    self.addEffect('wrong')
                    self.wrong_words += 1
                    self.wrong_word_amount.set('Incorrect: {}'.format(self.wrong_words))
                    self.wrong_chars += len(self.wordbank[bank_index])
                
                self.cur_letter = 0
                self.wrong_letter = 0
                
                self.cur_char += len(self.wordbank[bank_index]) + 1
                self.cur_word += 1
                
                if self.cur_word >= len(self.cur_random_nums): 
                    self.moveNextLine()

                self.text.config(state=DISABLED)
                self.addEffect('current_correct')
                return
            
            if self.cur_letter < len(self.wordbank[bank_index]) and self.wordbank[bank_index][self.cur_letter] == event.char and self.wrong_letter == 0:
                self.removeEffect('current_wrong')
                self.addEffect('current_correct')
            else:
                self.removeEffect('current_correct')
                self.addEffect('current_wrong')
                self.wrong_letter += 1

            self.cur_letter += 1
        except: 
            return
        finally:
            self.text.config(state=DISABLED)

    def addEffect(self, typeOf):
        bank_index = self.cur_random_nums[self.cur_word] 
        self.text.tag_add(typeOf, '1.{}'.format(self.cur_char), '1.{}'.format(self.cur_char + len(self.wordbank[bank_index])))

    def removeEffect(self, typeOf):
        bank_index = self.cur_random_nums[self.cur_word]
        self.text.tag_remove(typeOf, '1.{}'.format(self.cur_char), '1.{}'.format(self.cur_char + len(self.wordbank[bank_index])))

    def moveNextLine(self):

        self.cur_random_nums = list(self.next_random_nums)
        
        self.cur_word = 0
        self.cur_char = 0
        
        self.text.delete('1.0', END)
        
        for i in range(0, self.num_words_display):
            self.text.insert('end', self.wordbank[self.cur_random_nums[i]] + ' ')
            
        self.text.insert('end', '\n')
        
        for i in range(0, self.num_words_display):
            random_num = random.randint(0, len(self.wordbank)-1)
            self.next_random_nums[i] = random_num
            
            self.text.insert('end', self.wordbank[random_num] + ' ')
        
root = Tk()

MyWindow(root).pack()

root.mainloop()