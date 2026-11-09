import re
import uuid
from io import BytesIO
from pathlib import Path

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from PIL import Image
from rest_framework.exceptions import ValidationError

from commons import images

THUMBNAIL_SIZES = {64, 128, 192}
MAX_UPLOAD_SIZE = 512 * 1024 * 1024
MAX_DIMENSION = 2000
FORMATS = {"JPEG": "jpg", "PNG": "png", "WEBP": "webp", "GIF": "gif"}
UPLOAD_NAME = re.compile(r"^[0-9a-f]{32}\.(jpg|png|webp)$")


def thumbnail_path(name, size):
    return (
        Path(settings.MEDIA_ROOT)
        / "thumbnails"
        / str(size)
        / f"{name.rsplit('.', 1)[0]}.webp"
    )


def thumbnail(name, size):
    source = Path(settings.MEDIA_ROOT) / "uploads" / name
    if (
        not UPLOAD_NAME.match(name)
        or size not in THUMBNAIL_SIZES
        or not source.is_file()
    ):
        return None
    target = thumbnail_path(name, size)
    if not target.is_file():
        images.write_atomic(target, images.square(source, size))
    return target


def opened(raw):
    try:
        Image.open(BytesIO(raw)).verify()
        return Image.open(BytesIO(raw))
    except images.INVALID as error:
        raise ValidationError({"detail": "Datei ist kein gültiges Bild."}) from error


def limited(image, raw):
    if image.width <= MAX_DIMENSION and image.height <= MAX_DIMENSION:
        return raw
    image_format = image.format
    if image_format == "JPEG" and image.mode in ("RGBA", "P"):
        image = image.convert("RGB")
    image.thumbnail((MAX_DIMENSION, MAX_DIMENSION))
    output = BytesIO()
    image.save(output, format=image_format)
    return output.getvalue()


def store(upload):
    if upload.size > MAX_UPLOAD_SIZE:
        raise ValidationError({"detail": "Datei ist zu gross (max. 512 MB)."})
    raw = upload.read()
    image = opened(raw)
    extension = FORMATS.get(image.format)
    if not extension:
        raise ValidationError(
            {"detail": "Nicht unterstütztes Bildformat (JPEG, PNG, WEBP, GIF)."}
        )
    path = default_storage.save(
        f"uploads/{uuid.uuid4().hex}.{extension}", ContentFile(limited(image, raw))
    )
    return f"{settings.MEDIA_URL}{path}"
