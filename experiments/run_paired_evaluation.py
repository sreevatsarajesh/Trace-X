import argparse
import csv
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

from src.tracex.pipeline import run_trace_x
from src.tracex.metrics import binary_metrics


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--output", default="results/evaluation")
    parser.add_argument("--threshold", type=float, default=0.5)
    args = parser.parse_args()

    manifest = Path(args.manifest).resolve()
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    rows = []

    with manifest.open(newline="", encoding="utf-8") as f:
        entries = list(csv.DictReader(f))

    for index, item in enumerate(entries):
        image_path = (manifest.parent / item["image"]).resolve()
        mask_path = (manifest.parent / item["mask"]).resolve()
        report, evidence = run_trace_x(image_path, output / f"sample_{index:04d}")
        mask = cv2.imread(str(mask_path), cv2.IMREAD_GRAYSCALE)
        if mask is None:
            raise ValueError(f"Cannot read mask: {mask_path}")
        resized = cv2.resize(evidence, (mask.shape[1], mask.shape[0]), interpolation=cv2.INTER_LINEAR)
        metrics = binary_metrics(resized, mask, threshold=args.threshold)
        rows.append({"image": str(image_path), **metrics})

    csv_path = output / "metrics.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"Evaluated {len(rows)} pairs. Results: {csv_path}")
    for key in ("precision", "recall", "f1", "iou", "false_positive_rate"):
        print(f"Mean {key}: {np.mean([r[key] for r in rows]):.4f}")


if __name__ == "__main__":
    main()
