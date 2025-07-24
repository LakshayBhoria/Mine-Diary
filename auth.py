import os, json

os.makedirs("users", exist_ok=True)

def get_user_path(email):
    return f"users/{email.replace('@', '_at_')}.json"

def signup_user(email, password):
    path = get_user_path(email)
    if os.path.exists(path):
        return False
    with open(path, "w") as f:
        json.dump({"email": email, "password": password}, f)
    return True

def login_user(email, password):
    path = get_user_path(email)
    if not os.path.exists(path):
        return False
    with open(path) as f:
        data = json.load(f)
        return data["password"] == password
