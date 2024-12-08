import json
import tkinter as tk
from tkinter import messagebox
from utils.constants import USER_DB_FILE
from PIL import Image, ImageTk

class LoginSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("1920x1080")
        
        frame = tk.Frame(self.root)
        frame.pack()

        canvas = tk.Canvas(frame, width=1920, height=1080,bg='black')
        canvas.pack()

        # Memuat background
        bg_image_path = "assets/login-bg.png" 
        bg_image = Image.open(bg_image_path)
        bg_image = bg_image.resize((1920, 1080), Image.Resampling.LANCZOS)
        self.bg_image_tk = ImageTk.PhotoImage(bg_image)
        canvas.create_image(0, 0, anchor='nw', image=self.bg_image_tk)

        # Memuat logo
        logo_path = "assets/peek-a-job-logo-with-text.png" 
        logo_image = Image.open(logo_path)
        logo_image = logo_image.resize((500, 500), Image.Resampling.LANCZOS)
        self.logo_image_tk = ImageTk.PhotoImage(logo_image)
        canvas.create_image(960, 250, image=self.logo_image_tk) 

        # Username widget
        username_label = tk.Label(self.root, text="Username:", font=("Arial", 18, 'bold'), bg="white")
        username_label.place(relx=0.4, rely=0.4, anchor="center")
        self.username = tk.Entry(self.root, font=("Arial", 14))
        self.username.place(relx=0.55, rely=0.4, anchor="center")

        # Password widget
        password_label = tk.Label(self.root, text="Password:", font=("Arial", 18, 'bold'), bg="white")
        password_label.place(relx=0.4, rely=0.45, anchor="center")
        self.password = tk.Entry(self.root, show="*", font=("Arial", 14))
        self.password.place(relx=0.55, rely=0.45, anchor="center")

        # Tombol Login
        login_button = tk.Button(
            self.root, text="Login", font=("Arial", 16, "bold"), bg="black", fg="white",
            width=15, height=2, command=self.login
        )
        login_button.place(relx=0.5, rely=0.55, anchor="center")

    # fungsi autentikasi login
    def login(self):
        try:
            with open(USER_DB_FILE, "r") as f:
                users = json.load(f)

            username = self.username.get()
            password = self.password.get()

            if username in users and users[username]["password"] == password:
                role = users[username]["role"]
                self.root.destroy()
                
                from applicant_filter_app import ApplicantFilterApp
                main_app = tk.Tk()
                app = ApplicantFilterApp(main_app, username, role)
                main_app.mainloop()
            else:
                messagebox.showerror("Login Failed", "Invalid username or password.")
        except FileNotFoundError:
            messagebox.showerror("Error", "User database not found.")