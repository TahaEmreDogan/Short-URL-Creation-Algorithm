from db import user_register, user_login
from datetime import datetime
import tkinter as tk
from tkinter import messagebox


def register():
    user_name = entry_username.get()
    user_password = entry_password.get()
    register_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    success = user_register(user_name, user_password, register_date)
    if success:
        messagebox.showinfo("Successful", "Registration successful")
    else:
        messagebox.showerror("Error", "Registration failed.")

def login():
    user_name = entry_username.get()
    user_password = entry_password.get()
    login_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    success = user_login(user_name, user_password, login_date)
    if success:
        messagebox.showinfo("Login", "Login successful")
    else:
        messagebox.showerror("Login", "Login failed.")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("User Interface")
    root.geometry("300x250")

    label_username = tk.Label(root, text="User Name:")
    label_username.pack(pady=(20, 0))
    entry_username = tk.Entry(root)
    entry_username.pack()

    label_password = tk.Label(root, text="Password:")
    label_password.pack(pady=(10, 0))
    entry_password = tk.Entry(root, show="*")
    entry_password.pack()

    btn_register = tk.Button(root, text="Register", command=register)
    btn_register.pack(pady=(20, 5))

    btn_login = tk.Button(root, text="Login", command=login)
    btn_login.pack(pady=(0, 20))

    root.mainloop()
