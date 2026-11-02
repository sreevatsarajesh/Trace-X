# TRACE-X research protocol

Research question: can transformation-conditioned fusion improve localization robustness over fixed forensic signal fusion?

Current signals: ELA, block-DCT high-frequency energy, Gaussian-blur residual magnitude, and an 8-pixel boundary discontinuity cue. Each can respond to benign content and processing.

The current profiler reads format and dimensions; it does not reliably infer prior transformations. The profile can be supplied manually. Weights are heuristic placeholders. Per-image percentile normalization is visualization-oriented and can distort cross-image comparisons. Disagreement is not calibrated uncertainty.

Required experiments:
1. Audit dataset provenance, license, mask definitions and source IDs.
2. Split by source image before augmentation; keep all derivatives together.
3. Compare single-signal baselines, equal fusion and profile-conditioned fusion.
4. Include pristine images and benign edits to measure false positives.
5. Tune weights/thresholds on validation only; evaluate once on held-out test.
6. Report precision, recall, F1, IoU, FPR, calibration, runtime and cross-dataset performance.
7. Test unseen transformation chains and unknown-profile conditions.

Do not claim a validated detector or publication-level improvement until controlled, source-disjoint experiments and suitable baseline comparisons support it.
