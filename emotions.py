from textblob import TextBlob

def detect_emotion(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.5:
        return "Very Happy 😊"
    elif polarity > 0:
        return "Happy 🙂"
    elif polarity == 0:
        return "Neutral 😐"
    elif polarity > -0.5:
        return "Sad 😢"
    else:
        return "Very Sad 😞"
