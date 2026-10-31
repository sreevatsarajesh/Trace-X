from pathlib import Path
from src.forensics.dct import analyze_dct
def main():
    root = Path(__file__).resolve().parents[2]
    image_path = root / "data" / "processed" / "ela_sample.jpg"
    output_dir = root / "results" / "dct"
    result = analyze_dct(image_path, output_dir)
    print("\nTRACE-X | DCT RESULTS")
    print("-" * 40)
    for key, value in result.items():
        print(f"{key}: {value}")
if __name__ == "__main__":
    main()