from PIL import Image, ImageDraw, ImageFont
import random
import string
import io

def generate_captcha(width=150, height=50):
    # Generate random text
    captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

    # Create image with white background
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)

    # Load font
    try:
        font = ImageFont.truetype("arial.ttf", 30)
    except:
        font = ImageFont.load_default()

    # Get bounding box to center the text
    bbox = draw.textbbox((0, 0), captcha_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = (width - text_width) // 2
    text_y = (height - text_height) // 2

    # Draw text
    draw.text((text_x, text_y), captcha_text, fill="black", font=font)

    # Add some random noise lines
    for _ in range(5):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
        draw.line(((x1, y1), (x2, y2)), fill="gray", width=1)

    return image, captcha_text
