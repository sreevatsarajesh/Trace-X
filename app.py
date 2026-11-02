import tempfile
from pathlib import Path
import streamlit as st
from PIL import Image
from src.tracex.pipeline import run_trace_x
st.set_page_config(page_title="TRACE-X 2.0",page_icon="🔎",layout="wide")
st.title("TRACE-X 2.0")
st.caption("Exploratory transformation-resilient image-forensics framework")
st.warning("Research prototype: evidence maps are not manipulation probabilities or proof.")
upload=st.file_uploader("Upload image",type=["jpg","jpeg","png","tif","tiff"])
c1,c2=st.columns(2)
profile=c1.selectbox("Transformation profile",["auto","unknown","jpeg","resize","crop","screenshot"])
threshold=c2.slider("Exploratory threshold",.05,.95,.65,.05)
if upload and st.button("Analyze",type="primary"):
    with tempfile.TemporaryDirectory() as d:
        d=Path(d); path=d/("input"+Path(upload.name).suffix.lower()); Image.open(upload).save(path)
        with st.spinner("Analyzing forensic signals..."): report,_,_=run_trace_x(path,d/"out",profile,threshold)
        a,b=st.columns(2); a.image(str(d/"out/evidence_map.png"),caption="Relative evidence map"); b.image(str(d/"out/overlay.png"),caption="Overlay")
        st.image(str(d/"out/uncertainty_proxy.png"),caption="Signal disagreement proxy (not calibrated uncertainty)")
        st.json(report)
        st.download_button("Download JSON report",(d/"out/report.json").read_text(),"tracex_report.json")
