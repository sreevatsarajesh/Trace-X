from pathlib import Path
import json

import cv2
import numpy as np
import matplotlib.pyplot as plt

from src.forensics.ela import analyze_ela
from src.forensics.dct import analyze_dct
from src.forensics.noise import analyze_noise


def normalize_map(array):
    array = np.asarray(array, dtype=np.float32)
    low, high = np.percentile(array, [1, 99])
    return np.clip((array - low) / (high - low + 1e-8), 0, 1)


def run_trace_x(image_path, output_dir):
    image_path = Path(image_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    ela_dir = output_dir / "ela"
    dct_dir = output_dir / "dct"
    noise_dir = output_dir / "noise"

    ela_dir.mkdir(parents=True, exist_ok=True)

    ela_result = analyze_ela(
        image_path,
        ela_dir / "ela_map.jpg"
    )

    dct_result = analyze_dct(
        image_path,
        dct_dir
    )

    noise_result = analyze_noise(
        image_path,
        noise_dir
    )

    original = cv2.imread(str(image_path))
    height, width = original.shape[:2]

    ela_map = cv2.imread(
        str(ela_dir / "ela_map.jpg"),
        cv2.IMREAD_GRAYSCALE
    )

    dct_map = np.load(dct_dir / "dct_energy_map.npy")
    noise_map = np.load(noise_dir / "noise_magnitude.npy")

    ela_map = cv2.resize(ela_map, (width, height))
    dct_map = cv2.resize(dct_map, (width, height))
    noise_map = cv2.resize(noise_map, (width, height))

    ela_normalized = normalize_map(ela_map)
    dct_normalized = normalize_map(dct_map)
    noise_normalized = normalize_map(noise_map)

    evidence_map = (
        ela_normalized +
        dct_normalized +
        noise_normalized
    ) / 3.0

    np.save(output_dir / "combined_evidence.npy", evidence_map)

    plt.figure(figsize=(10, 8))
    plt.imshow(evidence_map, cmap="inferno", vmin=0, vmax=1)
    plt.colorbar(label="Relative combined signal")
    plt.title("TRACE-X | Combined Forensic Evidence")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(output_dir / "combined_evidence.png", dpi=200)
    plt.close()

    report = {
        "project": "TRACE-X",
        "input": str(image_path),
        "analysis": {
            "ela": ela_result,
            "dct": dct_result,
            "noise": noise_result
        },
        "fusion": {
            "method": "Equal-weight exploratory signal fusion",
            "mean_signal": float(np.mean(evidence_map)),
            "max_signal": float(np.max(evidence_map)),
            "note": "Relative forensic signal only; not a manipulation probability or proof."
        },
        "outputs": {
            "combined_map": str(output_dir / "combined_evidence.png"),
            "combined_array": str(output_dir / "combined_evidence.npy")
        }
    }

    with open(output_dir / "report.json", "w") as file:
        json.dump(report, file, indent=4)

    return report


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[2]

    image_path = root / "data" / "processed" / "ela_sample.jpg"
    output_dir = root / "results" / "trace_x"

    result = run_trace_x(image_path, output_dir)

    print("\nTRACE-X | INTEGRATED ANALYSIS")
    print("-" * 40)
    print("ELA mean difference:", result["analysis"]["ela"]["mean_difference"])
    print("DCT mean HF ratio:", result["analysis"]["dct"]["mean_high_frequency_ratio"])
    print("Noise mean magnitude:", result["analysis"]["noise"]["mean_magnitude"])
    print("Combined mean signal:", result["fusion"]["mean_signal"])
    print("\nReport:", output_dir / "report.json")
    print("Evidence map:", output_dir / "combined_evidence.png")