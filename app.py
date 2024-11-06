import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd

class ApplicantFilterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Job Applicant Filter")
        self.root.configure(bg="#E0F7FA")
        self.root.geometry("400x500")

        # Configure styles
        style = ttk.Style()
        style.configure("TLabel", font=("Helvetica", 12), background="#E0F7FA", foreground="#000000")
        style.configure("TEntry", font=("Helvetica", 11))
        style.configure("TCombobox", font=("Helvetica", 11))
        style.configure("TButton", font=("Helvetica", 11, "bold"), background="#4CAF50", foreground="black")
        style.map("TButton", background=[("active", "#45a049")])

        # Configuration Variables with default values
        self.min_height = tk.IntVar(value=0)  
        self.min_education = tk.IntVar(value=0)
        self.min_age = tk.IntVar(value=0)  
        self.max_age = tk.IntVar(value=100)  
        self.eyesight_allowed = tk.BooleanVar(value=True) 

        # UI Setup
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self.root, text="Minimum Height (cm):").grid(row=0, column=0, sticky='w', padx=20, pady=10)
        ttk.Entry(self.root, textvariable=self.min_height, width=15).grid(row=0, column=1, padx=20)

        ttk.Label(self.root, text="Minimum Education Level:").grid(row=1, column=0, sticky='w', padx=20, pady=10)
        education_options = [("SMP", 0), ("SMA", 1), ("S1", 2)]
        self.education_menu = ttk.Combobox(self.root, textvariable=self.min_education, values=[opt[0] for opt in education_options], width=13)
        self.education_menu.bind("<<ComboboxSelected>>", lambda event: self.min_education.set(dict(education_options)[self.education_menu.get()]))
        self.education_menu.grid(row=1, column=1, padx=20)

        ttk.Label(self.root, text="Minimum Age:").grid(row=2, column=0, sticky='w', padx=20, pady=10)
        ttk.Entry(self.root, textvariable=self.min_age, width=15).grid(row=2, column=1, padx=20)

        ttk.Label(self.root, text="Maximum Age:").grid(row=3, column=0, sticky='w', padx=20, pady=10)
        ttk.Entry(self.root, textvariable=self.max_age, width=15).grid(row=3, column=1, padx=20)

        ttk.Label(self.root, text="Eyesight Problem Allowed:").grid(row=4, column=0, sticky='w', padx=20, pady=10)
        ttk.Checkbutton(self.root, variable=self.eyesight_allowed).grid(row=4, column=1, sticky='w', padx=20)

        ttk.Button(self.root, text="Load File and Apply Filter", command=self.load_file).grid(row=5, column=0, columnspan=2, pady=30)

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx")])
        if not file_path:
            return

        try:
            # Load file based on file extension
            if file_path.endswith('.csv'):
                data = pd.read_csv(file_path)
            else:
                data = pd.read_excel(file_path)

            # Encode the 'Education' column in the loaded data
            education_map = {"SMP": 0, "SMA": 1, "S1": 2}
            data['Education'] = data['Education'].map(education_map).fillna(-1).astype(int)

            # Extract filename without extension
            filename = os.path.splitext(os.path.basename(file_path))[0]

            # Filter applicants based on criteria
            data['Status'] = data.apply(self.evaluate_applicant, axis=1)

            # Decode 'Education' column back to string format before saving
            decode_map = {0: "SMP", 1: "SMA", 2: "S1"}
            data['Education'] = data['Education'].map(decode_map)
                        
            # Create dynamic output filename
            output_path = f"output/filtered_{filename}.xlsx"
            data.to_excel(output_path, index=False)
            
            # Display a success message with the output file path
            messagebox.showinfo("Success", f"The applications have been filtered and saved in {output_path}")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def evaluate_applicant(self, applicant):
        try:
            # Retrieve applicant details
            height = applicant.get("Height", 0)
            education = applicant.get("Education", -1)
            age = applicant.get("Age", 0)
            eyesight_problem = applicant.get("Eyesight Problem", "").lower() == "yes"

            # Apply filter criteria, only applying checks if criteria are set
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

# Run the application
root = tk.Tk()
app = ApplicantFilterApp(root)
root.mainloop()