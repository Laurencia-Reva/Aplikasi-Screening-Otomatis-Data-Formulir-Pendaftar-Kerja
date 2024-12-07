import os
import json
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, Canvas, Frame
import pandas as pd
from PIL import Image, ImageTk

# Database pengguna (users.json)
USER_DB_FILE = "users.json"

# Kelas Login System
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
                main_app = tk.Tk()
                app = ApplicantFilterApp(main_app, username, role)
                main_app.mainloop()
            else:
                messagebox.showerror("Login Failed", "Invalid username or password.")
        except FileNotFoundError:
            messagebox.showerror("Error", "User database not found.")

# Aplikasi seleksi utama
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
        output_file = "output/output_database.xlsx"
        if os.path.exists(output_file):
            existing_data = pd.read_excel(output_file)
            combined_data = pd.concat([existing_data, data], ignore_index=True)
        else:
            combined_data = data
        combined_data.to_excel(output_file, index=False)
    
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
            output_file = "output/output_database.xlsx"
            if not os.path.exists(output_file):
                messagebox.showinfo("No Data", "No data available to preview.")
                return

            data = pd.read_excel(output_file)
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

# Laman Preview Data 
class PreviewWindow:
    def __init__(self, parent, data):
        self.window = tk.Toplevel(parent)
        self.window.title("Preview Data")
        self.window.geometry("1920x1080")
        self.data = data.copy()  
        self.filtered_data = data.copy() 
        self.create_widgets()

    # Fungsi mendefinisikan widget pada UI
    def create_widgets(self):
        filter_frame = ttk.Frame(self.window)
        filter_frame.pack(pady=10, fill=tk.X)

        self.status_filter = tk.StringVar(value="All")
        self.job_filter = tk.StringVar(value="All")
        self.education_filter= tk.StringVar(value="All")
        self.min_height_filter = tk.IntVar(value=0)
        self.max_height_filter = tk.IntVar(value=300)
        self.min_age_filter = tk.IntVar(value=0)
        self.max_age_filter = tk.IntVar(value=150)

        # Filter Status
        ttk.Label(filter_frame, text="Filter by Status:").grid(row=0, column=0, padx=5)
        ttk.Combobox(filter_frame, textvariable=self.status_filter, values=["All", "LOLOS", "TIDAK LOLOS"]).grid(row=0, column=1, padx=5)

        # Filter Job Description
        unique_jobs = ["All"] + self.data["Keterangan Loker"].dropna().unique().tolist()
        ttk.Label(filter_frame, text="Filter by Job Description:").grid(row=0, column=2, padx=5)
        ttk.Combobox(filter_frame, textvariable=self.job_filter, values=unique_jobs).grid(row=0, column=3, padx=5)

        # Filter Education
        unique_education = ["All"] + self.data["Education"].dropna().unique().tolist()
        ttk.Label(filter_frame, text="Filter by Education:").grid(row=0, column=4, padx=5)
        ttk.Combobox(filter_frame, textvariable=self.education_filter, values=unique_education).grid(row=0, column=5, padx=5)

        # Filter Height
        ttk.Label(filter_frame, text="Min Height (cm):").grid(row=1, column=0, padx=5)
        ttk.Entry(filter_frame, textvariable=self.min_height_filter, width=10).grid(row=1, column=1, padx=5)
        ttk.Label(filter_frame, text="Max Height (cm):").grid(row=1, column=2, padx=5)
        ttk.Entry(filter_frame, textvariable=self.max_height_filter, width=10).grid(row=1, column=3, padx=5)

        # Filter Age
        ttk.Label(filter_frame, text="Min Age:").grid(row=2, column=0, padx=5)
        ttk.Entry(filter_frame, textvariable=self.min_age_filter, width=10).grid(row=2, column=1, padx=5)
        ttk.Label(filter_frame, text="Max Age:").grid(row=2, column=2, padx=5)
        ttk.Entry(filter_frame, textvariable=self.max_age_filter, width=10).grid(row=2, column=3, padx=5)

        ttk.Button(filter_frame, text="Apply Filter", command=self.apply_filter).grid(row=3, column=0, columnspan=4, pady=10)

        # Tabel Preview Data
        table_frame = ttk.Frame(self.window)
        table_frame.pack(expand=True, fill=tk.BOTH)

        self.tree = ttk.Treeview(table_frame, columns=list(self.data.columns), show="headings")
        for col in self.data.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=100)
        self.tree.pack(expand=True, fill=tk.BOTH)

        self.populate_tree(self.filtered_data)

    def populate_tree(self, data):
        # isi data setelah filter
        self.tree.delete(*self.tree.get_children())
        for _, row in data.iterrows():
            self.tree.insert("", "end", values=list(row))

    def apply_filter(self):
        # Aplikasikan filter data data preview
        try:
            filtered_data = self.data.copy()

            if self.status_filter.get() != "All":
                filtered_data = filtered_data[filtered_data["Status"] == self.status_filter.get()]

            if self.job_filter.get() != "All":
                filtered_data = filtered_data[filtered_data["Keterangan Loker"] == self.job_filter.get()]

            if self.education_filter.get() != "All":
                filtered_data = filtered_data[filtered_data["Education"] == self.education_filter.get()]

            filtered_data = filtered_data[
                (filtered_data["Height"] >= self.min_height_filter.get()) &
                (filtered_data["Height"] <= self.max_height_filter.get())
            ]

            filtered_data = filtered_data[
                (filtered_data["Age"] >= self.min_age_filter.get()) &
                (filtered_data["Age"] <= self.max_age_filter.get())
            ]

            self.filtered_data = filtered_data
            self.populate_tree(self.filtered_data)

        except Exception as e:
            messagebox.showerror("Error", str(e))

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

if __name__ == "__main__":
    root = tk.Tk()
    login_app = LoginSystem(root)
    root.mainloop()