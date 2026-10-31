from pathlib import Path
from io import BytesIO
import numpy as np
from PIL import Image, ImageChops, ImageEnhance
def analyze_ela(image_path, output_path, quality=90, scale=10):
    image_path = Path(image_path)
    output_path = Path(output_path)
    if image_path.suffix.lower() not in {".jpg", ".jpeg"}:
        raise ValueError("ELA requires a JPEG input image.")
    if not 1 <= quality <= 95:
        raise ValueError("Quality must be between 1 and 95.")
    if scale <= 0:
        raise ValueError("Scale must be positive.")
    with Image.open(image_path) as source:
        original = source.convert("RGB")
    buffer = BytesIO()
    original.save(buffer, format="JPEG", quality=quality)
    buffer.seek(0)
    with Image.open(buffer) as recompressed:
        recompressed = recompressed.convert("RGB")
    difference = ImageChops.difference(original, recompressed)
    difference_array = np.asarray(difference, dtype=np.float32)
    mean_difference = float(np.mean(difference_array))
    max_difference = float(np.max(difference_array))
    enhanced = ImageEnhance.Brightness(difference).enhance(scale)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    enhanced.save(output_path)
    return {
        "input": str(image_path),
        "output": str(output_path),
        "quality": quality,
        "scale": scale,
        "mean_difference": mean_difference,
        "max_difference": max_difference
    }