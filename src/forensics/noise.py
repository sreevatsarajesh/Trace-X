from pathlib import Path
import cv2
import numpy as np
import matplotlib.pyplot as plt
def analyze_noise(image_path, output_dir, sigma=1.0):
    image_path = Path(image_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    image = cv2.imread(str(image_path), cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError(f"Unable to load image: {image_path}")
    if sigma <= 0:
        raise ValueError("Sigma must be positive.")
    image = image.astype(np.float32)
    denoised = cv2.GaussianBlur(
        image,
        (0, 0),
        sigmaX=sigma,
        sigmaY=sigma
    )
    residual = image - denoised
    residual_gray = cv2.cvtColor(
        residual,
        cv2.COLOR_BGR2GRAY
    )
    residual_magnitude = np.abs(residual_gray)
    mean_residual = float(np.mean(residual_gray))
    std_residual = float(np.std(residual_gray))
    mean_magnitude = float(np.mean(residual_magnitude))
    max_magnitude = float(np.max(residual_magnitude))
    np.save(
        output_dir / "noise_residual.npy",
        residual
    )
    np.save(
        output_dir / "noise_magnitude.npy",
        residual_magnitude
    )
    visualization = np.clip(
        residual_gray * 4 + 128,
        0,
        255
    ).astype(np.uint8)
    magnitude_visualization = np.clip(
        residual_magnitude * 4,
        0,
        255
    ).astype(np.uint8)
    cv2.imwrite(
        str(output_dir / "noise_residual.png"),
        visualization
    )
    cv2.imwrite(
        str(output_dir / "noise_magnitude.png"),
        magnitude_visualization
    )
    plt.figure(figsize=(10, 8))
    plt.imshow(residual_magnitude, cmap="inferno")
    plt.colorbar(label="Residual magnitude")
    plt.title("TRACE-X | Noise Residual Magnitude")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(
        output_dir / "noise_heatmap.png",
        dpi=200
    )
    plt.close()
    return {
        "image_shape": image.shape,
        "sigma": sigma,
        "mean_residual": mean_residual,
        "std_residual": std_residual,
        "mean_magnitude": mean_magnitude,
        "max_magnitude": max_magnitude,
        "output_directory": str(output_dir)
    }
