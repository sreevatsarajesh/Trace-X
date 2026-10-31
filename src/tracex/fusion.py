import cv2
import numpy as np


DEFAULT_WEIGHTS = {
    "unknown": (1 / 3, 1 / 3, 1 / 3),
    "jpeg": (0.25, 0.25, 0.50),
    "resize": (0.30, 0.40, 0.30),
    "crop": (0.30, 0.40, 0.30),
}


def normalize_map(array):
    arr = np.asarray(array, dtype=np.float32)
    lo, hi = np.percentile(arr, [1, 99])
    if hi - lo < 1e-8:
        return np.zeros_like(arr, dtype=np.float32)
    return np.clip((arr - lo) / (hi - lo), 0, 1)


def adaptive_fusion(ela_map, dct_map, noise_map, transformation="unknown", weights=None):
    shapes = [np.asarray(x).shape for x in (ela_map, dct_map, noise_map)]
    target_h, target_w = shapes[0]
    maps = []
    for item in (ela_map, dct_map, noise_map):
        arr = np.asarray(item, dtype=np.float32)
        if arr.shape != (target_h, target_w):
            arr = cv2.resize(arr, (target_w, target_h), interpolation=cv2.INTER_LINEAR)
        maps.append(normalize_map(arr))

    weight_table = dict(DEFAULT_WEIGHTS)
    if weights:
        weight_table.update(weights)
    selected = weight_table.get(transformation, weight_table["unknown"])
    selected = np.asarray(selected, dtype=np.float32)
    if selected.shape != (3,) or np.any(selected < 0) or selected.sum() <= 0:
        raise ValueError("Fusion weights must be three nonnegative values with positive sum")
    selected = selected / selected.sum()
    fused = sum(w * m for w, m in zip(selected, maps))
    return fused.astype(np.float32), {
        "ela": float(selected[0]),
        "dct": float(selected[1]),
        "noise": float(selected[2]),
    }
