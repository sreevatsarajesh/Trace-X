import numpy as np
from src.tracex.fusion import adaptive_fusion


def test_fusion_shape_and_range():
    a = np.arange(64, dtype=np.float32).reshape(8, 8)
    fused, weights = adaptive_fusion(a, a, a, "unknown")
    assert fused.shape == (8, 8)
    assert fused.min() >= 0
    assert fused.max() <= 1
    assert abs(sum(weights.values()) - 1) < 1e-6


def test_fusion_rejects_invalid_weights():
    a = np.ones((4, 4), dtype=np.float32)
    try:
        adaptive_fusion(a, a, a, weights={"unknown": (-1, 1, 1)})
    except ValueError:
        return
    raise AssertionError("Expected invalid weights to fail")
