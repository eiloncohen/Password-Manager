from tkinter import *
from tkinter import messagebox
import random
import string
import pyperclip

characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generatePassword():
    global password_entry

    password_entry.delete(0, END)  # deletes the current value

    # shuffling the characters
    random.shuffle(characters)

    # picking random characters from the list
    password = []
    for i in range(21):
        password.append(random.choice(characters))

    # shuffling the resultant password
    random.shuffle(password)

    # convert the list to string and remove spaces
    password_string = ''.join(password)
    password_string.replace(" ", "")

    # set the password in password entry
    password_entry.insert(0, password_string)

    # copy the password to clipboard automatically
    pyperclip.copy(password_string)


# ---------------------------- SAVE PASSWORD ------------------------------- #

def delete_entries():
    password_entry.delete(0, END)
    website_entry.delete(0, END)


def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    if website and password:
        is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered: \nEmail: {email}"
                                                              f"\nPassword: {password} "
                                                              f"\n \n Is it ok to save?")
        if is_ok:
            info_str = f"website: {website} | username: {email} | password:{password} \n"
            with open("password.txt", "a") as passwords_file:
                passwords_file.write(info_str)
                delete_entries()
            passwords_file.close()
        else:
            delete_entries()

    elif not website:
        messagebox.showwarning(title="Alert", message="Missing website")
    else:
        messagebox.showwarning(title="Alert", message="Missing password")


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
website_entry = Entry(width=35)
website_entry.grid(row=1, column=1, columnspan=2)
website_entry.focus()
email_entry = Entry(width=35)
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(0,"eiloncohen20@gmail.com")
password_entry = Entry(width=21)
password_entry.grid(row=3, column=1)

# Buttons
generate_password_button = Button(text="Generate Pass", width=11, command=generatePassword)
generate_password_button.grid(row=3, column=2)
add_button = Button(text="Add", width=34, command=save)
add_button.grid(row=4, column=1, columnspan=2)

window.mainloop()


