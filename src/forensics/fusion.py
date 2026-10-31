import numpy as np


def adaptive_fusion(ela_map, dct_map, noise_map, transformation):
    signals = {
        "ela": np.asarray(ela_map, dtype=np.float32),
        "dct": np.asarray(dct_map, dtype=np.float32),
        "noise": np.asarray(noise_map, dtype=np.float32)
    }

    weights = {
        "original": {"ela": 0.34, "dct": 0.33, "noise": 0.33},
        "jpeg": {"ela": 0.20, "dct": 0.20, "noise": 0.60},
        "resize": {"ela": 0.25, "dct": 0.50, "noise": 0.25},
        "crop": {"ela": 0.25, "dct": 0.50, "noise": 0.25},
        "unknown": {"ela": 0.34, "dct": 0.33, "noise": 0.33}
    }

    selected = weights.get(transformation, weights["unknown"])

    fused = sum(
        signals[name] * selected[name]
        for name in signals
    )

    return fused, selected