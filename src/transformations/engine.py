from pathlib import Path
from PIL import Image


def apply_transformations(image_path, output_dir):
    image_path = Path(image_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    with Image.open(image_path) as source:
        image = source.convert("RGB")

    width, height = image.size
    results = {}

    transformations = {
        "jpeg_70": lambda img: img.save(
            output_dir / "jpeg_70.jpg",
            "JPEG",
            quality=70
        ),
        "jpeg_40": lambda img: img.save(
            output_dir / "jpeg_40.jpg",
            "JPEG",
            quality=40
        ),
        "resized_50": lambda img: img.resize(
            (width // 2, height // 2)
        ).save(output_dir / "resized_50.jpg", "JPEG", quality=85),
        "resized_25": lambda img: img.resize(
            (width // 4, height // 4)
        ).save(output_dir / "resized_25.jpg", "JPEG", quality=85),
        "cropped": lambda img: img.crop((
            width // 8,
            height // 8,
            width * 7 // 8,
            height * 7 // 8
        )).save(output_dir / "cropped.jpg", "JPEG", quality=85)
    }

    for name, operation in transformations.items():
        operation(image)
        results[name] = str(output_dir / f"{name}.jpg")

    return results