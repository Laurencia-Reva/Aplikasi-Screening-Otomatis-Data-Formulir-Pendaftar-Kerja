import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from preview_data import PreviewWindow
from user_management import UserManagement
from login import LoginSystem
from utils.constants import OUTPUT_FILE
from PIL import Image, ImageTk

class ApplicantFilterApp:
    def __init__(self, root, username, role):
        self.root = root
        self.username = username
        self.role = role
        self.root.title("Job Applicant Filter")
        self.root.geometry("1920x1080")
        self.root.configure(bg="#f7c1d7")

        self.canvas = tk.Canvas(self.root, width=1920, height=1080)
        self.canvas.pack(fill="both", expand=True)

        # Load UI background 
        bg_image = Image.open("assets/main-app-bg.png") 
        bg_image = bg_image.resize((1920, 1080), Image.Resampling.LANCZOS)
        self.bg_image_tk = ImageTk.PhotoImage(bg_image)

        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image_tk)

        self.min_height = tk.IntVar(value=0)
        self.min_education = tk.IntVar(value=0)
        self.min_age = tk.IntVar(value=0)
        self.max_age = tk.IntVar(value=100)
        self.eyesight_allowed = tk.BooleanVar(value=True)
        self.keterangan_loker = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        # Teks welcome
        tk.Label(self.root, text=f"Welcome, {self.username} 🤚", font=("Helvetica", 38, "bold"), background="#001c70", foreground='white').place(relx=0.5, rely=0.180, anchor="center")

        # Keterangan Loker
        tk.Label(self.root, text="Keterangan Loker:", font=("Arial", 20), background="#f8f7f1").place(relx=0.4, rely=0.4, anchor="center")
        tk.Entry(self.root, textvariable=self.keterangan_loker, font=("Arial", 16)).place(relx=0.55, rely=0.4, anchor="center")

        # Sisi Kiri: Minimum Height, Minimum Age, Maximum Age
        tk.Label(self.root, text="Minimum Height (cm):", font=("Arial", 16), background="#f8f7f1").place(relx=0.25, rely=0.5, anchor="center")
        tk.Entry(self.root, textvariable=self.min_height, font=("Arial", 16)).place(relx=0.4, rely=0.5, anchor="center")

        tk.Label(self.root, text="Minimum Age:", font=("Arial", 16), background="#f8f7f1").place(relx=0.25, rely=0.55, anchor="center")
        tk.Entry(self.root, textvariable=self.min_age, font=("Arial", 16)).place(relx=0.4, rely=0.55, anchor="center")

        tk.Label(self.root, text="Maximum Age:", font=("Arial", 16), background="#f8f7f1").place(relx=0.25, rely=0.6, anchor="center")
        tk.Entry(self.root, textvariable=self.max_age, font=("Arial", 16)).place(relx=0.4, rely=0.6, anchor="center")

        # Sisi Kanan: Minimum Education Level, Eyesight Problem Allowed
        tk.Label(self.root, text="Minimum Education Level:", font=("Arial", 16), background="#f8f7f1").place(relx=0.6, rely=0.5, anchor="center")
        education_options = [("SMP", 0), ("SMA", 1), ("S1", 2)]
        self.education_menu = ttk.Combobox(self.root, values=[opt[0] for opt in education_options], state="readonly", font=("Arial", 16))
        self.education_menu.bind("<<ComboboxSelected>>", lambda event: self.min_education.set(dict(education_options)[self.education_menu.get()]))
        self.education_menu.place(relx=0.75, rely=0.5, anchor="center")

        tk.Label(self.root, text="Eyesight Problem Allowed:", font=("Arial", 16), background="#f8f7f1").place(relx=0.6, rely=0.55, anchor="center")
        tk.Checkbutton(self.root, variable=self.eyesight_allowed, font=("Arial", 16)).place(relx=0.75, rely=0.55, anchor="center")

        # Tombol Preview Data
        tk.Button(self.root, text="Preview Data", command=self.preview_data, width=20, font=("Arial", 14, "bold"), bg="#5273d6", fg='white', relief="flat").place(relx=0.7, rely=0.3, anchor="center")
        
        # Tombol management akun 
        tk.Button(self.root, text="Manage Users", command=self.manage_users, width=20, font=("Arial", 14, "bold"), bg="#5273d6", fg='white', relief="flat").place(relx=0.85, rely=0.3, anchor="center")

        # Tombol Load File and Apply Filter
        tk.Button(self.root, text="Load File and Apply Filter", command=self.load_file, width=25, font=("Arial", 16, "bold"), bg="#5273d6", fg='white', relief="flat").place(relx=0.5, rely=0.8, anchor="center")

        # Tombol Logout
        tk.Button(self.root, text=" ⛔\nLogout", command=self.logout, width=10, font=("Arial", 16, "bold"), bg="#ff6961", fg='white', relief="flat").place(relx=0.95, rely=0.025, anchor="ne")

    # Fungsi untuk membaca data yang di load
    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx")])
        if not file_path:
            return

        try:
            if file_path.endswith('.csv'):
                data = pd.read_csv(file_path)
            else:
                data = pd.read_excel(file_path)

            education_map = {"SMP": 0, "SMA": 1, "S1": 2}
            data['Education'] = data['Education'].map(education_map).fillna(-1).astype(int)

            data['Admin'] = self.username
            data['Keterangan Loker'] = self.keterangan_loker.get()

            data['Status'] = data.apply(self.evaluate_applicant, axis=1)

            decode_map = {0: "SMP", 1: "SMA", 2: "S1"}
            data['Education'] = data['Education'].map(decode_map)

            self.save_to_master_file(data)

            messagebox.showinfo("Success", "Data has been filtered and saved!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    # Fitur untuk menyimpan hasil seleksi ke database
    def save_to_master_file(self, data):
        if os.path.exists(OUTPUT_FILE):
            existing_data = pd.read_excel(OUTPUT_FILE)
            combined_data = pd.concat([existing_data, data], ignore_index=True)
        else:
            combined_data = data
        combined_data.to_excel(OUTPUT_FILE, index=False)
    
    # Fungsi untuk seleksi applicant sesuai input parameter
    def evaluate_applicant(self, applicant):
        try:
            height = applicant.get("Height", 0)
            education = applicant.get("Education", -1)
            age = applicant.get("Age", 0)
            eyesight_problem = applicant.get("Eyesight Problem", "").lower() == "yes"

            if (height >= self.min_height.get() and
                education >= self.min_education.get() and
                (self.min_age.get() == 0 or age >= self.min_age.get()) and
                (self.max_age.get() == 100 or age <= self.max_age.get()) and
                (eyesight_problem == False or self.eyesight_allowed.get())):
                return "LOLOS"
            else:
                return "TIDAK LOLOS"
        except KeyError as e:
            messagebox.showerror("Error", f"Missing required column: {e}")
            return "TIDAK LOLOS"

    # Fungsi untuk membuka app preview data
    def preview_data(self):
        try:
            if not os.path.exists(OUTPUT_FILE):
                messagebox.showinfo("No Data", "No data available to preview.")
                return

            data = pd.read_excel(OUTPUT_FILE)
            PreviewWindow(self.root, data)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Fungsi untuk autentikasi perizinan dan membuka manage user
    def manage_users(self):
        if self.role != "Head Of HR":
            messagebox.showerror("Access Denied", "Only Head of HR can manage users.")
            return
        
        UserManagement(self.root)

    # Fungsi untuk logout -> kembali ke laman login
    def logout(self):
        self.root.destroy()
        login_window = tk.Tk()
        login_system = LoginSystem(login_window)
        login_window.mainloop()