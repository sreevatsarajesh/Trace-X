from pathlib import Path
import tempfile

import streamlit as st
from PIL import Image

from src.tracex.pipeline import run_trace_x

st.set_page_config(page_title="TRACE-X", page_icon="🔎", layout="wide")
st.title("TRACE-X")
st.caption("Transformation-resilient exploratory image-forensics prototype")
st.warning(
    "Research prototype only. Relative evidence maps are not manipulation probabilities "
    "or proof of tampering. Validate against ground-truth datasets before drawing conclusions."
)

uploaded = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png", "tif", "tiff"])
col1, col2, col3 = st.columns(3)
with col1:
    profile = st.selectbox("Known transformation profile", ["unknown", "jpeg", "resize", "crop"])
with col2:
    quality = st.slider("ELA recompression quality", 50, 95, 90)
with col3:
    sigma = st.slider("Noise residual sigma", 0.5, 3.0, 1.0, 0.5)

if uploaded:
    image = Image.open(uploaded).convert("RGB")
    st.image(image, caption="Input image", use_container_width=True)
    if st.button("Analyze image", type="primary"):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            image_path = tmp / f"input{Path(uploaded.name).suffix.lower()}"
            output_dir = tmp / "analysis"
            image.save(image_path)
            with st.spinner("Running forensic signal analysis..."):
                report, _ = run_trace_x(
                    image_path, output_dir, transformation=profile,
                    ela_quality=quality, noise_sigma=sigma
                )
            a, b = st.columns(2)
            a.image(str(output_dir / "evidence_map.png"), caption="Relative combined evidence map", use_container_width=True)
            b.image(str(output_dir / "overlay.png"), caption="Evidence overlay", use_container_width=True)
            st.subheader("Signal measurements")
            st.json(report["signals"])
            st.subheader("Fusion details")
            st.json(report["fusion"])
            st.download_button(
                "Download JSON report",
                data=(output_dir / "report.json").read_text(),
                file_name="tracex_report.json",
                mime="application/json"
            )
