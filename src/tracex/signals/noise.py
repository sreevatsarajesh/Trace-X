import cv2
import numpy as np


def analyze_noise(image, sigma=1.0):
    if image is None:
        raise ValueError("Image could not be decoded")
    if sigma <= 0:
        raise ValueError("sigma must be positive")
    img = image.astype(np.float32)
    denoised = cv2.GaussianBlur(img, (0, 0), sigmaX=float(sigma), sigmaY=float(sigma))
    residual = img - denoised
    residual_gray = cv2.cvtColor(residual, cv2.COLOR_BGR2GRAY)
    magnitude = np.abs(residual_gray)
    return {
        "map": magnitude,
        "residual": residual,
        "mean_residual": float(residual_gray.mean()),
        "std_residual": float(residual_gray.std()),
        "mean_magnitude": float(magnitude.mean()),
        "max_magnitude": float(magnitude.max()),
        "sigma": float(sigma),
    }
