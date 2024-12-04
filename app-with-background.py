import os
import json
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import pandas as pd

# Database pengguna (users.json)
USER_DB_FILE = "users.json"

# Kelas Login System
class LoginSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("300x200")
        self.root.configure(bg="#f7c1d7")

        # Memuat gambar background asli
        self.bg_image_original = Image.open("background_canva.png")  # Ganti dengan path gambar Anda
        self.bg_photo = ImageTk.PhotoImage(self.bg_image_original)

        # Menambahkan label background
        self.bg_label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.place(relwidth=1, relheight=1)

        # Bind resize event
        self.root.bind("<Configure>", self.resize_background)

        # Form elemen login
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        ttk.Label(self.root, text="Username:").grid(row=0, column=0, pady=10, padx=10, sticky="w")
        ttk.Entry(self.root, textvariable=self.username).grid(row=0, column=1, pady=10, padx=10)

        ttk.Label(self.root, text="Password:").grid(row=1, column=0, pady=10, padx=10, sticky="w")
        ttk.Entry(self.root, textvariable=self.password, show="*").grid(row=1, column=1, pady=10, padx=10)

        ttk.Button(self.root, text="Login", command=self.login).grid(row=2, column=0, columnspan=2, pady=10)

    def resize_background(self, event):
        # Resize gambar sesuai ukuran jendela
        new_width = event.width
        new_height = event.height

        # Resize gambar original ke ukuran baru
        resized_image = self.bg_image_original.resize((new_width, new_height), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(resized_image)

        # Update label gambar
        self.bg_label.config(image=self.bg_photo)

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
        self.root.geometry("400x550")
        self.root.configure(bg="#f7c1d7")

        # Memuat gambar background asli
        self.original_bg_image = Image.open("background_canva.png")  # Ganti dengan path gambar Anda

        # Membuat tk.PhotoImage untuk digunakan sebagai background
        self.bg_photo = ImageTk.PhotoImage(self.original_bg_image)
        self.bg_label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.place(relwidth=1, relheight=1)

        # Bind untuk resize window
        self.root.bind("<Configure>", self.resize_background)

        # Configuration Variables
        self.min_height = tk.IntVar(value=0)
        self.min_education = tk.IntVar(value=0)
        self.min_age = tk.IntVar(value=0)
        self.max_age = tk.IntVar(value=100)
        self.eyesight_allowed = tk.BooleanVar(value=True)
        self.keterangan_loker = tk.StringVar()

        self.create_widgets()

    def resize_background(self, event):
        """Menyesuaikan ukuran background sesuai ukuran jendela."""
        new_width = event.width
        new_height = event.height

        resized_image = self.original_bg_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(resized_image)
        self.bg_label.config(image=self.bg_photo)

    def create_widgets(self):
                # Tambahkan elemen lainnya di atas background
        ttk.Label(self.root, text=f"Welcome, {self.username} 🤚", font=("Helvetica", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10, padx=45)

        ttk.Label(self.root, text="Keterangan Loker:").grid(row=1, column=0, pady=10, padx=40, sticky="w")
        ttk.Entry(self.root, textvariable=self.keterangan_loker).grid(row=1, column=1, pady=10)

        ttk.Label(self.root, text="Minimum Height (cm):").grid(row=2, column=0, pady=10, padx=40, sticky="w")
        ttk.Entry(self.root, textvariable=self.min_height).grid(row=2, column=1)

        ttk.Label(self.root, text="Minimum Education Level:").grid(row=3, column=0, pady=10, padx=40, sticky="w")
        education_options = [("SMP", 0), ("SMA", 1), ("S1", 2)]
        self.education_menu = ttk.Combobox(self.root, values=[opt[0] for opt in education_options], state="readonly")
        self.education_menu.bind("<<ComboboxSelected>>", lambda event: self.min_education.set(dict(education_options)[self.education_menu.get()]))
        self.education_menu.grid(row=3, column=1)

        ttk.Label(self.root, text="Minimum Age:").grid(row=4, column=0, pady=10, padx=40, sticky="w")
        ttk.Entry(self.root, textvariable=self.min_age).grid(row=4, column=1)

        ttk.Label(self.root, text="Maximum Age:").grid(row=5, column=0, pady=10, padx=40, sticky="w")
        ttk.Entry(self.root, textvariable=self.max_age).grid(row=5, column=1)

        ttk.Label(self.root, text="Eyesight Problem Allowed:").grid(row=6, column=0, pady=10, padx=40, sticky="w")
        ttk.Checkbutton(self.root, variable=self.eyesight_allowed).grid(row=6, column=1)

        ttk.Button(self.root, text="Load File and Apply Filter", command=self.load_file, width=25).grid(row=7, column=0, columnspan=2, pady=20)

        ttk.Button(self.root, text="Preview Data", command=self.preview_data).grid(row=8, column=0, columnspan=2, pady=10)

        if self.role == "Head Of HR":
            ttk.Button(self.root, text="Manage Users", command=self.manage_users).grid(row=9, column=0, columnspan=2, pady=10)

        ttk.Button(self.root, text="    ⛔\nLogout", command=self.logout, width=10).grid(row=10, column=1, columnspan=2, pady=40, padx=70)



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

    def save_to_master_file(self, data):
        output_file = "output/output_database.xlsx"
        if os.path.exists(output_file):
            existing_data = pd.read_excel(output_file)
            combined_data = pd.concat([existing_data, data], ignore_index=True)
        else:
            combined_data = data
        combined_data.to_excel(output_file, index=False)

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

    def manage_users(self):
        if self.role != "Head Of HR":
            messagebox.showerror("Access Denied", "Only head users can manage users.")
            return
        
        UserManagement(self.root)

    def logout(self):
        self.root.destroy()
        login_window = tk.Tk()
        login_system = LoginSystem(login_window)
        login_window.mainloop()

# Preview Data Window
class PreviewWindow:
    def __init__(self, parent, data):
        self.window = tk.Toplevel(parent)
        self.window.title("Preview Data")
        self.window.geometry("900x700")
        self.data = data.copy()  
        self.filtered_data = data.copy() 
        self.create_widgets()

    def create_widgets(self):
        # Opsi Filterisasi Preview
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
        # isi data awal preview
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
        self.root.geometry("800x400")
        self.root.configure(bg="#f7c1d7")

        self.load_users()

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
        # UI tambah akun
        ttk.Label(self.root, text="Username:", background="#f7c1d7").grid(row=0, column=0, pady=10, padx=10, sticky="w")
        ttk.Entry(self.root, textvariable=self.username).grid(row=0, column=1, pady=10, padx=10)

        ttk.Label(self.root, text="Password:", background="#f7c1d7").grid(row=1, column=0, pady=10, padx=10, sticky="w")
        ttk.Entry(self.root, textvariable=self.password, show="*").grid(row=1, column=1, pady=10, padx=10)

        ttk.Label(self.root, text="Role:", background="#f7c1d7").grid(row=2, column=0, pady=10, padx=10, sticky="w")
        ttk.Combobox(self.root, textvariable=self.role, values=["Staff", "Head Of HR"]).grid(row=2, column=1, pady=10, padx=10)

        ttk.Button(self.root, text="Add User", command=self.add_user).grid(row=3, column=0, columnspan=2, pady=10)

        # UI hapus akun
        ttk.Label(self.root, text="Existing Users:", background="#f7c1d7").grid(row=0, column=2, pady=10, padx=10, sticky="w")
        
        self.user_listbox = tk.Listbox(self.root)
        self.user_listbox.grid(row=1, column=2, rowspan=3, pady=10, padx=10, sticky="nsew")  # Spanning 3 rows
        
        ttk.Button(self.root, text="Delete User", command=self.delete_user).grid(row=4, column=2, pady=10)

        self.root.grid_rowconfigure(1, weight=1)  
        self.root.grid_columnconfigure(2, weight=1)

        self.populate_user_list()

    def populate_user_list(self):
        self.user_listbox.delete(0, tk.END)
        for user in self.users:
            self.user_listbox.insert(tk.END, f"{user} - {self.users[user]['role']}")

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