from PIL import Image, ImageDraw, ImageFont
import random
import string

def generate_captcha():
    # Generate random string
    captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    # Create image
    img = Image.new('RGB', (120, 40), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    d.text((10, 10), captcha_text, font=font, fill=(0, 0, 0))

    return img, captcha_text  # ✅ Return both
