import os
import random
import string
from tkinter import *
from tkinter import messagebox, scrolledtext
from PIL import Image, ImageDraw, ImageFont, ImageTk
from auth import authenticate
from datetime import datetime

# Generate CAPTCHA
def generate_captcha():
    captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    img = Image.new('RGB', (120, 40), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    d.text((10, 10), captcha_text, font=font, fill=(0, 0, 0))
    return img, captcha_text

class MineDiaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mine-Diary - Your Personal Diary")
        self.root.geometry("700x650")
        self.root.config(bg="#fffaf0")

        self.email = None
        self.captcha_code = ""

        os.makedirs("entries", exist_ok=True)
        os.makedirs("users", exist_ok=True)

        self.show_login()

    def show_login(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        try:
            logo_img = Image.open("image.jpg").resize((80, 80))
            self.logo_photo = ImageTk.PhotoImage(logo_img)
            Label(self.root, image=self.logo_photo, bg="#fffaf0").pack(pady=5)
        except:
            pass

        Label(self.root, text="📔 Mine-Diary", font=("Georgia", 28, "bold"), bg="#fffaf0", fg="#5a2a27").pack(pady=5)
        Label(self.root, text="Enter your Email:", font=("Georgia", 14), bg="#fffaf0").pack()
        self.email_entry = Entry(self.root, font=("Georgia", 12), width=30)
        self.email_entry.pack(pady=5)

        self.captcha_img, self.captcha_code = generate_captcha()
        self.tk_captcha = ImageTk.PhotoImage(self.captcha_img)
        self.captcha_label = Label(self.root, image=self.tk_captcha, bg="#fffaf0")
        self.captcha_label.pack()

        self.captcha_entry = Entry(self.root, font=("Georgia", 12), width=15)
        self.captcha_entry.pack(pady=5)
        Label(self.root, text="Enter CAPTCHA above", font=("Georgia", 10), bg="#fffaf0").pack()

        self.signup_var = IntVar()
        Checkbutton(self.root, text="New user? Sign up", variable=self.signup_var, bg="#fffaf0", font=("Georgia", 10)).pack()

        Button(self.root, text="Continue", command=self.verify_user, font=("Georgia", 12), bg="#8B4513", fg="white", padx=10).pack(pady=10)

    def verify_user(self):
        email = self.email_entry.get().strip()
        captcha_input = self.captcha_entry.get().strip().upper()

        if not email or not captcha_input:
            messagebox.showwarning("Input Error", "Please complete all fields.")
            return

        if captcha_input != self.captcha_code:
            messagebox.showerror("CAPTCHA Failed", "Invalid CAPTCHA. Please try again.")
            self.show_login()
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
    app = MineDiaryApp(root)
    root.mainloop()
