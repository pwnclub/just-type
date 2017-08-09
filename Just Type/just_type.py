from tkinter import *
from tkinter import ttk
import random

wordbank = ['the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'I', 'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do']
random_nums = [0, 0, 0, 0, 0, 0, 0, 0]

num_words_display = 8

cur_char = 0
cur_letter = 0
wrong_letter = 0
cur_word = 0
right = True

def onKeyPress(event):

    text.config(state=NORMAL)
    
    global cur_char
    global cur_letter
    global wrong_letter
    global cur_word
    global right
    
    #print(event.char)
    #print(cur_char)
    #print(ord(event.char))
    print(wrong_letter)

    if (ord(event.char) == 8):
        wrong_letter -= 1
        cur_letter -= 1
        if (wrong_letter <= 0):
            text.tag_remove('current_wrong', '1.%s' % (cur_char), '1.%s' % (cur_char + len(wordbank[random_nums[cur_word]])))
            text.tag_add('current_correct', '1.%s' % (cur_char), '1.%s' % (cur_char + len(wordbank[random_nums[cur_word]])))
            wrong_letter = 0
        if (cur_letter <= 0):
            cur_letter = 0
        right = True
        return

    try:
        if (ord(event.char) == 32):
            
            #print(len(wordbank[random_nums[cur_word]]))
            #print(cur_letter)
            
            if right:
                text.tag_remove('current_correct', '1.%s' % (cur_char), '1.%s' % (cur_char + len(wordbank[random_nums[cur_word]])))
                if cur_letter < len(wordbank[random_nums[cur_word]]):
                    text.tag_add('wrong', '1.%s' % (cur_char), '1.%s' % (cur_char + len(wordbank[random_nums[cur_word]])))
                else:
                    text.tag_add('correct', '1.%s' % (cur_char), '1.%s' % (cur_char + len(wordbank[random_nums[cur_word]])))
            else:
                text.tag_remove('current_wrong', '1.%s' % (cur_char), '1.%s' % (cur_char + len(wordbank[random_nums[cur_word]])))
                text.tag_add('wrong', '1.%s' % (cur_char), '1.%s' % (cur_char + len(wordbank[random_nums[cur_word]])))

            cur_letter = 0
            wrong_letter = 0
            cur_char += len(wordbank[random_nums[cur_word]]) + 1
            cur_word += 1

            right = True
            
            if cur_word >= len(random_nums):
                cur_word = 0
                cur_char = 0
                text.delete('1.0', END)
                for i in range(0, num_words_display):
                    random_num = random.randint(0, len(wordbank)-1)
                    random_nums[i] = random_num
                    text.insert('insert', wordbank[random_num] + ' ')

            text.config(state=DISABLED)
            return
        
        if cur_letter < len(wordbank[random_nums[cur_word]]) and wordbank[random_nums[cur_word]][cur_letter] == event.char and right:
            if cur_letter > 0:
                text.tag_remove('current_wrong', '1.%s' % (cur_char), '1.%s' % (cur_char + len(wordbank[random_nums[cur_word]])))
            text.tag_add('current_correct', '1.%s' % (cur_char), '1.%s' % (cur_char + len(wordbank[random_nums[cur_word]])))
        else:
            if cur_letter > 0:
                text.tag_remove('current_correct', '1.%s' % (cur_char), '1.%s' % (cur_char + len(wordbank[random_nums[cur_word]])))
            text.tag_add('current_wrong', '1.%s' % (cur_char), '1.%s' % (cur_char + len(wordbank[random_nums[cur_word]])))
            wrong_letter += 1
            right = False
    except:
        text.config(state=DISABLED)
        return
            
        
    cur_letter += 1

    text.config(state=DISABLED)

root = Tk()
text = Text(root, width=40, height=0)

for i in range(0, num_words_display):
        random_num = random.randint(0, len(wordbank)-1)
        random_nums[i] = random_num
        text.insert('insert', wordbank[random_num] + ' ')

text.config(state=DISABLED)

text.tag_config('current_correct', background='gray')
text.tag_config('current_wrong', background='red')
text.tag_config('correct', foreground='green')
text.tag_config('wrong', foreground='red')

text.pack()
root.bind('<KeyPress>', onKeyPress)

root.mainloop()
