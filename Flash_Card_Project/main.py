from tkinter import *
import pandas as pd
import random
BACKGROUND_COLOR = "#B1DDC6"
chosen = {}


# TODO: load the CSV file
try:
    data = pd.read_csv("data/words_to_learn.csv")
    # if data.empty:
    #     data = pd.read_csv("data/french_words.csv")
except FileNotFoundError:
    original_data = pd.read_csv("data/french_words.csv")
    learn_data = original_data.to_dict(orient="records")
else:
    learn_data = data.to_dict(orient="records")

def select_words():
    global  flip_timer,chosen
    window.after_cancel(flip_timer)
    chosen = random.choice(learn_data)
    flip_timer = window.after(3000, func=flip_card)
    canvas.itemconfig(Image, image=Front_img)
    canvas.itemconfig(title_txt, text="French", fill="black")
    canvas.itemconfig(text_item, text=chosen["French"], fill="black")


def flip_card():
    canvas.itemconfig(Image, image=Back_img)
    canvas.itemconfig(title_txt, text="English" , fill="white")
    canvas.itemconfig(text_item, text=chosen["English"], fill="white")

def is_known():
    learn_data.remove(chosen)
    print(len(learn_data))
    data = pd.DataFrame(learn_data)
    data.to_csv("data/words_to_learn.csv", index=False)
    select_words()


# TODO: Design the UI for the flash card
window = Tk()
window.title("Flash Card")
window.config(padx=25, pady=25,bg=BACKGROUND_COLOR)

flip_timer = window.after(3000,func=flip_card)
canvas = Canvas(height=526, width=800) # TODO: Create the Front Card logo
Front_img = PhotoImage(file="images\card_front.png")
Back_img = PhotoImage(file=fr"images\card_back.png")
Image = canvas.create_image(400,263,image=Front_img)
title_txt = canvas.create_text(400,150,text="Title",font=("Arial",40,"italic"))
text_item = canvas.create_text(400,263,text="Word",font=("Arial",60,"bold"))
select_words()
canvas.config(bg=BACKGROUND_COLOR,highlightthickness=0)
canvas.grid(row=0, column=0,columnspan=2)


# TODO: Create the Right logo
Right_img = PhotoImage(file=fr"images\right.png")
wrong_btn = Button(image=Right_img,bg=BACKGROUND_COLOR,highlightthickness=0, relief="flat", borderwidth=0, cursor="hand2",command=is_known)
wrong_btn.grid(row=1, column=1)


# TODO: Create the Wrong logo
Wrong_img = PhotoImage(file="images\wrong.png")
wrong_btn = Button(image=Wrong_img,bg=BACKGROUND_COLOR,highlightthickness=0, relief="flat", borderwidth=0, cursor="hand2",command=select_words)
wrong_btn.grid(row=1, column=0)


window.mainloop()