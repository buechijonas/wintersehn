import os
from io import BytesIO
from pathlib import Path
from uuid import uuid4

from PIL import Image, ImageOps, UnidentifiedImageError
from pillow_heif import register_heif_opener
from rest_framework.exceptions import ValidationError

register_heif_opener()

QUALITY = 75
MAX_SIDE = 1600
THUMBNAIL_SIZES = {96, 256}
INVALID = (UnidentifiedImageError, Image.DecompressionBombError, OSError, SyntaxError)


def webp(image, quality=QUALITY):
    mode = "RGBA" if image.has_transparency_data else "RGB"
    output = BytesIO()
    image.convert(mode).save(output, format="WEBP", quality=quality, method=6)
    return output.getvalue()


def resize(source, side):
    with Image.open(source) as original:
        image = ImageOps.exif_transpose(original)
        image.thumbnail((side, side), Image.Resampling.LANCZOS)
        return webp(image)


def square(source, size):
    with Image.open(source) as original:
        image = ImageOps.exif_transpose(original)
        side = min(size, image.width, image.height)
        return webp(
            ImageOps.fit(image, (side, side), method=Image.Resampling.LANCZOS), 82
        )


def thumbnail(data, size):
    return resize(BytesIO(data), size) if size in THUMBNAIL_SIZES else data


def encode(upload, side=MAX_SIDE):
    try:
        return resize(upload, side)
    except INVALID as error:
        raise ValidationError({"file": "Die Datei ist kein gültiges Bild."}) from error


def name(upload):
    return Path(upload.name).stem[:200] or "Bild"


def write_atomic(target, data):
    target.parent.mkdir(parents=True, exist_ok=True)
    partial = target.with_name(f"{target.name}.{uuid4().hex}.tmp")
    partial.write_bytes(data)
    os.replace(partial, target)
