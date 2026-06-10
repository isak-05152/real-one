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
current_viewing_platform = None  # Remembers which platform account view is rendering

# =========================================================
# HELPER FOR TOGGLING VIEWS (SPEED OPTIMIZATION)
# =========================================================

def switch_to_view(view_frame):
    """Hides all primary screen frames instantly and reveals the requested view frame."""
    close_active_menu()
    
    # Hide all pre-built root level structures
    set_master_frame.place_forget()
    login_frame.place_forget()
    platform_main_container.pack_forget()
    account_main_container.pack_forget()
    
    # Show target panel
    if view_frame in (set_master_frame, login_frame):
        view_frame.place(relx=0.5, rely=0.2, anchor="center")
    else:
        view_frame.pack(fill="both", expand=True)

def close_active_menu():
    global active_menu
    if active_menu is not None:
        try:
            active_menu.destroy()
        except:
            pass
        active_menu = None

# =========================================================
# PRE-INITIALIZING INTERFACES (PRE-BUILT FOR SPEED)
# =========================================================

set_master_frame = ctk.CTkFrame(root, width=600, height=600)
login_frame = ctk.CTkFrame(root, width=600, height=600)
platform_main_container = ctk.CTkFrame(root, fg_color="transparent")
account_main_container = ctk.CTkFrame(root, fg_color="transparent")

# =========================================================
# SET MASTER PASSWORD VIEW
# =========================================================

set_password_visible = False

def toggle_set_password():
    global set_password_visible
    set_password_visible = not set_password_visible
    mask = "" if set_password_visible else "*"
    set_password_entry.configure(show=mask)
    confirm_password_entry.configure(show=mask)

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

# Building View Structure Once
ctk.CTkLabel(set_master_frame, text="Set Master Password", font=("Arial", 24, "bold")).pack(pady=(30, 20))
set_password_entry = ctk.CTkEntry(set_master_frame, width=250, placeholder_text="Enter Password", show="*")
set_password_entry.pack(pady=5)
confirm_password_entry = ctk.CTkEntry(set_master_frame, width=250, placeholder_text="Confirm Password", show="*")
confirm_password_entry.pack(pady=10)

ctk.CTkButton(set_master_frame, text="👁 ", width=80, command=toggle_set_password).pack(padx=10)
ctk.CTkButton(set_master_frame, text="Save Password", command=save_master_password).pack(pady=20)
ctk.CTkLabel(set_master_frame, text="HINT: password should be at least 8 characters", text_color="black").pack(pady=(0, 5))

def show_set_master_window():
    global set_password_visible
    set_password_visible = False
    set_password_entry.delete(0, 'end')
    confirm_password_entry.delete(0, 'end')
    set_password_entry.configure(show="*")
    confirm_password_entry.configure(show="*")
    switch_to_view(set_master_frame)


# =========================================================
# LOGIN VIEW
# =========================================================

def unlock_vault():
    entered_password = login_password_entry.get()
    # ====================================================
    # BACKEND: verify master password here
    # ====================================================
    show_platform_window()

# Building View Structure Once
ctk.CTkLabel(login_frame, text="ENTER MASTER PASSWORD", font=("Arial", 24, "bold")).pack(pady=(30, 20))
login_password_entry = ctk.CTkEntry(login_frame, width=250, placeholder_text="Master Password", show="*")
login_password_entry.pack(pady=10)

def tflash_visibility():
    toggle_btn.configure(state="disabled")
    login_password_entry.configure(show="")
    login_password_entry.update_idletasks()

    def thide_again():
        login_password_entry.configure(show="*")
        login_password_entry.update_idletasks()
        toggle_btn.configure(state="normal")

    root.after(3000, thide_again)

toggle_btn = ctk.CTkButton(login_frame, text="👁 ", width=80, command=tflash_visibility)
toggle_btn.pack(pady=10)
ctk.CTkButton(login_frame, text="Unlock", command=unlock_vault).pack(pady=20)

def show_login_window():
    login_password_entry.delete(0, 'end')
    login_password_entry.configure(show="*")
    switch_to_view(login_frame)


# =========================================================
# LOGOUT & PASSWORD OVERLAYS
# =========================================================

def logout():
    if messagebox.askyesno("Logout", "Do you want to logout?"):
        show_login_window()

def open_change_master_popup():
    popup = ctk.CTkToplevel(root)
    popup.geometry("350x260")  
    popup.title("Verify Password")
    popup.transient(root)

    ctk.CTkLabel(popup, text="Verify Master Password", font=("Arial", 20, "bold")).pack(pady=(20, 15))
    password_entry = ctk.CTkEntry(popup, width=250, placeholder_text="Enter Current Password", show="•")
    password_entry.pack(pady=10)
    
    def flash_visibility():
        p_toggle_btn.configure(state="disabled")
        password_entry.configure(show="")
        password_entry.update_idletasks()  
        
        def hide_again():
            password_entry.configure(show="*")
            password_entry.update_idletasks()  
            p_toggle_btn.configure(state="normal")
            
        popup.after(3000, hide_again)

    p_toggle_btn = ctk.CTkButton(popup, text="👁 ", width=60, command=flash_visibility)
    p_toggle_btn.pack(pady=5)

    def verify_password():
        # ====================================================
        # BACKEND: verify password here
        # ====================================================
        popup.grab_release()
        popup.destroy()
        show_set_master_window()

    ctk.CTkButton(popup, text="Verify", command=verify_password).pack(pady=15)
    popup.wait_visibility()
    popup.grab_set()


# =========================================================
# PLATFORM PANELS BUILDING
# =========================================================

plat_top_frame = ctk.CTkFrame(platform_main_container)
plat_top_frame.pack(fill="x", padx=10, pady=10)

ctk.CTkLabel(plat_top_frame, text="Platforms", font=("Arial", 28, "bold")).pack(side="left", padx=10)
ctk.CTkButton(plat_top_frame, text="change M-password", width=40, command=open_change_master_popup).pack(side="right", padx=5)
ctk.CTkButton(plat_top_frame, width=40, text="⏻ ", fg_color="#F54927", hover_color="#F54927", text_color="white", command=logout).pack(side="right", padx=5)

ctk.CTkFrame(platform_main_container, height=2).pack(fill="x", padx=20)

platform_scroll_frame = ctk.CTkScrollableFrame(platform_main_container, width=700, height=400)
platform_scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)

def show_platform_window():
    switch_to_view(platform_main_container)
    render_platforms()

# =========================================================
# RENDER PLATFORMS
# =========================================================

def render_platforms():
    for widget in platform_scroll_frame.winfo_children():
        widget.destroy()

    if len(platforms) == 0:
        ctk.CTkLabel(platform_scroll_frame, text="No platform added yet", font=("Arial", 18)).pack(pady=30)
        return

    for platform in platforms:
        row = ctk.CTkFrame(platform_scroll_frame, width=500, height=50)
        row.pack(pady=5, padx=100) 
        row.pack_propagate(False)   
        
        platform_btn = ctk.CTkButton(
            row, text=platform, fg_color="pink", hover_color="pink", text_color="black", anchor="w",
            width=420, height=40, command=lambda p=platform: open_account_window(p)
        )
        platform_btn.pack(side="left", padx=(10, 5), pady=5)

        menu_btn = ctk.CTkButton(row, text="⋮", width=40, height=40, command=lambda p=platform: show_platform_menu(p))
        menu_btn.pack(side="left", padx=5, pady=5)

ctk.CTkButton(platform_main_container, text="+ Add Platform", fg_color="#8C8C3C", hover_color="#8C8C3C", height=40, command=lambda: open_add_platform_popup()).pack(pady=10)


# =========================================================
# ADD / EDIT / DELETE PLATFORM POPUPS
# =========================================================

def open_add_platform_popup():
    popup = ctk.CTkToplevel(root)
    popup.geometry("350x200")
    popup.title("Add Platform")
    popup.transient(root)

    ctk.CTkLabel(popup, text="Add Platform", font=("Arial", 20, "bold")).pack(pady=(20, 15))
    entry = ctk.CTkEntry(popup, width=250, fg_color="#8F6F6F", text_color="black", placeholder_text_color="black", placeholder_text="Platform Name")
    entry.pack(pady=10)

    def add_platform():
        name = entry.get().strip()
        if name == "" or name in platforms:
            messagebox.showwarning("Warning", "Invalid or existing platform name", parent=popup)
            return

        platforms.append(name)
        accounts_data[name] = []
        render_platforms()
        popup.grab_release()
        popup.destroy()

    ctk.CTkButton(popup, text="Add", fg_color="#332F3B", hover_color="#332F3B", command=add_platform).pack(pady=20)
    popup.wait_visibility()
    popup.grab_set()

def show_platform_menu(platform_name):
    global active_menu
    if active_menu is not None:
        close_active_menu()
        return

    menu = ctk.CTkToplevel(root)
    menu.geometry("120x90")
    menu.overrideredirect(True)
    menu.geometry(f"+{root.winfo_pointerx()}+{root.winfo_pointery()}")
    active_menu = menu

    ctk.CTkButton(menu, text="Edit", command=lambda: [close_active_menu(), open_edit_platform_popup(platform_name)]).pack(fill="x", padx=5, pady=5)
    ctk.CTkButton(menu, text="Delete", fg_color="darkred", hover_color="red", command=lambda: [close_active_menu(), open_delete_platform_popup(platform_name)]).pack(fill="x", padx=5, pady=5)
    menu.bind("<FocusOut>", lambda e: close_active_menu())

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
        if new_name == "" or (new_name in platforms and new_name != old_name):
            messagebox.showwarning("Warning", "Invalid or duplicate platform name", parent=popup)
            return

        index = platforms.index(old_name)
        platforms[index] = new_name
        accounts_data[new_name] = accounts_data.pop(old_name)
        render_platforms()
        popup.grab_release()
        popup.destroy()

    ctk.CTkButton(popup, text="Save", command=save_edit).pack(pady=10)
    popup.wait_visibility()
    popup.grab_set()

def open_delete_platform_popup(platform_name):
    popup = ctk.CTkToplevel(root)
    popup.geometry("400x260")
    popup.title("Delete Platform")
    popup.transient(root)

    ctk.CTkLabel(popup, text=f"Delete '{platform_name}' ?", font=("Arial", 18)).pack(pady=20)
    ctk.CTkLabel(popup, text=f"NOTE : all content inside '{platform_name}' will also be deleted", font=("italics", 10)).pack(pady=10)

    def delete_platform():
        platforms.remove(platform_name)
        del accounts_data[platform_name]
        render_platforms()
        popup.grab_release()
        popup.destroy()

    ctk.CTkButton(popup, text="Delete", fg_color="darkred", hover_color="red", command=delete_platform).pack(pady=10)
    popup.wait_visibility()
    popup.grab_set()


# =========================================================
# ACCOUNT PANELS BUILDING
# =========================================================

acc_top_frame = ctk.CTkFrame(account_main_container)
acc_top_frame.pack(fill="x", padx=10, pady=10)

ctk.CTkButton(acc_top_frame, text="<--", fg_color="#1C3327", hover_color="#1C3327", command=show_platform_window).pack(side="left", padx=5)
account_title_label = ctk.CTkLabel(acc_top_frame, text="", font=("Arial", 26, "bold"))
account_title_label.pack(side="left", padx=20)

ctk.CTkButton(acc_top_frame, text="change M-password", command=open_change_master_popup).pack(side="right", padx=5)
ctk.CTkButton(acc_top_frame, text="⏻", fg_color="#F20A0A", hover_color="#F20A0A", width=40, command=logout).pack(side="right", padx=5)

ctk.CTkFrame(account_main_container, height=2).pack(fill="x", padx=20)

account_scroll_frame = ctk.CTkScrollableFrame(account_main_container, width=700, height=400)
account_scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)

def render_accounts(platform_name):
    for widget in account_scroll_frame.winfo_children():
        widget.destroy()

    accounts = accounts_data.get(platform_name, [])

    if len(accounts) == 0:
        ctk.CTkLabel(account_scroll_frame, text="No account added yet", font=("Arial", 18)).pack(pady=30)
    else:
        for account in accounts:
            row = ctk.CTkFrame(account_scroll_frame)
            row.pack(fill="x", pady=5)

            ctk.CTkLabel(row, text=account["login_id"], width=250, anchor="w").pack(side="left", padx=10)
            password_label = ctk.CTkLabel(row, text="******", width=150)
            password_label.pack(side="left")

            ctk.CTkButton(row, text="⋮", width=40, command=lambda a=account: show_account_menu(platform_name, a)).pack(side="left", padx=10)

            def toggle_password(lbl=password_label, acc=account):
                lbl.configure(text=acc["password"] if lbl.cget("text") == "******" else "******")

            ctk.CTkButton(row, text="👁  ", width=40, command=toggle_password).pack(side="left", padx=10)

def open_account_window(platform_name):
    global current_viewing_platform
    current_viewing_platform = platform_name
    account_title_label.configure(text=platform_name)
    switch_to_view(account_main_container)
    render_accounts(platform_name)

ctk.CTkButton(account_main_container, text="+ Add Ac", fg_color="#D9367A", hover_color="#D9367A", command=lambda: open_add_account_popup(current_viewing_platform)).pack(pady=10)


# =========================================================
# ADD / EDIT / OPERATIONS FOR ACCOUNTS
# =========================================================

def open_add_account_popup(platform_name):
    popup = ctk.CTkToplevel(root)
    popup.geometry("400x320")
    popup.title("Add Account")
    popup.transient(root)

    ctk.CTkLabel(popup, text="Add Account", font=("Arial", 20, "bold")).pack(pady=(20, 15))
    login_entry = ctk.CTkEntry(popup, width=280, placeholder_text="Login ID")
    login_entry.pack(pady=10)
    password_entry = ctk.CTkEntry(popup, width=280, placeholder_text="Password", show="•")
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

    def add_account():
        login_id = login_entry.get().strip()
        password = password_entry.get().strip()
        if login_id == "" or password == "":
            messagebox.showwarning("Warning", "Fields cannot be empty", parent=popup)
            return

        accounts_data[platform_name].append({"login_id": login_id, "password": password})
        popup.grab_release()
        popup.destroy()
        render_accounts(platform_name)

    ctk.CTkButton(popup, text="Add", fg_color="#332F3B", hover_color="#332F3B", command=add_account).pack(pady=15)
    popup.wait_visibility()
    popup.grab_set()

def open_edit_account_popup(platform_name, account):
    popup = ctk.CTkToplevel(root)
    popup.geometry("400x320")
    popup.title("Edit Account")
    popup.transient(root)

    ctk.CTkLabel(popup, text="Edit Account Details", font=("Arial", 20, "bold")).pack(pady=(20, 15))
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
        render_accounts(platform_name)

    ctk.CTkButton(popup, text="Save Changes", command=save_account_edit).pack(pady=15)
    popup.wait_visibility()
    popup.grab_set()

def open_change_account_password_popup(platform_name, account):
    popup = ctk.CTkToplevel(root)
    popup.geometry("350x240")
    popup.title("Change Password")
    popup.transient(root)

    ctk.CTkLabel(popup, text="Update Account Password", font=("Arial", 18, "bold")).pack(pady=(20, 10))
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
        render_accounts(platform_name)

    ctk.CTkButton(popup, text="Update Password", command=save_password_edit).pack(pady=10)
    popup.wait_visibility()
    popup.grab_set()

def show_account_menu(platform_name, account):
    global active_menu
    if active_menu is not None:
        close_active_menu()
        return

    menu = ctk.CTkToplevel(root)
    menu.geometry("180x210")
    menu.overrideredirect(True)
    menu.geometry(f"+{root.winfo_pointerx()}+{root.winfo_pointery()}")
    active_menu = menu

    ctk.CTkButton(menu, text="Edit Login", command=lambda: [close_active_menu(), open_edit_account_popup(platform_name, account)]).pack(fill="x", padx=5, pady=3)
    ctk.CTkButton(menu, text="Change Password", command=lambda: [close_active_menu(), open_change_account_password_popup(platform_name, account)]).pack(fill="x", padx=5, pady=3)

    def copy_login():
        root.clipboard_clear()
        root.clipboard_append(account["login_id"])
        close_active_menu()
        messagebox.showinfo("Copied", "Login ID copied")

    ctk.CTkButton(menu, text="Copy Login", command=copy_login).pack(fill="x", padx=5, pady=3)

    def copy_password():
        root.clipboard_clear()
        root.clipboard_append(account["password"])
        close_active_menu()
        messagebox.showinfo("Copied", "Password copied")

    ctk.CTkButton(menu, text="Copy Password", command=copy_password).pack(fill="x", padx=5, pady=3)

    def delete_account():
        if messagebox.askyesno("confirm Deletion",f"Are you sure you want to delete the account details for '{account['login_id']}'?"):
         accounts_data[platform_name].remove(account)
         render_accounts(platform_name)
        close_active_menu()
    

    ctk.CTkButton(menu, text="Delete", fg_color="darkred", hover_color="red", command=delete_account).pack(fill="x", padx=5, pady=3)
    menu.bind("<FocusOut>", lambda e: close_active_menu())


# =========================================================
# START WINDOW INSTRUCTION
# =========================================================

show_set_master_window()
root.mainloop()
