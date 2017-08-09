from tkinter import *
from tkinter import ttk
import random

num_words_display = 12

wordbank = ['the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'I', 'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do']
cur_random_nums = [0]*num_words_display
next_random_nums = [0]*num_words_display

cur_char = 0
cur_letter = 0
wrong_letter = 0
cur_word = 0
correct_words = 0
correct_chars = 0
wrong_words = 0
wrong_chars = 0

def onKeyPress(event):
    global cur_char
    global cur_letter
    global wrong_letter
    global cur_word
    global cur_random_nums
    global next_random_nums
    global correct_words
    global correct_chars
    global wrong_words 
    global wrong_chars 

    if entry != entry.focus_get():
        return

    text.config(state=NORMAL)

    bank_index = cur_random_nums[cur_word]

    try:
        if (ord(event.char) == 8):
            
            wrong_letter -= 1
            cur_letter -= 1
            
            if (wrong_letter <= 0):
                removeEffect('current_wrong')
                addEffect('current_correct')
                wrong_letter = 0
                
            if (cur_letter <= 0):
                cur_letter = 0
                
            text.config(state=DISABLED)
            return
        
        if (ord(event.char) == 32):
            removeEffect('current_correct')
            removeEffect('current_wrong')

            entry.delete(0, END)
            
            if wrong_letter == 0 and cur_letter >= len(wordbank[bank_index]):
                addEffect('correct')
                correct_words += 1
                correct_chars += len(wordbank[bank_index])
            else:
                addEffect('wrong')
                wrong_words += 1
                wrong_chars += len(wordbank[bank_index])
            
            print('Correct Words Typed: ', correct_words)
            print('Correct Characters Typed: ', correct_chars)
            print('Wrong Words Typed: ', wrong_words)
            print('Wrong Characters Typed: ', wrong_chars)
            
            cur_letter = 0
            wrong_letter = 0
            
            cur_char += len(wordbank[bank_index]) + 1
            cur_word += 1
            
            if cur_word >= len(cur_random_nums): 
                moveNextLine()

            addEffect('current_correct')
            text.config(state=DISABLED)
            return
        
        if cur_letter < len(wordbank[bank_index]) and wordbank[bank_index][cur_letter] == event.char and wrong_letter == 0:
            removeEffect('current_wrong')
            addEffect('current_correct')
        else:
            removeEffect('current_correct')
            addEffect('current_wrong')
            wrong_letter += 1

        cur_letter += 1
    except:
        return
    finally:
        text.config(state=DISABLED)

def addEffect(typeOf):
    global cur_char
    bank_index = cur_random_nums[cur_word] 
    text.tag_add(typeOf, '1.%s' % (cur_char), '1.%s' % (cur_char + len(wordbank[bank_index])))

def removeEffect(typeOf):
    global cur_char
    bank_index = cur_random_nums[cur_word]
    text.tag_remove(typeOf, '1.%s' % (cur_char), '1.%s' % (cur_char + len(wordbank[bank_index])))

def moveNextLine():
    global cur_char
    global cur_word
    global cur_random_nums
    global next_random_nums
    
    cur_random_nums = list(next_random_nums)
    
    cur_word = 0
    cur_char = 0
    
    text.delete('1.0', END)
    
    for i in range(0, num_words_display):
        text.insert('end', wordbank[cur_random_nums[i]] + ' ')
        
    text.insert('end', '\n')
    
    for i in range(0, num_words_display):
        random_num = random.randint(0, len(wordbank)-1)
        next_random_nums[i] = random_num
        
        text.insert('end', wordbank[random_num] + ' ')
        
root = Tk()
typing = StringVar()

text = Text(root, width=50, height=2)
entry = Entry(root, textvariable=typing, takefocus=0)

entry.focus_set()

for i in range(0, num_words_display):
    random_num = random.randint(0, len(wordbank)-1)
    cur_random_nums[i] = random_num
    
    text.insert('end', wordbank[random_num] + ' ')
    
text.insert('end', '\n')

for i in range(0, num_words_display): 
    random_num = random.randint(0, len(wordbank)-1)
    next_random_nums[i] = random_num
    
    text.insert('end', wordbank[random_num] + ' ')

addEffect('current_correct')
text.config(state=DISABLED)

text.tag_config('current_correct', background='gray')
text.tag_config('current_wrong', background='red')
text.tag_config('correct', foreground='green')
text.tag_config('wrong', foreground='red')

text.pack()
entry.pack()
root.bind('<KeyPress>', onKeyPress)

root.mainloop()

