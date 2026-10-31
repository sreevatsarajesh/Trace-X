import cv2
import numpy as np


def analyze_dct(image, block_size=8, high_frequency_threshold=6):
    if image is None:
        raise ValueError("Image could not be decoded")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY).astype(np.float32)
    h, w = gray.shape
    pad_h = (block_size - h % block_size) % block_size
    pad_w = (block_size - w % block_size) % block_size
    gray = np.pad(gray, ((0, pad_h), (0, pad_w)), mode="reflect")
    mask = np.fromfunction(
        lambda u, v: (u + v) >= high_frequency_threshold,
        (block_size, block_size),
        dtype=int,
    )
    rows = []
    for y in range(0, gray.shape[0], block_size):
        row = []
        for x in range(0, gray.shape[1], block_size):
            coeff = cv2.dct(gray[y:y + block_size, x:x + block_size])
            ac = coeff.copy()
            ac[0, 0] = 0
            total = float(np.sum(ac ** 2))
            high = float(np.sum(coeff[mask] ** 2))
            row.append(high / (total + 1e-8))
        rows.append(row)
    block_map = np.asarray(rows, dtype=np.float32)
    full_map = cv2.resize(block_map, (w, h), interpolation=cv2.INTER_LINEAR)
    return {
        "map": full_map,
        "block_map": block_map,
        "mean_high_frequency_ratio": float(block_map.mean()),
        "std_high_frequency_ratio": float(block_map.std()),
        "blocks_processed": int(block_map.size),
    }
