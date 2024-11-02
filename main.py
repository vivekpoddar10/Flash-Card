from operator import index
from tkinter import *
import pandas
from random import choice

from pandas.core.window import Window

BACKGROUND_COLOR = "#B1DDC6"
#------------------------------------- Reading data from CSV file ---------------------------------
try:
    data_set = pandas.read_csv('./data/words_to_learn.csv')
except FileNotFoundError:
    data_set = pandas.read_csv('./data/french_words.csv')

data = data_set.to_dict(orient='records')
current_card = {}
#--------------------------------- finding english word -------------------------------------------
def flip_card():
    # changing the background image
    canvas.itemconfig(canvas_image, image = back_image)

    # changing the font color of title and word
    canvas.itemconfig(title_text, text = 'English' ,fill='white')

    # finding the English word for respective French word and updating it on the screen
    canvas.itemconfig(word_text, text = current_card['English'], fill='white')


#------------------------------------ Guessing new word ------------------------------------------
def new_card():
    global current_card, flip_timer
    current_card = choice(data)
    window.after_cancel(flip_timer)

    # change the background image
    canvas.itemconfig(canvas_image, image = front_image)
    # change title text, font color
    canvas.itemconfig(title_text, text = 'French', fill = 'black')
    # change word text to French word, font color
    canvas.itemconfig(word_text, text = current_card['French'], fill = 'black')

    flip_timer = window.after(3000, func=flip_card)

#----------------------------------- storing the words to learn --------------------------------
def words_to_learn():
    data.remove(current_card)
    df = pandas.DataFrame(data)
    df.to_csv('./data/words_to_learn.csv', index = False)


#----------------------------------- UI Setup ---------------------------------------------------

window = Tk()
window.title('Flash Card')
window.config(padx=50, pady=10, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, func=new_card)

canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
front_image = PhotoImage(file='./images/card_front.png')
back_image = PhotoImage(file='./images/card_back.png')
canvas_image = canvas.create_image(400, 263, image = front_image)
title_text = canvas.create_text(400, 150, text = '', font=('aerial', 40, 'italic'))
word_text = canvas.create_text(400, 263, text = '', font=('aerial', 60, 'bold'))
canvas.grid(row = 0, column = 0, columnspan = 2)

wrong_image = PhotoImage(file='./images/wrong.png')
wrong_btn = Button(image=wrong_image, highlightthickness=0, bg=BACKGROUND_COLOR, command=new_card)
wrong_btn.grid(row = 1, column = 0)

right_image = PhotoImage(file='./images/right.png')
right_btn = Button(image=right_image, highlightthickness=0, bg=BACKGROUND_COLOR, command=words_to_learn)
right_btn.grid(row=1, column = 1)


#----------------------------------- Updating the screen -----------------------------------------
new_card()

window.mainloop()