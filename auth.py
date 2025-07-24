import os
import json
import smtplib
import random
from email.message import EmailMessage
from email_validator import validate_email, EmailNotValidError

from dotenv import load_dotenv
load_dotenv()

USERS_DIR = "users"

# Load or create users directory
if not os.path.exists(USERS_DIR):
    os.makedirs(USERS_DIR)

# Load email credentials
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# Helper to generate CAPTCHA
def generate_captcha():
    a = random.randint(1, 20)
    b = random.randint(1, 20)
    return f"{a} + {b}", a + b

# Send email with code
def send_verification_email(to_email, code):
    msg = EmailMessage()
    msg.set_content(f"Your Emotionary verification code is: {code}")
    msg["Subject"] = "Emotionary Email Verification"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

# Signup or Login
def authenticate(email, is_signup=True):
    try:
        valid = validate_email(email)
        email = valid.email
    except EmailNotValidError as e:
        return False, str(e)

    user_file = os.path.join(USERS_DIR, f"{email}.json")

    if is_signup and os.path.exists(user_file):
        return False, "Email already registered."
    elif not is_signup and not os.path.exists(user_file):
        return False, "Email not found."

    # CAPTCHA
    q, ans = generate_captcha()
    try:
        user_ans = int(input(f"Solve CAPTCHA to continue: {q} = "))
        if user_ans != ans:
            return False, "CAPTCHA failed."
    except:
        return False, "Invalid CAPTCHA input."

    # Email Verification
    code = str(random.randint(100000, 999999))
    send_verification_email(email, code)
    user_input = input("Enter the 6-digit code sent to your email: ")

    if user_input.strip() != code:
        return False, "Email verification failed."

    # Save user if signup
    if is_signup:
        with open(user_file, "w") as f:
            json.dump({"email": email}, f)

    return True, "Authentication successful!"
