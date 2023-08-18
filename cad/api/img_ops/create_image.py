from PIL import Image
from uuid import uuid4
from io import BytesIO
from os import stat

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
