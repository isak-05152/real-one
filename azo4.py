# ================================
# INSTALL FIRST:
# pip install customtkinter cryptography bcrypt --break-system-packages
# ================================

import os
import sys
import base64
import sqlite3
import bcrypt
import customtkinter as ctk
from tkinter import messagebox
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes


# =========================================================
# DATABASE
# =========================================================

def get_connection():
    conn = sqlite3.connect("password2.db")
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS PLATFORM(
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        PLATFORM_NAME TEXT NOT NULL UNIQUE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ACCOUNT(
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        PLATFORM_ID INTEGER NOT NULL,
        ACCOUNT_IDENTIFIER TEXT NOT NULL,
        PASSWORD TEXT NOT NULL,
        UNIQUE(PLATFORM_ID, ACCOUNT_IDENTIFIER),
        FOREIGN KEY(PLATFORM_ID) REFERENCES PLATFORM(ID) ON DELETE CASCADE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS MASTER_AUTH(
        ID INTEGER PRIMARY KEY,
        PASSWORD_HASH TEXT NOT NULL,
        SALT TEXT NOT NULL,
        ENCRYPTED_DEK TEXT NOT NULL
    )
    """)

    connection.commit()
    connection.close()


# =========================================================
# CRYPTO
# =========================================================

def encrypt_data(password, DEK):
    fernet = Fernet(DEK)
    return fernet.encrypt(password.encode()).decode()

def decrypt_data(encrypted_password, DEK):
    fernet = Fernet(DEK)
    return fernet.decrypt(encrypted_password.encode()).decode()

def encrypt_DEK(DEK, KEK):
    fernet = Fernet(KEK)
    return fernet.encrypt(DEK).decode()

def decrypt_DEK(encrypted_DEK, KEK):
    fernet = Fernet(KEK)
    return fernet.decrypt(encrypted_DEK.encode())


# =========================================================
# MASTER AUTH
# =========================================================

def is_master_setup():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""SELECT PASSWORD_HASH FROM MASTER_AUTH WHERE ID = 1""")
    result = cursor.fetchone()
    connection.close()
    return result

def derive_KEK(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )
    KEK = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return KEK

def setup_master(password):
    connection = get_connection()
    cursor = connection.cursor()

    salt = os.urandom(16)
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    KEK = derive_KEK(password, salt)
    f = Fernet(KEK)
    DEK = Fernet.generate_key()
    encrypted_DEK = f.encrypt(DEK).decode()

    cursor.execute("""
        INSERT INTO MASTER_AUTH (ID, PASSWORD_HASH, SALT, ENCRYPTED_DEK)
        VALUES (?, ?, ?, ?)
        """, (1, hashed_password, salt, encrypted_DEK))

    connection.commit()
    connection.close()

def unlock_system(password):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT PASSWORD_HASH, SALT, ENCRYPTED_DEK FROM MASTER_AUTH WHERE ID = 1")
    result = cursor.fetchone()
    connection.close()

    if result:
        hashed_password, salt, encrypted_DEK = result
        if bcrypt.checkpw(password.encode(), hashed_password.encode()):
            KEK = derive_KEK(password, salt)
            f = Fernet(KEK)
            DEK = f.decrypt(encrypted_DEK.encode())
            return DEK
        else:
            return None
    else:
        print("No master authentication found")
        return None

def change_master_auth(new_master_auth, DEK):
    connection = get_connection()
    cursor = connection.cursor()

    new_salt = os.urandom(16)
    new_KEK = derive_KEK(new_master_auth, new_salt)
    encrypted_new_DEK = encrypt_DEK(DEK, new_KEK)
    hashed_new_master_auth = bcrypt.hashpw(new_master_auth.encode(), bcrypt.gensalt()).decode()

    cursor.execute("""
        UPDATE MASTER_AUTH
        SET PASSWORD_HASH = ?,
            SALT = ?,
            ENCRYPTED_DEK = ?
        """, (hashed_new_master_auth, new_salt, encrypted_new_DEK))

    connection.commit()
    connection.close()
    return True


# =========================================================
# PLATFORM MANAGER
# =========================================================

def add_platform(platform_name):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO PLATFORM (PLATFORM_NAME) VALUES (?)", (platform_name,))
    connection.commit()
    connection.close()

def update_platform(platform_id, new_name):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE PLATFORM SET PLATFORM_NAME = ? WHERE ID = ?", (new_name, platform_id))
    connection.commit()
    connection.close()

def delete_platform(platform_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM PLATFORM WHERE ID = ?", (platform_id,))
    connection.commit()
    connection.close()

def get_platforms():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM PLATFORM")
    platforms = cursor.fetchall()
    connection.close()
    return platforms


# =========================================================
# ACCOUNT MANAGER
# =========================================================

def add_account(platform_id, account_identifier, password, DEK):
    connection = get_connection()
    cursor = connection.cursor()
    encrypted_password = encrypt_data(password, DEK)
    cursor.execute("""
        INSERT INTO ACCOUNT (PLATFORM_ID, ACCOUNT_IDENTIFIER, PASSWORD)
        VALUES (?, ?, ?)
        """, (platform_id, account_identifier, encrypted_password))
    connection.commit()
    connection.close()

def update_account_identifier(new_account_identifier, account_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE ACCOUNT SET ACCOUNT_IDENTIFIER = ? WHERE ID = ?",
                   (new_account_identifier, account_id))
    connection.commit()
    connection.close()

def update_account_password(account_id, new_password, DEK):
    connection = get_connection()
    cursor = connection.cursor()
    encrypted_password = encrypt_data(new_password, DEK)
    cursor.execute("UPDATE ACCOUNT SET PASSWORD = ? WHERE ID = ?",
                   (encrypted_password, account_id))
    connection.commit()
    connection.close()

def delete_account(account_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM ACCOUNT WHERE ID = ?", (account_id,))
    connection.commit()
    connection.close()

def get_accounts(platform_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM ACCOUNT WHERE PLATFORM_ID = ?", (platform_id,))
    accounts = cursor.fetchall()
    connection.close()
    return accounts

def get_account(account_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM ACCOUNT WHERE ID = ?", (account_id,))
    account = cursor.fetchone()
    connection.close()
    return account

def get_decrypted_password(account_id, DEK):
    account = get_account(account_id)
    if not account:
        return None
    return decrypt_data(account[3], DEK)


# =========================================================
# GUI — MAIN WINDOW
# =========================================================

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.geometry("900x600")
root.title("Password Manager")

# Runtime memory (GUI layer only; real data persists in SQLite)
platforms_list = []
accounts_data = {}
active_menu = None
current_viewing_platform = None
DEK = None  # Session key; set after successful login


# =========================================================
# VIEW SWITCHER
# =========================================================

def switch_to_view(view_frame):
    close_active_menu()
    set_master_frame.place_forget()
    login_frame.place_forget()
    platform_main_container.pack_forget()
    account_main_container.pack_forget()

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
# PRE-INITIALIZING FRAMES
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

    setup_master(password)
    show_login_window()

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
    global DEK
    entered_password = login_password_entry.get()
    DEK = unlock_system(entered_password)
    if DEK:
        show_platform_window()
    else:
        messagebox.showerror("Error", "Wrong password")

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
# LOGOUT & CHANGE MASTER PASSWORD
# =========================================================

def logout():
    global DEK
    if messagebox.askyesno("Logout", "Do you want to logout?"):
        DEK = None
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

    def verify_and_change():
        current_pw = password_entry.get()
        verified_DEK = unlock_system(current_pw)
        if not verified_DEK:
            messagebox.showerror("Error", "Incorrect password", parent=popup)
            return

        popup.grab_release()
        popup.destroy()

        new_pw_popup = ctk.CTkToplevel(root)
        new_pw_popup.geometry("350x300")
        new_pw_popup.title("Set New Master Password")
        new_pw_popup.transient(root)

        ctk.CTkLabel(new_pw_popup, text="Set New Master Password", font=("Arial", 18, "bold")).pack(pady=(20, 10))
        new_row = ctk.CTkFrame(new_pw_popup, fg_color="transparent")
        new_row.pack(pady=5)
        new_entry = ctk.CTkEntry(new_row, width=210, placeholder_text="New Password", show="*")
        new_entry.pack(side="left")

        confirm_row = ctk.CTkFrame(new_pw_popup, fg_color="transparent")
        confirm_row.pack(pady=5)
        confirm_entry = ctk.CTkEntry(confirm_row, width=210, placeholder_text="Confirm New Password", show="*")
        confirm_entry.pack(side="left")

        new_pw_visible = [False]

        def toggle_new_pw():
            new_pw_visible[0] = not new_pw_visible[0]
            mask = "" if new_pw_visible[0] else "*"
            new_entry.configure(show=mask)
            confirm_entry.configure(show=mask)

        ctk.CTkButton(new_row, text="👁", width=40, command=toggle_new_pw).pack(side="left", padx=5)
        ctk.CTkButton(confirm_row, text="👁", width=40, command=toggle_new_pw).pack(side="left", padx=5)

        def save_new():
            new_pw = new_entry.get()
            confirm_pw = confirm_entry.get()
            if new_pw == "":
                messagebox.showerror("Error", "Password cannot be empty", parent=new_pw_popup)
                return
            if new_pw != confirm_pw:
                messagebox.showerror("Error", "Passwords do not match", parent=new_pw_popup)
                return
            change_master_auth(new_pw, verified_DEK)
            messagebox.showinfo("Success", "Master password updated")
            new_pw_popup.grab_release()
            new_pw_popup.destroy()

        ctk.CTkButton(new_pw_popup, text="Save", command=save_new).pack(pady=15)
        new_pw_popup.wait_visibility()
        new_pw_popup.grab_set()

    ctk.CTkButton(popup, text="Verify", command=verify_and_change).pack(pady=15)
    popup.wait_visibility()
    popup.grab_set()


# =========================================================
# PLATFORM PANEL
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

def render_platforms():
    for widget in platform_scroll_frame.winfo_children():
        widget.destroy()

    db_platforms = get_platforms()

    if not db_platforms:
        ctk.CTkLabel(platform_scroll_frame, text="No platform added yet", font=("Arial", 18)).pack(pady=30)
        return

    for platform in db_platforms:
        plat_id, plat_name = platform[0], platform[1]
        row = ctk.CTkFrame(platform_scroll_frame, width=500, height=50)
        row.pack(pady=5, padx=100)
        row.pack_propagate(False)

        ctk.CTkButton(
            row, text=plat_name, fg_color="pink", hover_color="pink", text_color="black",
            anchor="w", width=420, height=40,
            command=lambda pid=plat_id, pname=plat_name: open_account_window(pid, pname)
        ).pack(side="left", padx=(10, 5), pady=5)

        ctk.CTkButton(
            row, text="⋮", width=40, height=40,
            command=lambda pid=plat_id, pname=plat_name: show_platform_menu_popup(pid, pname)
        ).pack(side="left", padx=5, pady=5)

ctk.CTkButton(platform_main_container, text="+ Add Platform", fg_color="#8C8C3C",
              hover_color="#8C8C3C", height=40, command=lambda: open_add_platform_popup()).pack(pady=10)


# =========================================================
# PLATFORM POPUPS
# =========================================================

def open_add_platform_popup():
    popup = ctk.CTkToplevel(root)
    popup.geometry("350x200")
    popup.title("Add Platform")
    popup.transient(root)

    ctk.CTkLabel(popup, text="Add Platform", font=("Arial", 20, "bold")).pack(pady=(20, 15))
    entry = ctk.CTkEntry(popup, width=250, fg_color="#8F6F6F", text_color="black",
                         placeholder_text_color="black", placeholder_text="Platform Name")
    entry.pack(pady=10)

    def do_add():
        name = entry.get().strip()
        if not name:
            messagebox.showwarning("Warning", "Platform name cannot be empty", parent=popup)
            return
        try:
            add_platform(name)
        except sqlite3.IntegrityError:
            messagebox.showwarning("Warning", "Platform already exists", parent=popup)
            return
        render_platforms()
        popup.grab_release()
        popup.destroy()

    ctk.CTkButton(popup, text="Add", fg_color="#332F3B", hover_color="#332F3B", command=do_add).pack(pady=20)
    popup.wait_visibility()
    popup.grab_set()

def show_platform_menu_popup(platform_id, platform_name):
    global active_menu
    if active_menu is not None:
        close_active_menu()
        return

    menu = ctk.CTkToplevel(root)
    menu.geometry("120x90")
    menu.overrideredirect(True)
    menu.geometry(f"+{root.winfo_pointerx()}+{root.winfo_pointery()}")
    active_menu = menu

    ctk.CTkButton(menu, text="Edit",
                  command=lambda: [close_active_menu(), open_edit_platform_popup(platform_id, platform_name)]
                  ).pack(fill="x", padx=5, pady=5)
    ctk.CTkButton(menu, text="Delete", fg_color="darkred", hover_color="red",
                  command=lambda: [close_active_menu(), open_delete_platform_popup(platform_id, platform_name)]
                  ).pack(fill="x", padx=5, pady=5)
    menu.bind("<FocusOut>", lambda e: close_active_menu())

def open_edit_platform_popup(platform_id, old_name):
    popup = ctk.CTkToplevel(root)
    popup.geometry("350x180")
    popup.title("Edit Platform")
    popup.transient(root)

    entry = ctk.CTkEntry(popup, width=250)
    entry.insert(0, old_name)
    entry.pack(pady=30)

    def save_edit():
        new_name = entry.get().strip()
        if not new_name:
            messagebox.showwarning("Warning", "Name cannot be empty", parent=popup)
            return
        try:
            update_platform(platform_id, new_name)
        except sqlite3.IntegrityError:
            messagebox.showwarning("Warning", "Platform name already exists", parent=popup)
            return
        render_platforms()
        popup.grab_release()
        popup.destroy()

    ctk.CTkButton(popup, text="Save", command=save_edit).pack(pady=10)
    popup.wait_visibility()
    popup.grab_set()

def open_delete_platform_popup(platform_id, platform_name):
    popup = ctk.CTkToplevel(root)
    popup.geometry("400x260")
    popup.title("Delete Platform")
    popup.transient(root)

    ctk.CTkLabel(popup, text=f"Delete '{platform_name}' ?", font=("Arial", 18)).pack(pady=20)
    ctk.CTkLabel(popup, text=f"NOTE: all accounts inside '{platform_name}' will also be deleted",
                 font=("italics", 10)).pack(pady=10)

    def do_delete():
        delete_platform(platform_id)
        render_platforms()
        popup.grab_release()
        popup.destroy()

    ctk.CTkButton(popup, text="Delete", fg_color="darkred", hover_color="red", command=do_delete).pack(pady=10)
    popup.wait_visibility()
    popup.grab_set()


# =========================================================
# ACCOUNT PANEL
# =========================================================

acc_top_frame = ctk.CTkFrame(account_main_container)
acc_top_frame.pack(fill="x", padx=10, pady=10)

ctk.CTkButton(acc_top_frame, text="<--", fg_color="#1C3327", hover_color="#1C3327",
              command=show_platform_window).pack(side="left", padx=5)
account_title_label = ctk.CTkLabel(acc_top_frame, text="", font=("Arial", 26, "bold"))
account_title_label.pack(side="left", padx=20)
ctk.CTkButton(acc_top_frame, text="change M-password", command=open_change_master_popup).pack(side="right", padx=5)
ctk.CTkButton(acc_top_frame, text="⏻", fg_color="#F20A0A", hover_color="#F20A0A", width=40,
              command=logout).pack(side="right", padx=5)

ctk.CTkFrame(account_main_container, height=2).pack(fill="x", padx=20)

account_scroll_frame = ctk.CTkScrollableFrame(account_main_container, width=700, height=400)
account_scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)

def open_account_window(platform_id, platform_name):
    global current_viewing_platform
    current_viewing_platform = (platform_id, platform_name)
    account_title_label.configure(text=platform_name)
    switch_to_view(account_main_container)
    render_accounts(platform_id, platform_name)

def render_accounts(platform_id, platform_name):
    for widget in account_scroll_frame.winfo_children():
        widget.destroy()

    accounts = get_accounts(platform_id)

    if not accounts:
        ctk.CTkLabel(account_scroll_frame, text="No account added yet", font=("Arial", 18)).pack(pady=30)
        return

    for account in accounts:
        acc_id, _, acc_identifier, acc_enc_pw = account
        row = ctk.CTkFrame(account_scroll_frame)
        row.pack(fill="x", pady=5)

        ctk.CTkLabel(row, text=acc_identifier, width=250, anchor="w").pack(side="left", padx=10)
        password_label = ctk.CTkLabel(row, text="••••••", width=150)
        password_label.pack(side="left")

        def toggle_password(lbl=password_label, aid=acc_id):
            if lbl.cget("text") == "••••••":
                decrypted = get_decrypted_password(aid, DEK)
                lbl.configure(text=decrypted if decrypted else "Error")
            else:
                lbl.configure(text="••••••")

        ctk.CTkButton(row, text="👁  ", width=40, command=toggle_password).pack(side="left", padx=5)
        ctk.CTkButton(row, text="⋮", width=40,
                      command=lambda aid=acc_id, aname=acc_identifier, pid=platform_id, pname=platform_name:
                          show_account_menu_popup(pid, pname, aid, aname)
                      ).pack(side="left", padx=5)

ctk.CTkButton(account_main_container, text="+ Add Account", fg_color="#D9367A", hover_color="#D9367A",
              command=lambda: open_add_account_popup(*current_viewing_platform)).pack(pady=10)


# =========================================================
# ACCOUNT POPUPS
# =========================================================

def open_add_account_popup(platform_id, platform_name):
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

    def do_add():
        login_id = login_entry.get().strip()
        password = password_entry.get().strip()
        if not login_id or not password:
            messagebox.showwarning("Warning", "Fields cannot be empty", parent=popup)
            return
        try:
            add_account(platform_id, login_id, password, DEK)
        except sqlite3.IntegrityError:
            messagebox.showwarning("Warning", "Account identifier already exists", parent=popup)
            return
        popup.grab_release()
        popup.destroy()
        render_accounts(platform_id, platform_name)

    ctk.CTkButton(popup, text="Add", fg_color="#332F3B", hover_color="#332F3B", command=do_add).pack(pady=15)
    popup.wait_visibility()
    popup.grab_set()

def show_account_menu_popup(platform_id, platform_name, account_id, account_identifier):
    global active_menu
    if active_menu is not None:
        close_active_menu()
        return

    menu = ctk.CTkToplevel(root)
    menu.geometry("180x210")
    menu.overrideredirect(True)
    menu.geometry(f"+{root.winfo_pointerx()}+{root.winfo_pointery()}")
    active_menu = menu

    ctk.CTkButton(menu, text="Edit Login",
                  command=lambda: [close_active_menu(),
                                   open_edit_account_popup(platform_id, platform_name, account_id, account_identifier)]
                  ).pack(fill="x", padx=5, pady=3)
    ctk.CTkButton(menu, text="Change Password",
                  command=lambda: [close_active_menu(),
                                   open_change_account_password_popup(platform_id, platform_name, account_id)]
                  ).pack(fill="x", padx=5, pady=3)

    def copy_login():
        root.clipboard_clear()
        root.clipboard_append(account_identifier)
        close_active_menu()
        messagebox.showinfo("Copied", "Login ID copied")

    def copy_password():
        pw = get_decrypted_password(account_id, DEK)
        root.clipboard_clear()
        root.clipboard_append(pw or "")
        close_active_menu()
        messagebox.showinfo("Copied", "Password copied")

    def do_delete():
        if messagebox.askyesno("Confirm Deletion",
                               f"Delete account '{account_identifier}'?"):
            delete_account(account_id)
            render_accounts(platform_id, platform_name)
        close_active_menu()

    ctk.CTkButton(menu, text="Copy Login", command=copy_login).pack(fill="x", padx=5, pady=3)
    ctk.CTkButton(menu, text="Copy Password", command=copy_password).pack(fill="x", padx=5, pady=3)
    ctk.CTkButton(menu, text="Delete", fg_color="darkred", hover_color="red",
                  command=do_delete).pack(fill="x", padx=5, pady=3)
    menu.bind("<FocusOut>", lambda e: close_active_menu())

def open_edit_account_popup(platform_id, platform_name, account_id, old_identifier):
    popup = ctk.CTkToplevel(root)
    popup.geometry("400x220")
    popup.title("Edit Account")
    popup.transient(root)

    ctk.CTkLabel(popup, text="Edit Login ID", font=("Arial", 20, "bold")).pack(pady=(20, 15))
    login_entry = ctk.CTkEntry(popup, width=280)
    login_entry.insert(0, old_identifier)
    login_entry.pack(pady=10)

    def save_edit():
        new_login = login_entry.get().strip()
        if not new_login:
            messagebox.showwarning("Warning", "Login ID cannot be empty", parent=popup)
            return
        update_account_identifier(new_login, account_id)
        popup.grab_release()
        popup.destroy()
        render_accounts(platform_id, platform_name)

    ctk.CTkButton(popup, text="Save Changes", command=save_edit).pack(pady=15)
    popup.wait_visibility()
    popup.grab_set()

def open_change_account_password_popup(platform_id, platform_name, account_id):
    popup = ctk.CTkToplevel(root)
    popup.geometry("350x240")
    popup.title("Change Password")
    popup.transient(root)

    ctk.CTkLabel(popup, text="Update Account Password", font=("Arial", 18, "bold")).pack(pady=(20, 10))
    password_entry = ctk.CTkEntry(popup, width=250, show="•")
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

    def save_password():
        new_password = password_entry.get().strip()
        if not new_password:
            messagebox.showwarning("Warning", "Password cannot be empty", parent=popup)
            return
        update_account_password(account_id, new_password, DEK)
        popup.grab_release()
        popup.destroy()
        render_accounts(platform_id, platform_name)

    ctk.CTkButton(popup, text="Update Password", command=save_password).pack(pady=10)
    popup.wait_visibility()
    popup.grab_set()


# =========================================================
# STARTUP
# =========================================================

def startup():
    init_database()
    if is_master_setup():
        show_login_window()
    else:
        show_set_master_window()

startup()
root.mainloop()
