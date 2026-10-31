# TRACE-X research protocol

## Research question
Can transformation-aware weighting of multiple forensic signals improve manipulation localization under unseen image-processing transformations compared with fixed fusion?

## Hypothesis (to test, not assume)
A transformation-conditioned fusion strategy may preserve useful localization evidence better than a fixed equal-weight fusion strategy under selected transformation families.

## Required experiments
1. **Dataset audit:** record source IDs, manipulation types, mask availability, image dimensions, license and provenance.
2. **Leakage-safe split:** split by original source image before creating transformed copies. Never place derivatives of one source in different splits.
3. **Baselines:** ELA-only, DCT-only, noise-only, equal-weight fusion, heuristic profile-conditioned fusion.
4. **Transformations:** JPEG quality levels, resize ratios, crop ratios, blur, screenshot/re-encode if available. Record exact parameters and random seeds.
5. **Metrics:** pixel precision, recall, F1, IoU, false-positive rate, image-level metrics, calibration, runtime and memory.
6. **Ablations:** remove each signal, vary weights, vary transformation profile accuracy, compare known versus unknown profile.
7. **Generalization:** tune only on training/validation data; reserve source-disjoint and ideally dataset-disjoint test sets.

## Current implementation status
The repository implements classical signal extraction, heuristic fusion, basic transformation generation, visualization and paired-mask metric calculation. It does not yet contain a trained model, a learned transformation profiler, calibrated confidence, or validated adaptive weights.

## Reporting rule
Report measured outcomes exactly. Do not label the map as a probability or claim detection accuracy without held-out ground-truth evaluation. Include benign edits and pristine images to quantify false alarms.
