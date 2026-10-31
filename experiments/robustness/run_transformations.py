from pathlib import Path
from src.transformations.engine import apply_transformations


def main():
    root = Path(__file__).resolve().parents[2]

    results = apply_transformations(
        root / "data" / "processed" / "ela_sample.jpg",
        root / "data" / "processed" / "transformed"
    )

    for name, path in results.items():
        print(f"{name}: {path}")


if __name__ == "__main__":
    main()