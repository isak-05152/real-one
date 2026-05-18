from tkinter import *
from tkinter import messagebox

# ---------------- WINDOW ---------------- #
window = Tk()
window.title("Password Manager")
window.geometry("900x700")
window.config(bg="#efefef")

# ---------------- FUNCTIONS ---------------- #
show_password = False


def toggle_password():
    global show_password

    if show_password:
        password_entry.config(show="*")
        confirm_entry.config(show="*")
        enter_entry.config(show="*")
        eye_btn.config(text="👁")
        show_password = False
    else:
        password_entry.config(show="")
        confirm_entry.config(show="")
        enter_entry.config(show="")
        eye_btn.config(text="🙈")
        show_password = True


def create_password():
    password = password_entry.get()
    confirm = confirm_entry.get()

    if len(password) < 8:
        messagebox.showerror(
            "Error",
            "Password must contain at least 8 characters"
        )

    elif password != confirm:
        messagebox.showerror(
            "Error",
            "Passwords do not match"
        )

    else:
        messagebox.showinfo(
            "Success",
            "Master Password Created Successfully"
        )


# ---------------- TOP SECTION ---------------- #
title1 = Label(
    window,
    text="SET MASTER PASSWORD",
    font=("Times New Roman", 22),
    bg="#efefef",
    fg="black"
)
title1.pack(pady=(50, 20))

# Password Entry
password_frame = Frame(window, bg="#efefef")
password_frame.pack(pady=10)

password_entry = Entry(
    password_frame,
    width=30,
    font=("Times New Roman", 18),
    bg="#d9d9d9",
    bd=0,
    justify="center",
    show="*"
)
password_entry.insert(0, "SET PASSWORD")
password_entry.pack(side=LEFT, ipady=10)

book1 = Label(
    password_frame,
    text="📖",
    font=("Arial", 25),
    bg="#efefef"
)
book1.pack(side=LEFT, padx=10)

# Confirm Password
confirm_frame = Frame(window, bg="#efefef")
confirm_frame.pack(pady=10)

confirm_entry = Entry(
    confirm_frame,
    width=30,
    font=("Times New Roman", 18),
    bg="#d9d9d9",
    bd=0,
    justify="center",
    show="*"
)
confirm_entry.insert(0, "CONFIRM PASSWORD")
confirm_entry.pack(side=LEFT, ipady=10)

book2 = Label(
    confirm_frame,
    text="📖",
    font=("Arial", 25),
    bg="#efefef"
)
book2.pack(side=LEFT, padx=10)

# Create Button
create_btn = Button(
    window,
    text="CREATE",
    font=("Times New Roman", 22),
    bg="#d9d9d9",
    bd=0,
    width=10,
    command=create_password
)
create_btn.pack(pady=30)

# Feature Text
feature = Label(
    window,
    text="feature : at least 8 character including number and symbol",
    font=("Times New Roman", 18),
    bg="#efefef",
    fg="black"
)
feature.pack(pady=(20, 70))

# ---------------- BOTTOM SECTION ---------------- #
title2 = Label(
    window,
    text="ENTER MASTER PASSWORD",
    font=("Times New Roman", 35),
    bg="#efefef",
    fg="black"
)
title2.pack(pady=20)

enter_frame = Frame(window, bg="#efefef")
enter_frame.pack(pady=20)

enter_entry = Entry(
    enter_frame,
    width=30,
    font=("Times New Roman", 22),
    bg="#d9d9d9",
    bd=0,
    justify="center",
    show="*"
)
enter_entry.insert(0, "ENTER PASSWORD")
enter_entry.pack(side=LEFT, ipady=12)

eye_btn = Button(
    enter_frame,
    text="👁",
    font=("Arial", 22),
    bg="#efefef",
    bd=0,
    command=toggle_password
)
eye_btn.pack(side=LEFT, padx=15)

window.mainloop()
