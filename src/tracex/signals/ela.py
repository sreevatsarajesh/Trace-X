from io import BytesIO
import numpy as np
from PIL import Image, ImageChops

def analyze_ela(path, quality=90, scale=10):
    if not 1 <= int(quality) <= 95:
        raise ValueError("quality must be 1..95")
    with Image.open(path) as im:
        original = im.convert("RGB")
    buf = BytesIO()
    original.save(buf, format="JPEG", quality=int(quality))
    buf.seek(0)
    with Image.open(buf) as im:
        recompressed = im.convert("RGB")
    raw = np.asarray(ImageChops.difference(original, recompressed), dtype=np.float32)
    return {"map": raw.mean(axis=2), "mean_difference": float(raw.mean()),
            "max_difference": float(raw.max()),
            "visualization": np.clip(raw * scale, 0, 255).astype(np.uint8)}
