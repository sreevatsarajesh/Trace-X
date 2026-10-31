from pathlib import Path
from PIL import Image


def apply_transformations(image_path, output_dir):
    image_path = Path(image_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    with Image.open(image_path) as source:
        image = source.convert("RGB")
    width, height = image.size
    if min(width, height) < 16:
        raise ValueError("Image is too small for the configured crop/resize operations")

    variants = {
        "jpeg_70": lambda: image.save(output_dir / "jpeg_70.jpg", "JPEG", quality=70),
        "jpeg_40": lambda: image.save(output_dir / "jpeg_40.jpg", "JPEG", quality=40),
        "resized_50": lambda: image.resize((max(1, width // 2), max(1, height // 2))).save(
            output_dir / "resized_50.jpg", "JPEG", quality=85
        ),
        "resized_25": lambda: image.resize((max(1, width // 4), max(1, height // 4))).save(
            output_dir / "resized_25.jpg", "JPEG", quality=85
        ),
        "cropped": lambda: image.crop((
            width // 8, height // 8, width * 7 // 8, height * 7 // 8
        )).save(output_dir / "cropped.jpg", "JPEG", quality=85),
    }
    result = {}
    for name, operation in variants.items():
        operation()
        result[name] = str(output_dir / f"{name}.jpg")
    return result


def infer_transformation(label):
    name = str(label).lower()
    if "jpeg" in name or "jpg" in name or "compress" in name:
        return "jpeg"
    if "resize" in name or "resized" in name:
        return "resize"
    if "crop" in name:
        return "crop"
    if name == "original":
        return "unknown"
    return "unknown"
