from pathlib import Path
import cv2
import numpy as np
import matplotlib.pyplot as plt
def analyze_dct(image_path, output_dir):
    image_path = Path(image_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    image = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError(f"Unable to load image: {image_path}")
    height, width = image.shape
    pad_h = (8 - height % 8) % 8
    pad_w = (8 - width % 8) % 8
    image = np.pad(
        image.astype(np.float32),
        ((0, pad_h), (0, pad_w)),
        mode="reflect"
    )
    height, width = image.shape
    high_frequency_mask = np.fromfunction(
        lambda u, v: (u + v) >= 6,
        (8, 8),
        dtype=int
    )
    energy_map = []
    average_spectrum = np.zeros((8, 8), dtype=np.float64)
    for y in range(0, height, 8):
        row = []
        for x in range(0, width, 8):
            block = image[y:y + 8, x:x + 8]
            coefficients = cv2.dct(block)
            ac_coefficients = coefficients.copy()
            ac_coefficients[0, 0] = 0
            total_energy = np.sum(ac_coefficients ** 2)
            high_energy = np.sum(
                coefficients[high_frequency_mask] ** 2
            )
            high_frequency_ratio = (
                high_energy / (total_energy + 1e-8)
            )
            row.append(high_frequency_ratio)
            average_spectrum += np.abs(coefficients)
        energy_map.append(row)
    energy_map = np.array(energy_map)
    average_spectrum /= (
        (height // 8) * (width // 8)
    )
    np.save(
        output_dir / "dct_energy_map.npy",
        energy_map
    )
    plt.figure(figsize=(10, 8))
    plt.imshow(energy_map, cmap="inferno")
    plt.colorbar(label="High-frequency energy ratio")
    plt.title("TRACE-X | Block-wise DCT Energy")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(
        output_dir / "dct_energy_map.png",
        dpi=200
    )
    plt.close()
    plt.figure(figsize=(8, 6))
    plt.imshow(
        np.log1p(average_spectrum),
        cmap="viridis"
    )
    plt.colorbar(label="Log average coefficient magnitude")
    plt.title("TRACE-X | Average DCT Spectrum")
    plt.xlabel("Horizontal frequency")
    plt.ylabel("Vertical frequency")
    plt.tight_layout()
    plt.savefig(
        output_dir / "dct_spectrum.png",
        dpi=200
    )
    plt.close()
    return {
        "image_shape": (height, width),
        "blocks_processed": int(energy_map.size),
        "mean_high_frequency_ratio": float(np.mean(energy_map)),
        "std_high_frequency_ratio": float(np.std(energy_map)),
        "output_directory": str(output_dir)
    }