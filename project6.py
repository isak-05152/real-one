import tkinter as tk

root = tk.Tk()
root.title("Password Manager")
root.geometry("900x700")
root.configure(bg="#1e1e1e")

# =========================
# CLEAR WINDOW
# =========================

def clear_window():
    for widget in root.winfo_children():
        widget.destroy()

# =========================
# 1. CREATE MASTER PASSWORD
# =========================

def create_master_window():

    clear_window()

    frame = tk.Frame(root, bg="#e8e8e8", width=400, height=250)
    frame.place(relx=0.5, rely=0.25, anchor="center")

    title = tk.Label(
        frame,
        text="SET MASTER PASSWORD",
        bg="#e8e8e8",
        font=("Times New Roman", 18)
    )
    title.pack(pady=20)

    password_entry = tk.Entry(frame, width=30, show="*")
    password_entry.pack(pady=10)

    confirm_entry = tk.Entry(frame, width=30, show="*")
    confirm_entry.pack(pady=10)

    create_btn = tk.Button(
        frame,
        text="CREATE",
        width=20,
        command=login_window
    )
    create_btn.pack(pady=20)

# =========================
# 2. LOGIN WINDOW
# =========================

def login_window():

    clear_window()

    frame = tk.Frame(root, bg="#e8e8e8", width=400, height=250)
    frame.place(relx=0.5, rely=0.25, anchor="center")

    title = tk.Label(
        frame,
        text="ENTER MASTER PASSWORD",
        bg="#e8e8e8",
        font=("Times New Roman", 18)
    )
    title.pack(pady=20)

    password_entry = tk.Entry(frame, width=30, show="*")
    password_entry.pack(pady=10)

    eye_btn = tk.Button(
        frame,
        text="👁"
        #command=show_password()
    )
    eye_btn.pack()

    enter_btn = tk.Button(
        frame,
        text="ENTER",
        width=20,
        command=applications_window
    )
    enter_btn.pack(pady=20)

# =========================
# 3. APPLICATION WINDOW
# =========================

def applications_window():

    clear_window()

    # LEFT SIDE

    left_frame = tk.Frame(root, bg="#f0eaea", width=350)
    left_frame.pack(side="left", fill="y")

    title = tk.Label(
        left_frame,
        text="APPLICATIONS",
        bg="#f0eaea",
        font=("Times New Roman", 18)
    )
    title.pack(pady=20)

    # PLATFORM BUTTONS

    insta_btn = tk.Button(
        left_frame,
        text="INSTAGRAM",
        width=25,
        command=lambda: platform_window("INSTAGRAM")
    )
    insta_btn.pack(pady=10)

    facebook_btn = tk.Button(
        left_frame,
        text="FACEBOOK",
        width=25,
        command=lambda: platform_window("FACEBOOK")
    )
    facebook_btn.pack(pady=10)

    steam_btn = tk.Button(
        left_frame,
        text="STEAM",
        width=25,
        command=lambda: platform_window("STEAM")
    )
    steam_btn.pack(pady=10)

    add_more_btn = tk.Button(
        left_frame,
        text="ADD MORE",
        width=25
    )
    add_more_btn.pack(pady=20)

# =========================
# 4. PLATFORM WINDOW
# =========================

def platform_window(platform_name):

    clear_window()

    frame = tk.Frame(root, bg="#dddddd")
    frame.pack(expand=True, fill="both")

    title = tk.Label(
        frame,
        text=platform_name,
        fg="red",
        bg="#dddddd",
        font=("Arial", 20)
    )
    title.pack(pady=20)

    # EMAIL

    email_entry = tk.Entry(frame, width=40)
    email_entry.insert(0, "EMAIL")
    email_entry.pack(pady=10)

    # USERNAME

    username_entry = tk.Entry(frame, width=40)
    username_entry.insert(0, "USERNAME")
    username_entry.pack(pady=10)

    # PASSWORD

    password_frame = tk.Frame(frame, bg="#dddddd")
    password_frame.pack(pady=10)

    password_entry = tk.Entry(
        password_frame,
        width=35,
        show="*"
    )
    password_entry.pack(side="left")

    eye_btn = tk.Button(
        password_frame,
        text="👁"
    )
    eye_btn.pack(side="left", padx=5)

    # ADD ACCOUNT BUTTON

    add_account_btn = tk.Button(
        frame,
        text="ADD ACCOUNT",
        width=25,
        bg="#555555",
        fg="white"
    )
    add_account_btn.pack(pady=20)

    # BACK BUTTON

    back_btn = tk.Button(
        frame,
        text="BACK",
        width=15,
        command=applications_window
    )
    back_btn.pack()

# =========================
# START APP
# =========================

create_master_window()

root.mainloop()
