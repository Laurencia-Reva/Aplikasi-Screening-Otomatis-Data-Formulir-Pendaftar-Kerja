import os
import tkinter as tk
from tkinter import messagebox, ttk
import json
from PIL import Image, ImageTk


class UserManagement:
    def __init__(self, parent):
        self.root = tk.Toplevel(parent)
        self.root.title("Manage Users")
        self.root.geometry("1920x1080")
        self.root.configure(bg="#f7c1d7")

        self.load_users()

        self.canvas = tk.Canvas(self.root, width=1920, height=1080)
        self.canvas.pack(fill="both", expand=True)

        bg_image = Image.open("assets/user-management-bg.png") 
        bg_image = bg_image.resize((1920, 1080), Image.Resampling.LANCZOS)
        self.bg_image_tk = ImageTk.PhotoImage(bg_image)

        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image_tk)

        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.role = tk.StringVar()

        self.create_widgets()

    def load_users(self):
        if os.path.exists("users.json"):
            with open("users.json", "r") as f:
                self.users = json.load(f)
        else:
            self.users = {}

    def create_widgets(self):
        # UI untuk penambahan akun (sisi kiri)
        tk.Label(self.root, text="Username:", background="white", font=("Arial", 18)).place(relx=0.15, rely=0.25, anchor="center")
        tk.Entry(self.root, textvariable=self.username, font=("Arial", 18), width=30).place(relx=0.3, rely=0.25, anchor="center")

        tk.Label(self.root, text="Password:", background="white", font=("Arial", 18)).place(relx=0.15, rely=0.35, anchor="center")
        tk.Entry(self.root, textvariable=self.password, show="*", font=("Arial", 18), width=30).place(relx=0.3, rely=0.35, anchor="center")

        tk.Label(self.root, text="Role:", background="white", font=("Arial", 18)).place(relx=0.15, rely=0.45, anchor="center")
        role_options = ["Staff", "Head Of HR", "Intern"]
        self.role = ttk.Combobox(self.root, values=role_options, font=("Arial", 18), state="readonly")
        self.role.place(relx=0.3, rely=0.45, anchor="center")

        tk.Button(self.root, text="Add User", command=self.add_user, font=("Arial", 18, "bold"), bg="#5273d6", fg="white", relief="flat", width=20).place(relx=0.25, rely=0.6, anchor="center")

        # UI untuk mengahpus akun (sisi kanan)
        tk.Label(self.root, text="Existing Users:", background="white", font=("Arial", 18), bg="#5273d6", fg="white").place(relx=0.587, rely=0.25, anchor="center")

        self.user_listbox = tk.Listbox(self.root, font=("Arial", 16), height=11, width=50)
        self.user_listbox.place(relx=0.7, rely=0.275, anchor="n")

        tk.Button(self.root, text="Delete User", command=self.delete_user, font=("Arial", 18, "bold"), bg="#ff6961", fg="white", relief="flat", width=20).place(relx=0.7, rely=0.6, anchor="center")

        self.populate_user_list()

    # Fungsi untuk menampilkan list akun yang ada
    def populate_user_list(self):
        self.user_listbox.delete(0, tk.END)
        for user in self.users:
            self.user_listbox.insert(tk.END, f"{user} - {self.users[user]['role']}")

    # Fungsi untuk menambahkan user ke dalam database users.json 
    def add_user(self):
        username = self.username.get()
        password = self.password.get()
        role = self.role.get()

        if username and password and role:
            self.users[username] = {"password": password, "role": role}
            with open("users.json", "w") as f:
                json.dump(self.users, f)
            self.populate_user_list()
            messagebox.showinfo("Success", "User added successfully.")
        else:
            messagebox.showerror("Error", "All fields are required.")

    # Fungsi menghapus akun pada users.json
    def delete_user(self):
        selected_user = self.user_listbox.curselection()
        if selected_user:
            user = self.user_listbox.get(selected_user).split(" ")[0]
            del self.users[user]
            with open("users.json", "w") as f:
                json.dump(self.users, f)
            self.populate_user_list()
            messagebox.showinfo("Success", "User deleted successfully.")
        else:
            messagebox.showerror("Error", "No user selected.")