from hashlib import md5
from PIL import Image
from io import BytesIO

def get_bytes(image_location):
    out = BytesIO()
    image = Image.open(image_location)
    image.save(out, 'png')
    return out.read()

def get_hash(image_bytes):
    image_hash = str(md5(image_bytes).hexdigest())
    return image_hash
