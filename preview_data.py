import tkinter as tk
from tkinter import ttk, messagebox

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