from tkinter import *
import requests
quote = ""
def txt():
    global quote
    response = requests.get(url="https://api.kanye.rest/")
    data = response.json()
    quote = data["quote"]

def update_quote():
    txt()
    canvas.itemconfig(quote_txt, text=quote)

txt()
window = Tk()
window.title("Kanya Say Quotes")
window.config(padx=25, pady=25)


canvas = Canvas(height=414, width=300)
img = PhotoImage(file="background.png")
canvas.create_image(150,207,image=img)
quote_txt = canvas.create_text(150,207,text=quote,width=250,font=("Arial",20,"italic"))

canvas.config(highlightthickness=0)
canvas.grid(row=0, column=0)


kanya_img = PhotoImage(file="kanye.png")
wrong_btn = Button(image=kanya_img,highlightthickness=0, relief="flat", borderwidth=0, command=update_quote)
wrong_btn.grid(row=1, column=0)


window.mainloop()