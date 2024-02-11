from tkinter import *
from tkinter import messagebox
import json
import random

alphabet = ["A", "B", "C", "D", "E", "D", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
            "U", "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o",
            "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
symbols = ["~", "`", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "-", "+", "=", "{", "[", "}", "]", "|",
           "\\", ":", ";", "'", "<", ",", ">", ".", "?", "/"]
numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]


# ---------------------------- Data Search ------------------------------- #
def search_data():
    password_entry.delete(0, END)
    email_entry.delete(0, END)
    website = website_entry.get().lower()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Oops", message="File not found.")
    else:
        if website in data:
            password = data[website]["password"]
            email = data[website]["email"]
            password_entry.insert(0, password)
            email_entry.insert(0, email)
        else:
            messagebox.showinfo(title="Oops", message="Website not found.")


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def password_generator():
    password_entry.delete(0, END)
    password = ""
    for _ in range(random.randint(8, 16)):
        random_variable = random.choices([alphabet, symbols, numbers], weights=[4, 2, 1], k=1)[0]
        password += random.choice(random_variable)
    password_entry.insert(0, password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    website = website_entry.get().lower()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }
    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty.")
    else:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file) # TODO:  load the already existed data
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data) # TODO: Update the value by adding the new data
            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4) # TODO: storing the data inside the json file
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(height=200, width=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# Labels
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)
email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)
password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

# Entries
website_entry = Entry(width=21)
website_entry.grid(row=1, column=1)
website_entry.focus()
email_entry = Entry(width=39)
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(0, "your_email@gmail.com")
password_entry = Entry(width=21)
password_entry.grid(row=3, column=1, columnspan=1)

# Buttons
search_button = Button(text="Search", width=15, command=search_data)
search_button.grid(row=1, column=2)
generate_password_button = Button(text="Generate Password", width=15, command=password_generator)
generate_password_button.grid(row=3, column=2)
add_button = Button(text="Add", width=36, command=save_password)
add_button.grid(row=4, column=1, columnspan=2)

window.mainloop()
