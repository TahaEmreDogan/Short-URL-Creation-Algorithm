from db import user_register, user_login, shorten_links
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk

def register():
    user_name = entry_username.get()
    user_password = entry_password.get()
    if not user_name or not user_password:
        messagebox.showerror("Error", "Please fill all fields!")
        return
    register_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    success = user_register(user_name, user_password, register_date)
    if success:
        messagebox.showinfo("Successful", "Registration successful!")
        entry_username.delete(0, tk.END)
        entry_password.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Registration failed!")

def login():
    user_name = entry_username.get()
    user_password = entry_password.get()
    if not user_name or not user_password:
        messagebox.showerror("Error", "Please fill all fields!")
        return
    success = user_login(user_name, user_password)
    if success:
        messagebox.showinfo("Login", "Login successful!")
        entry_username.delete(0, tk.END)
        entry_password.delete(0, tk.END)
    else:
        messagebox.showerror("Login", "Login failed!")

def shorten_url():
    original_url = entry_url.get()
    if not original_url:
        messagebox.showerror("Error", "Please enter a URL!")
        return
    shortened = shorten_links(original_url, "")
    if shortened:
        messagebox.showinfo("URL Shortened", f"Shortened URL: {shortened}")
        entry_url.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "URL shortening failed!")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("ShortURL - User Interface")
    root.geometry("500x600")
    root.configure(bg='#f0f0f0')

    style = ttk.Style()
    style.theme_use('clam')
    style.configure('Title.TLabel', font=('Arial', 18, 'bold'), foreground='#2c3e50')
    style.configure('Header.TLabel', font=('Arial', 12, 'bold'), foreground='#34495e')
    style.configure('Success.TButton', background='#27ae60', foreground='white')
    style.configure('Primary.TButton', background='#3498db', foreground='white')

    main_frame = ttk.Frame(root)
    main_frame.pack(pady=20, padx=20, fill="both", expand=True)

    title_label = ttk.Label(main_frame, text="ShortURL Application", style='Title.TLabel')
    title_label.pack(pady=(0, 20))

    notebook = ttk.Notebook(main_frame)
    notebook.pack(fill="both", expand=True, pady=10)

    user_frame = ttk.Frame(notebook)
    notebook.add(user_frame, text="👤 User Management")

    user_title = ttk.Label(user_frame, text="User Management", style='Title.TLabel')
    user_title.pack(pady=20)

    username_label = ttk.Label(user_frame, text="Username:", style='Header.TLabel')
    username_label.pack(pady=(10, 5))
    entry_username = ttk.Entry(user_frame, width=35, font=('Arial', 10))
    entry_username.pack(pady=(0, 15))

    password_label = ttk.Label(user_frame, text="Password:", style='Header.TLabel')
    password_label.pack(pady=(10, 5))
    entry_password = ttk.Entry(user_frame, width=35, show="*", font=('Arial', 10))
    entry_password.pack(pady=(0, 20))

    btn_frame = ttk.Frame(user_frame)
    btn_frame.pack(pady=10)

    register_btn = ttk.Button(btn_frame, text="📝 Register", command=register, style='Success.TButton')
    register_btn.pack(side=tk.LEFT, padx=10)

    login_btn = ttk.Button(btn_frame, text="🔐 Login", command=login, style='Primary.TButton')
    login_btn.pack(side=tk.LEFT, padx=10)

    url_frame = ttk.Frame(notebook)
    notebook.add(url_frame, text="🔗 URL Shortener")

    url_title = ttk.Label(url_frame, text="URL Shortener", style='Title.TLabel')
    url_title.pack(pady=20)

    url_label = ttk.Label(url_frame, text="Enter URL to shorten:", style='Header.TLabel')
    url_label.pack(pady=(10, 5))
    
    entry_url = ttk.Entry(url_frame, width=50, font=('Arial', 10))
    entry_url.pack(pady=(0, 20))

    shorten_btn = ttk.Button(url_frame, text="✂️ Shorten URL", command=shorten_url, style='Success.TButton')
    shorten_btn.pack(pady=10)

    instructions = ttk.Label(url_frame, text="Enter a long URL and get a short, shareable link!", 
                           font=('Arial', 9), foreground='#7f8c8d')
    instructions.pack(pady=20)

    root.mainloop()
