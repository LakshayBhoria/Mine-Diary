import os
from tkinter import *
from tkinter import messagebox, scrolledtext
from auth import authenticate
from datetime import datetime

# Make sure required folders exist
if not os.path.exists("entries"):
    os.makedirs("entries")
if not os.path.exists("users"):
    os.makedirs("users")

# ---- MAIN APP GUI ---- #
class EmotionaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Emotionary - Your Personal Diary")
        self.root.geometry("700x600")
        self.root.config(bg="#fffaf0")

        self.email = None

        self.show_login()

    def show_login(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        Label(self.root, text="📔 Emotionary", font=("Georgia", 28, "bold"), bg="#fffaf0", fg="#5a2a27").pack(pady=20)
        Label(self.root, text="Enter your Email:", font=("Georgia", 14), bg="#fffaf0").pack()

        self.email_entry = Entry(self.root, font=("Georgia", 12), width=30)
        self.email_entry.pack(pady=10)

        self.signup_var = IntVar()
        Checkbutton(self.root, text="New user? Sign up", variable=self.signup_var, bg="#fffaf0", font=("Georgia", 10)).pack()

        Button(self.root, text="Continue", command=self.verify_user, font=("Georgia", 12), bg="#8B4513", fg="white", padx=10).pack(pady=15)

    def verify_user(self):
        email = self.email_entry.get().strip()
        if not email:
            messagebox.showwarning("Input Error", "Please enter your email.")
            return

        is_signup = bool(self.signup_var.get())
        success, msg = authenticate(email, is_signup)

        if success:
            self.email = email
            self.show_diary()
        else:
            messagebox.showerror("Authentication Failed", msg)

    def show_diary(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        Label(self.root, text="📖 Your Diary", font=("Georgia", 24, "bold"), bg="#fffaf0", fg="#5a2a27").pack(pady=20)

        self.text_area = scrolledtext.ScrolledText(self.root, wrap=WORD, font=("Georgia", 13), bg="#fffef8", width=70, height=20)
        self.text_area.pack(padx=15, pady=10)

        Button(self.root, text="Save Entry", command=self.save_entry, font=("Georgia", 12), bg="#006400", fg="white", padx=12).pack(pady=10)
        Button(self.root, text="Logout", command=self.show_login, font=("Georgia", 10), bg="#a52a2a", fg="white").pack(pady=5)

    def save_entry(self):
        content = self.text_area.get("1.0", END).strip()
        if not content:
            messagebox.showwarning("Empty", "Diary entry is empty.")
            return

        date_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        user_folder = os.path.join("entries", self.email.replace("@", "_"))
        os.makedirs(user_folder, exist_ok=True)

        file_path = os.path.join(user_folder, f"{date_str}.txt")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        messagebox.showinfo("Saved", "Your diary entry has been saved.")
        self.text_area.delete("1.0", END)

# Run the App
if __name__ == "__main__":
    root = Tk()
    app = EmotionaryApp(root)
    root.mainloop()
