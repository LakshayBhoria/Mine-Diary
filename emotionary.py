import os
import json
from datetime import datetime
from emotions import detect_emotion
import random

# Load affirmations
with open("affirmations.json", "r") as f:
    affirmations = json.load(f)

# Create folder if not exists
os.makedirs("entries", exist_ok=True)

def save_entry(text, emotion, affirmation):
    today = datetime.today().strftime("%Y-%m-%d")
    filename = f"entries/{today}.json"
    with open(filename, "w") as f:
        json.dump({
            "date": today,
            "entry": text,
            "emotion": emotion,
            "affirmation": affirmation
        }, f, indent=2)
    print(f"\n✅ Entry saved to {filename}")

def main():
    print("🧠 Welcome to Emotionary 📝")
    text = input("\nWrite your entry:\n> ")

    emotion = detect_emotion(text)
    affirmation = random.choice(affirmations.get(emotion.split()[0], ["You're strong. Keep going."]))

    print(f"\n🧠 Detected Emotion: {emotion}")
    print(f"💌 Affirmation: {affirmation}")

    save_entry(text, emotion, affirmation)

if __name__ == "__main__":
    main()
