import tkinter as tk
from tkinter import messagebox
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=3000)
try:
    client.admin.command("ping")
except ServerSelectionTimeoutError:
    print("ERROR: MongoDB server is not running on localhost:27017.")
    print("Start MongoDB and run this program again.")
    raise SystemExit(1)

db = client["collegeDB"]
collection = db["students"]


# Insert student record into MongoDB
def insert_student():
    name = name_entry.get().strip()
    roll = roll_entry.get().strip()
    branch = branch_entry.get().strip()
    cgpa = cgpa_entry.get().strip()

    if not (name and roll and branch and cgpa):
        messagebox.showwarning("Input Error", "All fields are required!")
        return

    try:
        cgpa = float(cgpa)
    except ValueError:
        messagebox.showerror("Invalid Input", "CGPA must be a number.")
        return

    if cgpa < 0 or cgpa > 10:
        messagebox.showerror("Invalid Input", "CGPA must be between 0 and 10.")
        return

    student = {"name": name, "roll": roll, "branch": branch, "cgpa": cgpa}
    collection.insert_one(student)
    messagebox.showinfo("Success", "Student record inserted.")
    for entry in (name_entry, roll_entry, branch_entry, cgpa_entry):
        entry.delete(0, tk.END)


# Display all student records
def display_students():
    result_text.delete("1.0", tk.END)
    count = 0
    for s in collection.find():
        fields = [s.get("name"), s.get("roll"), s.get("branch"), s.get("cgpa")]
        line = " | ".join(str(f) for f in fields) + "\n"
        result_text.insert(tk.END, line)
        count += 1
    if count == 0:
        result_text.insert(tk.END, "No student records found.\n")


# GUI setup
app = tk.Tk()
app.title("Student Database App (MongoDB)")

tk.Label(app, text="Name:").grid(row=0, column=0)
name_entry = tk.Entry(app)
name_entry.grid(row=0, column=1)

tk.Label(app, text="Roll No:").grid(row=1, column=0)
roll_entry = tk.Entry(app)
roll_entry.grid(row=1, column=1)

tk.Label(app, text="Branch:").grid(row=2, column=0)
branch_entry = tk.Entry(app)
branch_entry.grid(row=2, column=1)

tk.Label(app, text="CGPA:").grid(row=3, column=0)
cgpa_entry = tk.Entry(app)
cgpa_entry.grid(row=3, column=1)

insert_btn = tk.Button(app, text="Insert Student", command=insert_student)
insert_btn.grid(row=4, column=0, columnspan=2, pady=10)
show_btn = tk.Button(app, text="Show All Students", command=display_students)
show_btn.grid(row=5, column=0, columnspan=2, pady=5)

result_text = tk.Text(app, width=50, height=10)
result_text.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

app.mainloop()
