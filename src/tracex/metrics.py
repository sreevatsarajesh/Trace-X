import numpy as np


def binary_metrics(prediction, ground_truth, threshold=0.5):
    pred = np.asarray(prediction) >= threshold
    truth = np.asarray(ground_truth) > 0
    if pred.shape != truth.shape:
        raise ValueError("Prediction and ground-truth mask must have identical shapes")
    tp = int(np.logical_and(pred, truth).sum())
    fp = int(np.logical_and(pred, ~truth).sum())
    fn = int(np.logical_and(~pred, truth).sum())
    tn = int(np.logical_and(~pred, ~truth).sum())
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    iou = tp / (tp + fp + fn) if tp + fp + fn else 0.0
    fpr = fp / (fp + tn) if fp + tn else 0.0
    return {
        "tp": tp, "fp": fp, "fn": fn, "tn": tn,
        "precision": precision, "recall": recall,
        "f1": f1, "iou": iou, "false_positive_rate": fpr,
    }
