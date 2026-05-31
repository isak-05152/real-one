# ================================
# INSTALL FIRST:
# python3 -m pip install customtkinter --break-system-packages
# ================================

import customtkinter as ctk
from tkinter import messagebox

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# =========================================================
# MAIN WINDOW
# =========================================================

root = ctk.CTk()
root.geometry("900x600")
root.title("Password Manager")

# =========================================================
# RUNTIME MEMORY STORAGE
# =========================================================

platforms = []
accounts_data = {}
active_menu = None  # Tracks open dropdown menus to prevent duplicates

# =========================================================
# HELPER
# =========================================================

def clear_window():
    for widget in root.winfo_children():
        widget.destroy()

def close_active_menu():
    global active_menu
    if active_menu is not None:
        try:
            active_menu.destroy()
        except:
            pass
        active_menu = None

# =========================================================
# SET MASTER PASSWORD WINDOW
# =========================================================

def toggle_set_password():
    global set_password_visible
    set_password_visible = not set_password_visible

    if set_password_visible:
        set_password_entry.configure(show="")
        confirm_password_entry.configure(show="")
    else:
        set_password_entry.configure(show="*")
        confirm_password_entry.configure(show="*")

def save_master_password():
    password = set_password_entry.get()
    confirm = confirm_password_entry.get()

    if password == "":
        messagebox.showerror("Error", "Password cannot be empty")
        return

    if password != confirm:
        messagebox.showerror("Error", "Passwords do not match")
        return

    # ====================================================
    # BACKEND: save master password hash here
    # ====================================================
    show_login_window()

def show_set_master_window():
    global set_password_entry
    global confirm_password_entry
    global set_password_visible

    clear_window()
    set_password_visible = False

    frame = ctk.CTkFrame(root, width=600, height=600)
    frame.place(relx=0.5, rely=0.2, anchor="center")

    title = ctk.CTkLabel(frame, text="Set Master Password", font=("Arial", 24, "bold"))
    title.pack(pady=(30, 20))

    set_password_entry = ctk.CTkEntry(frame, width=250, placeholder_text="Enter Password", show="*")
    set_password_entry.pack(pady=5)

    confirm_password_entry = ctk.CTkEntry(frame, width=250, placeholder_text="Confirm Password", show="*")
    confirm_password_entry.pack(pady=10)

    toggle_btn = ctk.CTkButton(frame, text="👁 ", width=80, command=toggle_set_password)
    toggle_btn.pack(padx=10)

    save_btn = ctk.CTkButton(frame, text="Save Password", command=save_master_password)
    save_btn.pack(pady=20)

    i_label = ctk.CTkLabel(frame, text="HINT: password should be at least 8 characters", text_color="black")
    i_label.pack(pady=(0, 5))


# =========================================================
# LOGIN WINDOW
# =========================================================

def toggle_login_password():
    global login_password_visible
    login_password_visible = not login_password_visible

    if login_password_visible:
        login_password_entry.configure(show="")
    else:
        login_password_entry.configure(show="•")

def unlock_vault():
    entered_password = login_password_entry.get()
    # ====================================================
    # BACKEND: verify master password here
    # ====================================================
    show_platform_window()

def show_login_window():
    global login_password_entry
    global login_password_visible

    clear_window()
    login_password_visible = False

    frame = ctk.CTkFrame(root, width=600, height=600)
    frame.place(relx=0.5, rely=0.2, anchor="center")

    title = ctk.CTkLabel(frame, text="ENTER MASTER PASSWORD", font=("Arial", 24, "bold"))
    title.pack(pady=(30, 20))

    login_password_entry = ctk.CTkEntry(frame, width=250, placeholder_text="Master Password", show="*")
    login_password_entry.pack(pady=10)

    toggle_btn = ctk.CTkButton(frame, text="👁 ", width=80, command=toggle_login_password)
    toggle_btn.pack(pady=10)

    unlock_btn = ctk.CTkButton(frame, text="Unlock", command=unlock_vault)
    unlock_btn.pack(pady=20)


# =========================================================
# LOGOUT
# =========================================================

def logout():
    result = messagebox.askyesno("Logout", "Do you want to logout?")
    if result:
        show_login_window()


# =========================================================
# CHANGE MASTER PASSWORD
# =========================================================

def open_change_master_popup():
    popup = ctk.CTkToplevel(root)
    popup.geometry("350x260")  
    popup.title("Verify Password")
    popup.transient(root)

    title = ctk.CTkLabel(popup, text="Verify Master Password", font=("Arial", 20, "bold"))
    title.pack(pady=(20, 15))

    password_entry = ctk.CTkEntry(popup, width=250, placeholder_text="Enter Current Password", show="•")
    password_entry.pack(pady=10)

    
    def flash_visibility():
        toggle_btn.configure(state="disabled")
        password_entry.configure(show="")
        password_entry.update_idletasks()  
        
        def hide_again():
            password_entry.configure(show="*")
            password_entry.update_idletasks()  
            toggle_btn.configure(state="normal")
            
        popup.after(1000, hide_again)

    
    toggle_btn = ctk.CTkButton(popup, text="👁 ", width=60, command=flash_visibility)
    toggle_btn.pack(pady=5)

    def verify_password():
        entered_password = password_entry.get()
        # ====================================================
        # BACKEND: verify password here
        # ====================================================
        popup.grab_release()
        popup.destroy()
        show_set_master_window()

    verify_btn = ctk.CTkButton(popup, text="Verify", command=verify_password)
    verify_btn.pack(pady=15)

    popup.wait_visibility()
    popup.grab_set()


# =========================================================
# PLATFORM WINDOW
# =========================================================

def show_platform_window():
    global platform_frame
    clear_window()

    top_frame = ctk.CTkFrame(root)
    top_frame.pack(fill="x", padx=10, pady=10)

    title = ctk.CTkLabel(top_frame, text="Platforms", font=("Arial", 28, "bold"))
    title.pack(side="left", padx=10)

    change_btn = ctk.CTkButton(top_frame, text="change M-password", width=40, command=open_change_master_popup)
    change_btn.pack(side="right", padx=5)

    logout_btn = ctk.CTkButton(top_frame, width=40, text="Logout", fg_color="#F54927", hover_color="#F54927", text_color="white", command=logout)
    logout_btn.pack(side="right", padx=5)

    separator = ctk.CTkFrame(root, height=2)
    separator.pack(fill="x", padx=20)

    platform_frame = ctk.CTkScrollableFrame(root, width=700, height=400)
    platform_frame.pack(fill="both", expand=True, padx=20, pady=20)

    add_btn = ctk.CTkButton(root, text="+ Add Platform", fg_color="#8C8C3C", hover_color="#8C8C3C",height=40, command=open_add_platform_popup)
    add_btn.pack(pady=10)

    render_platforms()


# =========================================================
# RENDER PLATFORMS
# =========================================================

def render_platforms():
    for widget in platform_frame.winfo_children():
        widget.destroy()

    if len(platforms) == 0:
        label = ctk.CTkLabel(platform_frame, text="No platform added yet", font=("Arial", 18))
        label.pack(pady=30)
        return

    for platform in platforms:
        
        row = ctk.CTkFrame(platform_frame, width=500, height=50)
        row.pack(pady=5, padx=100) 
        row.pack_propagate(False)   

        
        platform_btn = ctk.CTkButton(
            row, text=platform, fg_color="pink", hover_color="pink", text_color="black", anchor="w",
            width=420, height=40, command=lambda p=platform: open_account_window(p)
        )
        platform_btn.pack(side="left", padx=(10, 5), pady=5)


        menu_btn = ctk.CTkButton(row, text="⋮", width=40, height=40, command=lambda p=platform: show_platform_menu(p))
        menu_btn.pack(side="left", padx=5, pady=5)


# =========================================================
# ADD PLATFORM
# =========================================================

def open_add_platform_popup():
    popup = ctk.CTkToplevel(root)
    popup.geometry("350x200")
    popup.title("Add Platform")
    popup.transient(root)

    title = ctk.CTkLabel(popup, text="Add Platform", font=("Arial", 20, "bold"))
    title.pack(pady=(20, 15))

    entry = ctk.CTkEntry(popup, width=250, fg_color="#8F6F6F", text_color="black", placeholder_text_color="black", placeholder_text="Platform Name")
    entry.pack(pady=10)

    def add_platform():
        name = entry.get().strip()

        if name == "":
            messagebox.showwarning("Warning", "Platform name cannot be empty", parent=popup)
            return

        if name in platforms:
            messagebox.showwarning("Warning", "Platform already exists", parent=popup)
            return

        platforms.append(name)
        accounts_data[name] = []

        render_platforms()
        popup.grab_release()
        popup.destroy()

    add_btn = ctk.CTkButton(popup, text="Add", fg_color="#332F3B", hover_color="#332F3B", command=add_platform)
    add_btn.pack(pady=20)

    popup.wait_visibility()
    popup.grab_set()


# =========================================================
# PLATFORM MENU
# =========================================================

def show_platform_menu(platform_name):
    global active_menu
    
    if active_menu is not None:
        close_active_menu()
        return

    menu = ctk.CTkToplevel(root)
    menu.geometry("120x90")
    menu.overrideredirect(True)

    x = root.winfo_pointerx()
    y = root.winfo_pointery()
    menu.geometry(f"+{x}+{y}")
    
    active_menu = menu

    edit_btn = ctk.CTkButton(menu, text="Edit", command=lambda: [close_active_menu(), open_edit_platform_popup(platform_name)])
    edit_btn.pack(fill="x", padx=5, pady=5)

    delete_btn = ctk.CTkButton(menu, text="Delete", fg_color="darkred", hover_color="red", command=lambda: [close_active_menu(), open_delete_platform_popup(platform_name)])
    delete_btn.pack(fill="x", padx=5, pady=5)

    menu.bind("<FocusOut>", lambda e: close_active_menu())


# =========================================================
# EDIT PLATFORM
# =========================================================

def open_edit_platform_popup(old_name):
    popup = ctk.CTkToplevel(root)
    popup.geometry("350x180")
    popup.title("Edit Platform")
    popup.transient(root)

    entry = ctk.CTkEntry(popup, width=250)
    entry.insert(0, old_name)
    entry.pack(pady=30)

    def save_edit():
        new_name = entry.get().strip()

        if new_name == "":
            messagebox.showwarning("Warning", "Platform name cannot be empty", parent=popup)
            return

        if new_name in platforms and new_name != old_name:
            messagebox.showwarning("Warning", "Platform already exists", parent=popup)
            return

        index = platforms.index(old_name)
        platforms[index] = new_name
        accounts_data[new_name] = accounts_data.pop(old_name)

        render_platforms()
        popup.grab_release()
        popup.destroy()

    save_btn = ctk.CTkButton(popup, text="Save", command=save_edit)
    save_btn.pack(pady=10)

    popup.wait_visibility()
    popup.grab_set()


# =========================================================
# DELETE PLATFORM
# =========================================================

def open_delete_platform_popup(platform_name):
    popup = ctk.CTkToplevel(root)
    popup.geometry("400x260")
    popup.title("Delete Platform")
    popup.transient(root)

    label = ctk.CTkLabel(popup, text=f"Delete '{platform_name}' ?", font=("Arial", 18))
    label.pack(pady=20)
    u_label = ctk.CTkLabel(popup, text=f"NOTE : all the content inside '{platform_name}' will also be deleted ", font=("italics", 10))
    u_label.pack(pady=10)


    def delete_platform():
        platforms.remove(platform_name)
        del accounts_data[platform_name]

        render_platforms()
        popup.grab_release()
        popup.destroy()

    delete_btn = ctk.CTkButton(popup, text="Delete", fg_color="darkred", hover_color="red", command=delete_platform)
    delete_btn.pack(pady=10)

    popup.wait_visibility()
    popup.grab_set()


# =========================================================
# ACCOUNT WINDOW
# =========================================================

def open_account_window(platform_name):
    clear_window()

    top_frame = ctk.CTkFrame(root)
    top_frame.pack(fill="x", padx=10, pady=10)

    back_btn = ctk.CTkButton(top_frame, text="<--", fg_color="#1C3327", hover_color="#1C3327", command=show_platform_window)
    back_btn.pack(side="left", padx=5)

    title = ctk.CTkLabel(top_frame, text=platform_name, font=("Arial", 26, "bold"))
    title.pack(side="left", padx=20)

    change_btn = ctk.CTkButton(top_frame, text="change M-password", command=open_change_master_popup)
    change_btn.pack(side="right", padx=5)

    logout_btn = ctk.CTkButton(top_frame, text="Logout", fg_color="#F20A0A", hover_color="#F20A0A", width=40, command=logout)
    logout_btn.pack(side="right", padx=5)

    separator = ctk.CTkFrame(root, height=2)
    separator.pack(fill="x", padx=20)

    account_frame = ctk.CTkScrollableFrame(root, width=700, height=400)
    account_frame.pack(fill="both", expand=True, padx=20, pady=20)

    accounts = accounts_data.get(platform_name, [])

    if len(accounts) == 0:
        label = ctk.CTkLabel(account_frame, text="No account added yet", font=("Arial", 18))
        label.pack(pady=30)
    else:
        for account in accounts:
            row = ctk.CTkFrame(account_frame)
            row.pack(fill="x", pady=5)

            login_label = ctk.CTkLabel(row, text=account["login_id"], width=250, anchor="w")
            login_label.pack(side="left", padx=10)

            password_label = ctk.CTkLabel(row, text="******", width=150)
            password_label.pack(side="left")

            menu_btn = ctk.CTkButton(row, text="⋮", width=40, command=lambda a=account: show_account_menu(platform_name, a))
            menu_btn.pack(side="left", padx=10)

            def toggle_password(label=password_label, acc=account):
                if label.cget("text") == "******":
                    label.configure(text=acc["password"])
                else:
                    label.configure(text="******")

            view_btn = ctk.CTkButton(row, text="👁  ", width=40, command=toggle_password)
            view_btn.pack(side="left", padx=10)

    add_btn = ctk.CTkButton(root, text="+ Add Ac", fg_color="#D9367A", hover_color="#D9367A", command=lambda: open_add_account_popup(platform_name))
    add_btn.pack(pady=10)


# =========================================================
# ADD ACCOUNT (FORCED INTERACTION UPDATE)
# =========================================================

def open_add_account_popup(platform_name):
    popup = ctk.CTkToplevel(root)
    popup.geometry("400x320")
    popup.title("Add Account")
    popup.transient(root)

    title = ctk.CTkLabel(popup, text="Add Account", font=("Arial", 20, "bold"))
    title.pack(pady=(20, 15))

    login_entry = ctk.CTkEntry(popup, width=280, placeholder_text="Login ID")
    login_entry.pack(pady=10)

    password_entry = ctk.CTkEntry(popup, width=280, placeholder_text="Password", show="•")
    password_entry.pack(pady=5)

    def flash_visibility():
        eye_btn.configure(state="disabled")
        password_entry.configure(show="")
        password_entry.update_idletasks()  # Forces system redraw
        
        def hide_again():
            password_entry.configure(show="•")
            password_entry.update_idletasks()  # Forces system mask redraw
            eye_btn.configure(state="normal")
            
        popup.after(1000, hide_again)

    eye_btn = ctk.CTkButton(popup, text="👁 ", width=60, command=flash_visibility)
    eye_btn.pack(pady=5)

    def add_account():
        login_id = login_entry.get().strip()
        password = password_entry.get().strip()

        if login_id == "" or password == "":
            messagebox.showwarning("Warning", "Fields cannot be empty", parent=popup)
            return

        accounts_data[platform_name].append({
            "login_id": login_id,
            "password": password
        })

        popup.grab_release()
        popup.destroy()
        open_account_window(platform_name)

    add_btn = ctk.CTkButton(popup, text="Add", fg_color="#332F3B", hover_color="#332F3B", command=add_account)
    add_btn.pack(pady=15)

    popup.wait_visibility()
    popup.grab_set()


# =========================================================
# EDIT ACCOUNT CREDENTIALS (FORCED INTERACTION UPDATE)
# =========================================================

def open_edit_account_popup(platform_name, account):
    popup = ctk.CTkToplevel(root)
    popup.geometry("400x320")
    popup.title("Edit Account")
    popup.transient(root)

    title = ctk.CTkLabel(popup, text="Edit Account Details", font=("Arial", 20, "bold"))
    title.pack(pady=(20, 15))

    login_entry = ctk.CTkEntry(popup, width=280)
    login_entry.insert(0, account["login_id"])
    login_entry.pack(pady=10)

    password_entry = ctk.CTkEntry(popup, width=280, show="•")
    password_entry.insert(0, account["password"])
    password_entry.pack(pady=5)

    def flash_visibility():
        eye_btn.configure(state="disabled")
        password_entry.configure(show="")
        password_entry.update_idletasks()
        
        def hide_again():
            password_entry.configure(show="•")
            password_entry.update_idletasks()
            eye_btn.configure(state="normal")
            
        popup.after(1000, hide_again)

    eye_btn = ctk.CTkButton(popup, text="👁 ", width=60, command=flash_visibility)
    eye_btn.pack(pady=5)

    def save_account_edit():
        new_login = login_entry.get().strip()
        new_password = password_entry.get().strip()

        if new_login == "" or new_password == "":
            messagebox.showwarning("Warning", "Fields cannot be empty", parent=popup)
            return

        account["login_id"] = new_login
        account["password"] = new_password

        popup.grab_release()
        popup.destroy()
        open_account_window(platform_name)

    save_btn = ctk.CTkButton(popup, text="Save Changes", command=save_account_edit)
    save_btn.pack(pady=15)

    popup.wait_visibility()
    popup.grab_set()


# =========================================================
# CHANGE ACCOUNT PASSWORD (FORCED INTERACTION UPDATE)
# =========================================================

def open_change_account_password_popup(platform_name, account):
    popup = ctk.CTkToplevel(root)
    popup.geometry("350x240")
    popup.title("Change Password")
    popup.transient(root)

    title = ctk.CTkLabel(popup, text="Update Account Password", font=("Arial", 18, "bold"))
    title.pack(pady=(20, 10))

    password_entry = ctk.CTkEntry(popup, width=250, show="•")
    password_entry.insert(0, account["password"])
    password_entry.pack(pady=5)

    def flash_visibility():
        eye_btn.configure(state="disabled")
        password_entry.configure(show="")
        password_entry.update_idletasks()
        
        def hide_again():
            password_entry.configure(show="•")
            password_entry.update_idletasks()
            eye_btn.configure(state="normal")
            
        popup.after(1000, hide_again)

    eye_btn = ctk.CTkButton(popup, text="👁 ", width=60, command=flash_visibility)
    eye_btn.pack(pady=5)

    def save_password_edit():
        new_password = password_entry.get().strip()

        if new_password == "":
            messagebox.showwarning("Warning", "Password field cannot be empty", parent=popup)
            return

        account["password"] = new_password

        popup.grab_release()
        popup.destroy()
        open_account_window(platform_name)

    save_btn = ctk.CTkButton(popup, text="Update Password", command=save_password_edit)
    save_btn.pack(pady=10)

    popup.wait_visibility()
    popup.grab_set()


# =========================================================
# ACCOUNT MENU
# =========================================================

def show_account_menu(platform_name, account):
    global active_menu

    if active_menu is not None:
        close_active_menu()
        return

    menu = ctk.CTkToplevel(root)
    menu.geometry("180x210")
    menu.overrideredirect(True)

    x = root.winfo_pointerx()
    y = root.winfo_pointery()
    menu.geometry(f"+{x}+{y}")

    active_menu = menu

    edit_btn = ctk.CTkButton(menu, text="Edit Login", command=lambda: [close_active_menu(), open_edit_account_popup(platform_name, account)])
    edit_btn.pack(fill="x", padx=5, pady=3)

    password_btn = ctk.CTkButton(menu, text="Change Password", command=lambda: [close_active_menu(), open_change_account_password_popup(platform_name, account)])
    password_btn.pack(fill="x", padx=5, pady=3)

    def copy_login():
        root.clipboard_clear()
        root.clipboard_append(account["login_id"])
        close_active_menu()
        messagebox.showinfo("Copied", "Login ID copied")

    copy_login_btn = ctk.CTkButton(menu, text="Copy Login", command=copy_login)
    copy_login_btn.pack(fill="x", padx=5, pady=3)

    def copy_password():
        root.clipboard_clear()
        root.clipboard_append(account["password"])
        close_active_menu()
        messagebox.showinfo("Copied", "Password copied")

    copy_password_btn = ctk.CTkButton(menu, text="Copy Password", command=copy_password)
    copy_password_btn.pack(fill="x", padx=5, pady=3)

    def delete_account():
        accounts_data[platform_name].remove(account)
        close_active_menu()
        open_account_window(platform_name)

    delete_btn = ctk.CTkButton(menu, text="Delete", fg_color="darkred", hover_color="red", command=delete_account)
    delete_btn.pack(fill="x", padx=5, pady=3)

    menu.bind("<FocusOut>", lambda e: close_active_menu())


# =========================================================
# START WINDOW
# =========================================================

show_set_master_window()
root.mainloop()
