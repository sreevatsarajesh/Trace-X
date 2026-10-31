
from pathlib import Path

from src.forensics.noise import analyze_noise


def main():
    root = Path(__file__).resolve().parents[2]

    image_path = root / "data" / "processed" / "ela_sample.jpg"

    output_dir = root / "results" / "noise"

    result = analyze_noise(
        image_path,
        output_dir,
        sigma=1.0
    )

    print("\nTRACE-X | NOISE ANALYSIS")
    print("-" * 40)

    for key, value in result.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
