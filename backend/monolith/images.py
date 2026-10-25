from io import BytesIO
from pathlib import Path

from PIL import Image, ImageOps, UnidentifiedImageError
from pillow_heif import register_heif_opener
from rest_framework.exceptions import ValidationError

register_heif_opener()

MAX_SIDE = 1600
QUALITY = 75
THUMBNAIL_SIZES = {96, 256}


def resize(source, side):
    with Image.open(source) as original:
        image = ImageOps.exif_transpose(original)
        image.thumbnail((side, side), Image.Resampling.LANCZOS)
        mode = "RGBA" if image.has_transparency_data else "RGB"
        output = BytesIO()
        image.convert(mode).save(output, format="WEBP", quality=QUALITY, method=6)
    return output.getvalue()


def encode_image(upload):
    try:
        return resize(upload, MAX_SIDE)
    except (UnidentifiedImageError, Image.DecompressionBombError, OSError) as error:
        raise ValidationError({"file": "Die Datei ist kein gültiges Bild."}) from error


def image_name(upload):
    return Path(upload.name).stem[:200] or "Bild"


def thumbnail(data, size):
    return resize(BytesIO(data), size) if size in THUMBNAIL_SIZES else data
