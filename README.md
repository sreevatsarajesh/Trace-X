# TRACE-X 2.0
Transformation-Resilient Adaptive Cross-platform Evidence Engine.

Experimental image-forensics framework with ELA, block-DCT, noise residuals, JPEG-grid cues, heuristic transformation profiling, weighted evidence fusion, exploratory localization maps, disagreement visualization, transformations, paired-mask evaluation, CLI and Streamlit UI.

## Limitations
This is a research prototype, not a validated manipulation detector. Maps are not probabilities or proof. Profiles are heuristic; weights are hand-designed; disagreement is not calibrated uncertainty; threshold masks are not trained segmentation predictions. Validate against source-disjoint ground-truth data before making performance claims.

## Install
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run
```bash
python -m tracex.cli analyze path/to/image.jpg --output results/demo
python -m tracex.cli transform path/to/image.jpg --output data/transformed
python -m tracex.cli robustness path/to/image.jpg --variants data/transformed --output results/robustness
streamlit run app.py
pytest -q
```

## Evaluation manifest
CSV columns: `image,mask,split,source_id`. Paths are relative to the manifest directory or absolute. Manipulated mask pixels must be nonzero.
```csv
image,mask,split,source_id
images/a.jpg,masks/a.png,test,source-a
```
```bash
python experiments/run_paired_evaluation.py --manifest data/manifest.csv --output results/evaluation --split test
```
Split by original source BEFORE creating transformed variants. Keep all derivatives together. Tune weights/thresholds on validation only. Compare individual signals, fixed fusion, profile-conditioned fusion, and pristine/benign-edit false positives.
