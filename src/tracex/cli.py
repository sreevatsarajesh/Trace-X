import argparse
import csv
import json
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

from .pipeline import run_trace_x
from .transformations import apply_transformations, infer_transformation


def analyze_command(args):
    report, _ = run_trace_x(
        args.image, args.output, transformation=args.transformation,
        ela_quality=args.ela_quality, noise_sigma=args.noise_sigma
    )
    print(json.dumps(report, indent=2))


def transform_command(args):
    results = apply_transformations(args.image, args.output)
    for name, path in results.items():
        print(f"{name}: {path}")


def robustness_command(args):
    original = Path(args.image)
    variants_dir = Path(args.variants)
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    candidates = [("original", original)]
    candidates.extend((p.stem, p) for p in sorted(variants_dir.glob("*")) if p.suffix.lower() in {".jpg", ".jpeg", ".png"})
    rows = []
    for label, path in candidates:
        profile = infer_transformation(label)
        report, _ = run_trace_x(path, output / label, transformation=profile)
        signals = report["signals"]
        rows.append({
            "image": label,
            "transformation": profile,
            "ela_mean_difference": signals["ela"]["mean_difference"],
            "dct_mean_hf_ratio": signals["dct"]["mean_high_frequency_ratio"],
            "noise_mean_magnitude": signals["noise"]["mean_magnitude"],
            "fusion_mean_relative_signal": report["fusion"]["mean_relative_signal"],
        })
    csv_path = output / "robustness_results.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"Saved {csv_path}")
    for row in rows:
        print(row)


def main():
    parser = argparse.ArgumentParser(prog="tracex")
    sub = parser.add_subparsers(dest="command", required=True)

    analyze = sub.add_parser("analyze")
    analyze.add_argument("image")
    analyze.add_argument("--output", default="results/analysis")
    analyze.add_argument("--transformation", default="unknown", choices=["unknown", "jpeg", "resize", "crop"])
    analyze.add_argument("--ela-quality", type=int, default=90)
    analyze.add_argument("--noise-sigma", type=float, default=1.0)
    analyze.set_defaults(func=analyze_command)

    transform = sub.add_parser("transform")
    transform.add_argument("image")
    transform.add_argument("--output", default="data/transformed")
    transform.set_defaults(func=transform_command)

    robust = sub.add_parser("robustness")
    robust.add_argument("image")
    robust.add_argument("--variants", default="data/transformed")
    robust.add_argument("--output", default="results/robustness")
    robust.set_defaults(func=robustness_command)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
