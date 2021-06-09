# ---------------------------- PASSWORD GENERATOR ------------------------------- #

import pyperclip
from tkinter import *
from tkinter import messagebox
import json

import random


def gen():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = []

    for char in range(nr_letters):
        password_list.append(random.choice(letters))

    for char in range(nr_symbols):
        password_list += random.choice(symbols)

    for char in range(nr_numbers):
        password_list += random.choice(numbers)

    random.shuffle(password_list)

    password = ""
    for char in password_list:
        password += char

    entry_password.delete(0, 'end')
    entry_password.insert(0, password)
    pyperclip.copy(password)



def search():
    website=entry_website.get().capitalize()
    try:
        with open('data.json', 'r') as f:
            # reading
            d = json.load(f)
    except FileNotFoundError:
        messagebox.showinfo(title='Error', message='No data found')
    else:

        if website in d:
            email=d[website]['email']
            password = d[website]['password']
            messagebox.showinfo(title=f'{website} email and password: ',
                                message=f"Email: {email} "
                                        f"\nPassword: {password}")
        else:
            messagebox.showinfo(title='Error', message= f'No details for {website} exists. ')


# ---------------------------- SAVE PASSWORD ------------------------------- #


def add():
    website = entry_website.get().capitalize()
    email = entry_email_uname.get()
    password = entry_password.get()

    if len(password) == 0 or len(website) == 0:
        return messagebox.showinfo(title="Error", message="Website/Password field is empty")

    is_ok = messagebox.askyesno(title=entry_website,
                                message=f"These are the details entered: \nEmail: {entry_email_uname.get()} "
                                        f"\nPassword: {entry_password.get()} \nOk to save?")

    new_data = {
        website: {
            'email': email,
            'password': password
        }
    }

    if is_ok:
        try:
            with open('data.json', 'r') as f:
                # reading
                d = json.load(f)
            if website in d:
                update = messagebox.askyesno("Warning", f"There is already a password saved for {website}.\n"
                                                        f"Would you like to overwrite?")
                if update:
                    d[website]["password"] = password
                    d[website]["email"] = email
                else:
                    return

        except FileNotFoundError:
            with open('data.json', 'w') as f:
                # saving
                json.dump(new_data, f, indent=4)
        else:
            # updating
            d.update(new_data)

            with open('data.json', 'w') as f:
                # saving
                json.dump(d, f, indent=4)
        finally:
            entry_website.delete(0, END)
            entry_password.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Generator")
window.config(padx=20, pady=20)

canvas = Canvas(width=200, height=200)
tomato_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=tomato_img)
canvas.grid(column=1, row=0)

label_website = Label(text="Website:")
label_website.grid(column=0, row=1)

entry_website = Entry()
entry_website.focus()
entry_website.grid(column=1, row=1, sticky="EW")

label_email_uname = Label(text="Email/Username:")
label_email_uname.grid(column=0, row=2)

entry_email_uname = Entry()
entry_email_uname.insert(0, "LoremIpsum@gmail.com")
entry_email_uname.grid(column=1, row=2, columnspan=2, sticky="EW")

label_password = Label(text="Password:")
label_password.grid(column=0, row=3)

entry_password = Entry()
entry_password.grid(column=1, row=3, sticky="EW")

generate_btn = Button(text="Generate Password", command=gen)
generate_btn.grid(column=2, row=3, sticky="EW")

add_btn = Button(text="Add", width=35, command=add)
add_btn.grid(column=1, row=4, columnspan=2, sticky="EW")

search_btn = Button(text="Search", command=search)
search_btn.grid(column=2, row=1, sticky="EW")

mainloop()
