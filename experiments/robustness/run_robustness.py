from pathlib import Path
import csv

from src.forensics.pipeline import run_trace_x


def main():
    root = Path(__file__).resolve().parents[2]

    original = root / "data" / "processed" / "ela_sample.jpg"
    transformed_dir = root / "data" / "processed" / "transformed"
    output_dir = root / "results" / "robustness"

    output_dir.mkdir(parents=True, exist_ok=True)

    images = {
        "original": original,
        **{
            path.stem: path
            for path in sorted(transformed_dir.glob("*.jpg"))
        }
    }

    rows = []

    for name, image_path in images.items():
        print(f"\nAnalyzing: {name}")

        result = run_trace_x(
            image_path,
            output_dir / name
        )

        rows.append({
            "image": name,
            "ela_mean_difference": result["analysis"]["ela"]["mean_difference"],
            "dct_mean_hf_ratio": result["analysis"]["dct"]["mean_high_frequency_ratio"],
            "noise_mean_magnitude": result["analysis"]["noise"]["mean_magnitude"],
            "combined_mean_signal": result["fusion"]["mean_signal"]
        })

    csv_path = output_dir / "robustness_results.csv"

    with open(csv_path, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print("\nTRACE-X | ROBUSTNESS RESULTS")
    print("-" * 65)

    for row in rows:
        print(
            f"{row['image']:15} "
            f"ELA: {row['ela_mean_difference']:.4f} | "
            f"DCT: {row['dct_mean_hf_ratio']:.4f} | "
            f"Noise: {row['noise_mean_magnitude']:.4f} | "
            f"Fusion: {row['combined_mean_signal']:.4f}"
        )

    print(f"\nCSV saved: {csv_path}")


if __name__ == "__main__":
    main()