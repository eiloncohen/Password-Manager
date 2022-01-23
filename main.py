from tkinter import *
from tkinter import messagebox
import random
import string
import pyperclip
import json

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


def find_user_and_pass():
    website_to_search = website_entry.get().capitalize()
    try:
        with open("data.json", 'r') as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="file Data doesnt exist")
    else:
        found_data = {key for key in data.keys() if key == website_to_search}
        if len(found_data) == 1:
            messagebox.showinfo(title=website_to_search, message=f"Email: {data[website_to_search]['email']}"
                                                                 f"\nPassword: {data[website_to_search]['password']} ")
        else:
            messagebox.showinfo(title=website_to_search, message="email and password not found")

# ---------------------------- SAVE PASSWORD ------------------------------- #


def delete_entries():
    password_entry.delete(0, END)
    website_entry.delete(0, END)


def save():
    website = website_entry.get().capitalize()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            'email': email,
            'password': password,
        }
    }

    if website and password:
        is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered: \nEmail: {email}"
                                                              f"\nPassword: {password} "
                                                              f"\n \n Is it ok to save?")
        if is_ok:
            try:
                with open("data.json", "r") as data_file:
                    # enter json file to dict obj / reading old data
                    data = json.load(data_file)
            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                # updating old data with new data
                data.update(new_data)
                # saving updated data
                with open("data.json", "w") as data_file:
                    json.dump(data, data_file, indent=4)
            finally:
                delete_entries()
                data_file.close()
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
website_entry = Entry(width=21)
website_entry.grid(row=1, column=1)
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
search_btn = Button(text="Search", width=11, command=find_user_and_pass)
search_btn.grid(row=1, column=2, columnspan=2)

window.mainloop()


