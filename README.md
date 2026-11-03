# TRACE-X 2.0
### Transformation-Resilient Adaptive Cross-platform Evidence Engine

**An exploratory digital image-forensics framework for analyzing image manipulation signals under common image transformations.**

TRACE-X investigates whether combining multiple forensic signals can provide more useful evidence when images undergo transformations such as JPEG compression, resizing, cropping, and blurring.

Rather than relying on a single detection technique, TRACE-X combines multiple image-analysis methods into an evidence-fusion pipeline and generates visual outputs to help users investigate suspicious image regions.

---

## Overview

Images shared through social media and messaging platforms frequently undergo compression, resizing, and other transformations. These operations can alter or weaken forensic traces, making image manipulation analysis more challenging.

TRACE-X explores a multi-signal approach to this problem.

The framework currently combines four forensic signals:

- **Error Level Analysis (ELA):** Examines differences introduced through JPEG recompression.
- **Discrete Cosine Transform (DCT):** Analyzes frequency-domain characteristics and high-frequency energy.
- **Noise Residual Analysis:** Examines residual patterns after smoothing an image.
- **JPEG Grid Analysis:** Examines discontinuities associated with JPEG block boundaries.

These signals are processed through a heuristic, profile-conditioned evidence-fusion mechanism to generate a combined evidence map.

## Key Features

| Feature | Description |
|---|---|
| Multi-signal analysis | Combines four forensic analysis techniques |
| Image profiling | Uses basic image properties to select an analysis profile |
| Adaptive evidence fusion | Applies profile-conditioned heuristic weights |
| Evidence localization | Produces visual maps highlighting relative signal intensity |
| Disagreement analysis | Visualizes differences between forensic signals |
| Transformation testing | Tests JPEG compression, resizing, cropping and blur |
| Quantitative evaluation | Supports precision, recall, F1, IoU and false-positive-rate evaluation |
| HTML reporting | Converts JSON results into readable forensic reports |
| CLI interface | Runs analysis and experiments from the terminal |

## Architecture

```text
                    Input Image
                         |
                         v
                 Image Profiling
                         |
             +-----------+-----------+
             |           |           |
             v           v           v
            ELA         DCT        Noise
             |           |           |
             +-----------+-----------+
                         |
                         v
                   JPEG Grid
                         |
                         v
                Evidence Fusion
                         |
              +----------+----------+
              |          |          |
              v          v          v
          Evidence   Disagreement  Threshold
            Map         Map          Mask
              |          |          |
              +----------+----------+
                         |
                         v
                  Report Generation
                    /         \
                   v           v
                JSON         HTML
```

## Project Structure

```text
TRACE-X/
│
├── configs/
│   └── default.yaml
│
├── data/
│   └── README.md
│
├── docs/
│   └── RESEARCH_PROTOCOL.md
│
├── experiments/
│   └── run_paired_evaluation.py
│
├── results/
│   └── demo/
│
├── src/
│   └── tracex/
│       ├── signals/
│       │   ├── ela.py
│       │   ├── dct.py
│       │   ├── noise.py
│       │   └── jpeg_grid.py
│       │
│       ├── profiler.py
│       ├── fusion.py
│       ├── transformations.py
│       ├── pipeline.py
│       ├── metrics.py
│       └── cli.py
│
├── tests/
│   └── test_core.py
│
├── app.py
├── generate_html_report.py
├── requirements.txt
├── LICENSE
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/Trace-X.git
cd Trace-X
```

### 2. Create a virtual environment

Python 3.11 or 3.12 is recommended.

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Usage

### 1. Analyze an image

Place your test image inside the `data/` directory.

Run:

```bash
python -m src.tracex.cli analyze "data/your-image.jpg"
```

The pipeline performs forensic analysis and generates the corresponding outputs.

### 2. Generate a readable HTML report

TRACE-X maintains JSON output for machine-readable results and research experiments.

To generate a human-readable report:

```bash
python generate_html_report.py results/demo/report.json
```

Open the generated report:

```bash
open results/demo/report.html
```

Replace the report path if your analysis was saved in a different directory.

### 3. Run transformation experiments

TRACE-X supports experiments involving:

- JPEG compression
- Image resizing
- Cropping
- Gaussian blur

Use the transformation and robustness commands exposed by the CLI:

```bash
python -m src.tracex.cli transform --help
python -m src.tracex.cli robustness --help
```

### 4. Run the dashboard

```bash
streamlit run app.py
```

### 5. Run tests

```bash
python -m pytest -q
```

## Understanding the Outputs

A typical analysis directory contains:

| Output | Purpose |
|---|---|
| `report.json` | Structured analysis results |
| `report.html` | Human-readable analysis report |
| `evidence_map.png` | Combined relative evidence visualization |
| `overlay.png` | Evidence visualization overlaid on the input image |
| `threshold_mask.png` | Exploratory threshold-based evidence mask |
| `uncertainty_proxy.png` | Signal disagreement visualization |
| `evidence_map.npy` | Numerical evidence map |
| `disagreement_map.npy` | Numerical disagreement map |

**Important:** Evidence maps indicate relative forensic signal strength. They are not calibrated manipulation probabilities. A highlighted region does not establish that an image has been altered.

## Research Direction

TRACE-X is being developed around the following research question:

> Can an adaptive multi-signal forensic system detect and localize image manipulations more reliably than fixed forensic detectors after images undergo unknown social-media-style transformations?

The proposed research direction includes:

1. Transformation-aware image profiling.
2. Adaptive forensic evidence weighting.
3. Multi-signal fusion and disagreement analysis.
4. Robustness evaluation under image transformations.
5. Quantitative localization and detection evaluation.
6. Cross-dataset generalization.

The current implementation is an experimental baseline. Establishing research novelty and effectiveness requires controlled comparisons against established forensic methods.

## Evaluation

The framework includes support for evaluating localization predictions against ground-truth masks.

Metrics include:

- Precision
- Recall
- F1-score
- Intersection over Union (IoU)
- False Positive Rate

Future experiments should also investigate:

- Cross-dataset generalization.
- Robustness under multiple transformations.
- Runtime and computational efficiency.
- Calibration and uncertainty estimation.
- Ablation studies for individual forensic signals.

For valid evaluation, transformed derivatives of the same original image must remain within the same dataset split to prevent data leakage.

## Current Limitations

TRACE-X 2.0 is an exploratory research framework, not a validated forensic detection product.

Current limitations include:

- The fusion weights are heuristic rather than learned.
- Image profiling uses basic metadata rather than a trained transformation classifier.
- The noise residual method is not a complete camera PRNU analysis.
- JPEG grid analysis is a heuristic signal.
- The threshold mask is not a trained segmentation model.
- Signal disagreement is not calibrated statistical uncertainty.
- No forensic output should be treated as definitive proof of manipulation.

These limitations define important areas for future development.

## Roadmap

- [x] Implement ELA analysis.
- [x] Implement DCT frequency analysis.
- [x] Implement noise residual analysis.
- [x] Implement JPEG grid analysis.
- [x] Build multi-signal evidence fusion.
- [x] Implement transformation experiments.
- [x] Generate evidence and disagreement maps.
- [x] Add quantitative evaluation utilities.
- [x] Add JSON reporting.
- [x] Add human-readable HTML reporting.
- [ ] Integrate publicly available image-forensics datasets.
- [ ] Establish reliable train, validation and test splits.
- [ ] Implement learned transformation profiling.
- [ ] Develop and validate adaptive fusion.
- [ ] Compare against established forensic baselines.
- [ ] Conduct ablation and cross-dataset experiments.

## Technology Stack

- Python
- NumPy
- OpenCV
- Pillow
- SciPy
- Matplotlib
- PyYAML
- Streamlit
- Pytest

## License

This project is distributed under the MIT License. See [LICENSE](LICENSE) for details.

## Author

**Sreevatsa Rajesh**

Mathematics and Computing Undergraduate  
Interested in Digital Forensics, Computer Vision, Machine Learning and Cybersecurity.

---

*TRACE-X 2.0 — Exploring more resilient image-forensics analysis through multi-signal evidence.*
