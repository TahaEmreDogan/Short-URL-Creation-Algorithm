from db import user_register, user_login, shorten_links, get_user_links
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk
import pyperclip

current_user = None
current_user_id = None

def load_user_links():
    for row in links_tree.get_children():
        links_tree.delete(row)
    if current_user:
        links = get_user_links(current_user)
        for original, shortened in links:
            links_tree.insert('', 'end', values=(original, shortened))

def register():
    user_name = entry_username.get()
    user_password = entry_password.get()
    if not user_name or not user_password:
        messagebox.showerror("Error", "Please fill all fields!")
        return
    register_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    success = user_register(user_name, user_password, register_date)
    if success:
        messagebox.showinfo("Success", "Registration successful!")
        entry_username.delete(0, tk.END)
        entry_password.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Registration failed!")

def login():
    global current_user, current_user_id
    user_name = entry_username.get()
    user_password = entry_password.get()
    if not user_name or not user_password:
        messagebox.showerror("Error", "Please fill all fields!")
        return
    success = user_login(user_name, user_password)
    if success:
        from db import db_connect
        connection = db_connect()
        cursor = connection.cursor()
        cursor.execute("SELECT user_id FROM users WHERE user_name = %s", (user_name,))
        user = cursor.fetchone()
        cursor.close()
        connection.close()
        if user:
            current_user_id = user[0]
        else:
            current_user_id = None
        current_user = user_name
        messagebox.showinfo("Login", "Login successful!")
        entry_username.delete(0, tk.END)
        entry_password.delete(0, tk.END)
        notebook.hide(user_frame)
        notebook.select(url_frame)
        user_box_var.set(f"👤 {current_user}")
        user_box_label.place(relx=1.0, rely=0.0, anchor="ne")
        logout_btn.place(relx=0.85, rely=0.0, anchor="ne")
        load_user_links()
    else:
        messagebox.showerror("Login", "Login failed!")

def copy_short_url():
    short_url = short_url_var.get()
    if short_url:
        short_url_entry.config(state='normal')
        short_url_entry.selection_range(0, tk.END)
        short_url_entry.focus_set()
        messagebox.showinfo("Selected", "Shortened URL selected, you can copy it with Ctrl+C!")

def shorten_url():
    if not current_user or not current_user_id:
        messagebox.showerror("Error", "Please login first!")
        return
    original_url = entry_url.get()
    if not original_url:
        messagebox.showerror("Error", "Please enter a URL!")
        return
    shortened = shorten_links(current_user_id, original_url, "")
    if shortened:
        messagebox.showinfo("URL Shortened", f"Shortened URL: {shortened}")
        entry_url.delete(0, tk.END)
        short_url_var.set(shortened)
        load_user_links()
    else:
        messagebox.showerror("Error", "URL shortening failed!")

def logout():
    global current_user, current_user_id
    current_user = None
    current_user_id = None
    user_box_var.set("")
    user_box_label.place_forget()
    logout_btn.place_forget()
    for row in links_tree.get_children():
        links_tree.delete(row)
    notebook.add(user_frame, text="👤 User Management")
    notebook.select(user_frame)

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

    user_box_var = tk.StringVar()
    user_box_label = ttk.Label(url_frame, textvariable=user_box_var, style='Header.TLabel', anchor="e")
    user_box_label.place_forget()

    logout_btn = ttk.Button(url_frame, text="Logout", style='Primary.TButton', command=logout)
    logout_btn.place_forget()

    links_tree = ttk.Treeview(url_frame, columns=("Original", "Shortened"), show="headings", height=8)
    links_tree.heading("Original", text="Original URL")
    links_tree.heading("Shortened", text="Shortened URL")
    links_tree.column("Original", width=250)
    links_tree.column("Shortened", width=180)
    links_tree.pack(pady=10, padx=10, anchor="n")

    short_url_var = tk.StringVar()
    short_url_entry = ttk.Entry(url_frame, textvariable=short_url_var, width=40, font=('Arial', 10), state='normal')
    short_url_entry.pack(pady=(0, 5))
    copy_btn = ttk.Button(url_frame, text="Copy", command=copy_short_url, style='Primary.TButton')
    copy_btn.pack(pady=(0, 10))

    root.mainloop()
