import numpy as np
from src.tracex.metrics import binary_metrics


def test_perfect_prediction():
    mask = np.array([[0, 1], [1, 0]], dtype=np.uint8)
    result = binary_metrics(mask, mask)
    assert result["f1"] == 1.0
    assert result["iou"] == 1.0


def test_empty_prediction():
    mask = np.array([[0, 1], [0, 0]], dtype=np.uint8)
    result = binary_metrics(np.zeros_like(mask), mask)
    assert result["recall"] == 0.0
    assert result["false_positive_rate"] == 0.0
