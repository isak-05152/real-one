import tkinter as tk
from tkinter import simpledialog
root=tk.Tk()
root.title("master password")
root.geometry("900x700")
root.configure(bg="pink")
# clear window
def clear_window():
    for widget in root.winfo_children():
        widget.destroy()


 # master password interface


def create_master_password():
     
    clear_window()
      
    frame=tk.Frame(root,bg="white",height=250,width=400)
    frame.place(relx=0.5, rely=0.25, anchor="center")
    label=tk.Label(frame,text="SET password",bg="black",
        font=("Times New Roman", 18),fg="green")

    label.pack(pady=20)
    password_entry=tk.Entry(frame,width=30,show="*")
    password_entry.pack(pady=10)

    confirm_pass=tk.Entry(frame,width=30,show="*")
    confirm_pass.pack(pady=10)

    create_btn=tk.Button(frame,text="CREATE",width=20,command=login_win)
    create_btn.pack(pady=10)

def login_win():
    frame=tk.Frame(root,bg="#e8e8e8",width=400,height=300)
    frame.place(relx=0.5, rely=0.25, anchor="center")
    label=tk.Label(frame,text="ENTER MASTER PASSWORD",fg="green",bg="#e8e8e8")
    label.pack(pady=10)


    password_entry=tk.Entry(frame,width=30,show="*")
    password_entry.pack(pady=10)



    def show_password(event):
        password_entry.config(show="")

    def hide_password(event):
        password_entry.config(show="*")
    

    eye_btn = tk.Button(
        frame,
        text="eye",
        
    )
    eye_btn.pack()

    eye_btn.bind("<ButtonPress>",show_password)
    eye_btn.bind("<ButtonRelease>",hide_password)

    enter_btn = tk.Button(
        frame,
        text="ENTER",
        width=20,command=add_platform
        
    )
    enter_btn.pack(pady=20)

def add_platform():
    clear_window()


    frame=tk.Frame(root,bg="black",width=700)
    frame.place(relx=0.5, rely=0.25,anchor="center")
    label=tk.Label(frame,text="PLATFORM",fg="white",bg="black",bd=0,highlightthickness=0
)
    label.pack(pady=10)
    def add_name():
        name=simpledialog.askstring("input","enter platform name")
        if name:
            new_label=tk.Button(frame,fg="#0a192f",bg="#00f1e8", bd=2,
    relief="solid",text=name,font=("Sans Serif",10,"bold"),command=lambda: open_platform(name))
            new_label.pack(side="top",pady=5)

    add_button=tk.Button(
            frame,text="add platform + ",bg="#3a86ff",fg="white", activebackground="#3a86ff", activeforeground="white",command=add_name)

    add_button.pack(side="bottom")
def open_platform(platform_name):
    clear_window()
    frame=tk.Frame(root,bg="black",width=700)
    frame.pack(fill="both", expand=True)
    title=tk.Label(frame,text=platform_name,fg="white",bg="black",font=("Arial", 18, "bold"))
    title.pack(pady=10)
    username_label = tk.Label(
        frame,
        text="Username",
        fg="white",
        bg="black"
    )
    username_label.pack()
    user_name=tk.Entry(frame,width=50)
    user_name.pack(pady=10)
    gmail_label = tk.Label(
        frame,
        text="gmail",
        fg="white",
        bg="black"
    )
    gmail_label.pack()
    user_gmail=tk.Entry(frame,width=50)
    user_gmail.pack(pady=10)
    password_label = tk.Label(
        frame,
        text="Password",
        fg="white",
        bg="black"
    )
    password_label.pack()
    pass_word=tk.Entry(frame,width=50,show="*")
    pass_word.pack(pady=10)

    def show_password(event):
        pass_word.config(show="")

    def hide_password(event):
        pass_word.config(show="*")


    eye_button = tk.Button(
        frame,
        text="eye",

    )
    eye_button.pack()

    eye_button.bind("<ButtonPress>",show_password)
    eye_button.bind("<ButtonRelease>",hide_password)


    plus_button=tk.Button(frame,text="+ account")
    plus_button.pack(pady=10)




      













create_master_password()

root.mainloop()

