from pathlib import Path
import json, cv2, numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image
from .signals.ela import analyze_ela
from .signals.dct import analyze_dct
from .signals.noise import analyze_noise
from .signals.jpeg_grid import analyze_jpeg_grid
from .profiler import profile_image
from .fusion import fuse_maps

def run_trace_x(path,out,transformation="auto",threshold=.65):
    path,out=Path(path),Path(out); out.mkdir(parents=True,exist_ok=True)
    image=cv2.imread(str(path))
    if image is None: raise ValueError(f"Cannot read image: {path}")
    h,w=image.shape[:2]; prof=profile_image(path)
    selected=prof["profile"] if transformation=="auto" else transformation
    ela_path=path; temp=None
    if path.suffix.lower() not in (".jpg",".jpeg"):
        temp=out/"_ela_temp.jpg"; Image.fromarray(cv2.cvtColor(image,cv2.COLOR_BGR2RGB)).save(temp,quality=95); ela_path=temp
    e=analyze_ela(ela_path); d=analyze_dct(image); n=analyze_noise(image); j=analyze_jpeg_grid(image)
    fused,disagreement,weights=fuse_maps({"ela":e["map"],"dct":d["map"],"noise":n["map"],"jpeg_grid":j["map"]},selected)
    mask=(fused>=threshold).astype(np.uint8)*255
    color=cv2.applyColorMap(np.uint8(np.clip(fused,0,1)*255),cv2.COLORMAP_INFERNO)
    cv2.imwrite(str(out/"overlay.png"),cv2.addWeighted(image,.58,color,.42,0))
    cv2.imwrite(str(out/"threshold_mask.png"),mask)
    np.save(out/"evidence_map.npy",fused); np.save(out/"disagreement_map.npy",disagreement)
    for name,array in [("evidence_map.png",fused),("uncertainty_proxy.png",disagreement)]:
        plt.figure(figsize=(8,6)); plt.imshow(array,cmap="inferno"); plt.colorbar(); plt.axis("off"); plt.tight_layout(); plt.savefig(out/name,dpi=140); plt.close()
    report={"project":"TRACE-X 2.0","input":str(path),"dimensions":[w,h],"image_profile":prof,
      "fusion_profile":selected,"signals":{"ela_mean_difference":e["mean_difference"],
      "dct_mean_high_frequency_ratio":d["mean_high_frequency_ratio"],
      "noise_mean_magnitude":n["mean_magnitude"],"jpeg_grid_boundary_strength":j["mean_boundary_strength"]},
      "fusion":{"weights":weights,"mean_relative_evidence":float(fused.mean()),"threshold":threshold,
      "thresholded_pixel_fraction":float((mask>0).mean())},
      "uncertainty_proxy":{"mean_disagreement":float(disagreement.mean()),"note":"Signal disagreement only; not calibrated confidence."},
      "limitations":["Heuristic signals and weights; not a validated detector.","Evidence is not a manipulation probability or proof.","Threshold mask is exploratory, not a trained segmentation output."]}
    (out/"report.json").write_text(json.dumps(report,indent=2))
    if temp and temp.exists():temp.unlink()
    return report,fused,disagreement
