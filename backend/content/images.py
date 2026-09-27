import os
import re
import uuid
from pathlib import Path

from django.conf import settings
from PIL import Image, ImageOps

# Fixed set so a client can't fill the disk by requesting arbitrary sizes.
THUMBNAIL_SIZES = {64, 128, 192}

# GIFs are left out on purpose: a WebP thumbnail would drop the animation.
UPLOAD_NAME = re.compile(r"^[0-9a-f]{32}\.(jpg|png|webp)$")


def thumbnail_path(name, size):
    return Path(settings.MEDIA_ROOT) / "thumbnails" / str(size) / f"{name.rsplit('.', 1)[0]}.webp"


def build_thumbnail(source, target, size):
    with Image.open(source) as original:
        image = ImageOps.exif_transpose(original)
        side = min(size, image.width, image.height)
        image = ImageOps.fit(image, (side, side), method=Image.Resampling.LANCZOS)
        if image.mode not in ("RGB", "RGBA"):
            image = image.convert("RGBA")

        target.parent.mkdir(parents=True, exist_ok=True)
        partial = target.with_name(f"{target.name}.{uuid.uuid4().hex}.tmp")
        image.save(partial, format="WEBP", quality=82)
        os.replace(partial, target)
