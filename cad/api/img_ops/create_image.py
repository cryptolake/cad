from PIL import Image, ImageFont, ImageDraw
from uuid import uuid4
from io import BytesIO
from os import stat

def create_text_image(image, text, font, size, color, x, y):
    font = ImageFont.truetype(font, size, layout_engine=ImageFont.Layout.RAQM)
    image_draw = ImageDraw.Draw(image)
    image_draw.multiline_text((x, y), text, fill=color,
                              anchor='ls', font=font, embedded_color=True)
    return image

def save_image(image_bytes):

    if not issubclass(type(image_bytes), Image.Image):
        image_obj = Image.open(BytesIO(image_bytes))
    else:
        image_obj = image_bytes
    
    image_name = str(uuid4()) + ".jpg"
    image_path = f"static/{image_name}"

    image_jpg = image_obj.convert("RGB")
    image_jpg.save(image_path)

    image_size = stat(image_path).st_size

    return image_jpg, image_path, image_size


def create_image(image_loc, headline, short,
                    headline_text, short_text):
    ad_image = Image.open(image_loc)
    create_text_image(ad_image, headline_text, headline.font,
                      headline.size, headline.color, headline.x, headline.y)
    create_text_image(ad_image, short_text, short.font,
                      short.size, short.color, short.x, short.y)
    return ad_image
