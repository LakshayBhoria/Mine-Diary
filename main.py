import tkinter as tk
from tkinter import messagebox, simpledialog
from emotions import detect_emotion
from auth import login_user, signup_user
import json, os
from datetime import datetime
import random

with open("affirmations.json", "r") as f:
    affirmations = json.load(f)

# --- App Window Setup ---
app = tk.Tk()
app.title("Emotionary - AI Diary")
app.geometry("400x500")
app.resizable(False, False)

current_user = None

# --- Frame Switcher ---
frames = {}

def show_frame(name):
    for f in frames.values():
        f.pack_forget()
    frames[name].pack(fill="both", expand=True)

# --- Login Frame ---
login_frame = tk.Frame(app)
frames["login"] = login_frame

tk.Label(login_frame, text="Login", font=("Arial", 20)).pack(pady=20)
email_entry = tk.Entry(login_frame, width=30)
email_entry.pack(pady=5)
email_entry.insert(0, "Enter your email")

password_entry = tk.Entry(login_frame, show="*", width=30)
password_entry.pack(pady=5)
password_entry.insert(0, "password")

def handle_login():
    global current_user
    email = email_entry.get()
    password = password_entry.get()
    if login_user(email, password):
        current_user = email
        show_frame("diary")
    else:
        messagebox.showerror("Error", "Invalid credentials!")

tk.Button(login_frame, text="Login", command=handle_login).pack(pady=10)
tk.Button(login_frame, text="Sign up", command=lambda: show_frame("signup")).pack()

# --- Signup Frame ---
signup_frame = tk.Frame(app)
frames["signup"] = signup_frame

tk.Label(signup_frame, text="Signup", font=("Arial", 20)).pack(pady=20)
signup_email = tk.Entry(signup_frame, width=30)
signup_email.pack(pady=5)

signup_password = tk.Entry(signup_frame, show="*", width=30)
signup_password.pack(pady=5)

def handle_signup():
    email = signup_email.get()
    password = signup_password.get()
    if signup_user(email, password):
        messagebox.showinfo("Success", "Account created. Please login.")
        show_frame("login")
    else:
        messagebox.showerror("Error", "User already exists.")

tk.Button(signup_frame, text="Create Account", command=handle_signup).pack(pady=10)
tk.Button(signup_frame, text="Back to Login", command=lambda: show_frame("login")).pack()

# --- Diary Frame ---
diary_frame = tk.Frame(app)
frames["diary"] = diary_frame

tk.Label(diary_frame, text="How are you feeling today?", font=("Arial", 14)).pack(pady=10)
entry_text = tk.Text(diary_frame, height=10, width=40)
entry_text.pack()

output_label = tk.Label(diary_frame, text="", wraplength=300, font=("Arial", 11))
output_label.pack(pady=10)

def analyze_and_save():
    text = entry_text.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("Empty", "Please write something.")
        return
    emotion = detect_emotion(text)
    aff = random.choice(affirmations.get(emotion.split()[0], ["You're strong."]))
    output_label.config(text=f"🧠 {emotion}\n💌 {aff}")

    today = datetime.today().strftime("%Y-%m-%d")
    os.makedirs("entries", exist_ok=True)
    filename = f"entries/{current_user}_{today}.json"
    with open(filename, "w") as f:
        json.dump({
            "user": current_user,
            "date": today,
            "entry": text,
            "emotion": emotion,
            "affirmation": aff
        }, f, indent=2)

    entry_text.delete("1.0", tk.END)
    messagebox.showinfo("Saved", f"Entry saved for {today}.")

tk.Button(diary_frame, text="Analyze & Save", command=analyze_and_save).pack(pady=10)

# --- Start on Login Frame ---
show_frame("login")
app.mainloop()
