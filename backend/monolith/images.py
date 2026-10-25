from io import BytesIO

from PIL import Image, ImageOps, UnidentifiedImageError
from pillow_heif import register_heif_opener
from rest_framework.exceptions import ValidationError

register_heif_opener()

MAX_UPLOAD_SIZE = 10 * 1024 * 1024
MAX_SIDE = 1600


def encode_image(upload):
    if upload.size > MAX_UPLOAD_SIZE:
        raise ValidationError({"file": "Das Bild darf höchstens 10 MB gross sein."})
    try:
        with Image.open(upload) as original:
            image = ImageOps.exif_transpose(original)
            image.thumbnail((MAX_SIDE, MAX_SIDE), Image.Resampling.LANCZOS)
            output = BytesIO()
            image.convert("RGBA").save(output, format="WEBP", quality=82)
    except (UnidentifiedImageError, OSError) as error:
        raise ValidationError({"file": "Die Datei ist kein gültiges Bild."}) from error
    return output.getvalue()
