
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

from src.forensics.ela import analyze_ela


def create_sample_image(output_path):
    rng = np.random.default_rng(42)

    width, height = 512, 512

    x = np.linspace(0, 255, width, dtype=np.uint8)
    gradient = np.tile(x, (height, 1))

    image_array = np.stack(
        [gradient, np.flip(gradient, axis=1), gradient],
        axis=2
    )

    noise = rng.normal(0, 4, image_array.shape)
    image_array = np.clip(
        image_array.astype(np.float32) + noise,
        0,
        255
    ).astype(np.uint8)

    image = Image.fromarray(image_array)

    draw = ImageDraw.Draw(image)
    draw.rectangle((80, 80, 250, 250), fill=(220, 40, 60))
    draw.ellipse((280, 120, 440, 280), fill=(30, 180, 90))
    draw.rectangle((100, 320, 420, 420), fill=(40, 70, 220))

    output_path.parent.mkdir(parents=True, exist_ok=True)

    image.save(output_path, format="JPEG", quality=95)


def main():
    root = Path(__file__).resolve().parents[2]

    input_path = root / "data" / "processed" / "ela_sample.jpg"
    output_path = root / "results" / "ela_sample.png"

    create_sample_image(input_path)

    result = analyze_ela(
        input_path,
        output_path,
        quality=90,
        scale=10
    )

    print("\nTRACE-X | ELA RESULTS")
    print("-" * 35)

    for key, value in result.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
