from pathlib import Path

import cv2
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

from .fusion import adaptive_fusion
from .signals.ela import analyze_ela
from .signals.dct import analyze_dct
from .signals.noise import analyze_noise


def _load_image(path):
    image = cv2.imread(str(path), cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError(f"Could not read image: {path}")
    return image


def _save_heatmap(array, path, title):
    plt.figure(figsize=(9, 7))
    plt.imshow(array, cmap="inferno", vmin=0, vmax=1)
    plt.colorbar(label="Relative signal (0–1)")
    plt.title(title)
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(path, dpi=160)
    plt.close()


def run_trace_x(image_path, output_dir, transformation="unknown",
                ela_quality=90, ela_scale=10, noise_sigma=1.0):
    image_path = Path(image_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    image = _load_image(image_path)
    h, w = image.shape[:2]

    ela_input = image_path
    temporary_jpeg = None
    if image_path.suffix.lower() not in {".jpg", ".jpeg"}:
        temporary_jpeg = output_dir / "_ela_input.jpg"
        Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)).save(
            temporary_jpeg, "JPEG", quality=95
        )
        ela_input = temporary_jpeg

    ela = analyze_ela(ela_input, quality=ela_quality, scale=ela_scale)
    dct = analyze_dct(image)
    noise = analyze_noise(image, sigma=noise_sigma)

    ela_map = cv2.resize(ela["map"], (w, h), interpolation=cv2.INTER_LINEAR)
    fused, selected_weights = adaptive_fusion(
        ela_map, dct["map"], noise["map"], transformation=transformation
    )

    overlay = cv2.applyColorMap(
        np.uint8(np.clip(fused, 0, 1) * 255), cv2.COLORMAP_INFERNO
    )
    overlay = cv2.addWeighted(image, 0.55, overlay, 0.45, 0)
    overlay_path = output_dir / "overlay.png"
    cv2.imwrite(str(overlay_path), overlay)
    _save_heatmap(fused, output_dir / "evidence_map.png", "TRACE-X | Relative forensic evidence")

    np.save(output_dir / "evidence_map.npy", fused)
    report = {
        "project": "TRACE-X",
        "input": str(image_path),
        "image_width": int(w),
        "image_height": int(h),
        "transformation_profile": transformation,
        "signals": {
            "ela": {
                "mean_difference": ela["mean_difference"],
                "max_difference": ela["max_difference"],
                "jpeg_quality": ela_quality,
            },
            "dct": {
                "mean_high_frequency_ratio": dct["mean_high_frequency_ratio"],
                "std_high_frequency_ratio": dct["std_high_frequency_ratio"],
                "blocks_processed": dct["blocks_processed"],
            },
            "noise": {
                "mean_residual": noise["mean_residual"],
                "std_residual": noise["std_residual"],
                "mean_magnitude": noise["mean_magnitude"],
                "max_magnitude": noise["max_magnitude"],
                "sigma": noise_sigma,
            },
        },
        "fusion": {
            "method": "heuristic weighted fusion of per-image normalized maps",
            "weights": selected_weights,
            "mean_relative_signal": float(fused.mean()),
            "max_relative_signal": float(fused.max()),
            "warning": "Not a manipulation probability, calibrated confidence, or proof of tampering.",
        },
        "artifacts": {
            "evidence_map": str(output_dir / "evidence_map.png"),
            "overlay": str(overlay_path),
            "array": str(output_dir / "evidence_map.npy"),
        },
    }
    import json
    with open(output_dir / "report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    if temporary_jpeg and temporary_jpeg.exists():
        temporary_jpeg.unlink()
    return report, fused
