from io import BytesIO
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageEnhance


def analyze_ela(image_path, quality=90, scale=10):
    path = Path(image_path)
    if path.suffix.lower() not in {".jpg", ".jpeg"}:
        raise ValueError("ELA requires a JPEG image. Convert the image to JPEG first.")
    if not 1 <= int(quality) <= 95:
        raise ValueError("quality must be between 1 and 95")
    if scale <= 0:
        raise ValueError("scale must be positive")

    with Image.open(path) as im:
        original = im.convert("RGB")
    buffer = BytesIO()
    original.save(buffer, format="JPEG", quality=int(quality))
    buffer.seek(0)
    with Image.open(buffer) as recompressed:
        recompressed = recompressed.convert("RGB")

    diff = ImageChops.difference(original, recompressed)
    raw = np.asarray(diff, dtype=np.float32)
    enhanced = ImageEnhance.Brightness(diff).enhance(float(scale))
    return {
        "map": np.mean(raw, axis=2),
        "visualization": np.asarray(enhanced),
        "mean_difference": float(raw.mean()),
        "max_difference": float(raw.max()),
        "quality": int(quality),
        "scale": float(scale),
    }
