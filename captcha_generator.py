from PIL import Image, ImageDraw, ImageFont
import random
import string

def generate_captcha():
    width, height = 150, 50
    image = Image.new("RGB", (width, height), color=(255, 255, 255))

    try:
        font = ImageFont.truetype("arial.ttf", 28)
    except:
        font = ImageFont.load_default()

    captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

    draw = ImageDraw.Draw(image)

    # Use textbbox instead of textsize (works in new Pillow versions)
    bbox = draw.textbbox((0, 0), captcha_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x = (width - text_width) // 2
    y = (height - text_height) // 2
    draw.text((x, y), captcha_text, font=font, fill=(0, 0, 0))

    # Add noise
    for _ in range(20):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = x1 + random.randint(0, 10)
        y2 = y1 + random.randint(0, 10)
        draw.line(((x1, y1), (x2, y2)), fill=(0, 0, 0))

    return image, captcha_text
