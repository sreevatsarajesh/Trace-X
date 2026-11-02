import argparse,csv
from pathlib import Path
import cv2,numpy as np
from src.tracex.pipeline import run_trace_x
from src.tracex.metrics import binary_metrics

def main():
    p=argparse.ArgumentParser(); p.add_argument("--manifest",required=True); p.add_argument("--output",default="results/evaluation")
    p.add_argument("--threshold",type=float,default=.65); p.add_argument("--split",default=None); a=p.parse_args()
    manifest=Path(a.manifest).resolve(); out=Path(a.output); out.mkdir(parents=True,exist_ok=True)
    with manifest.open(newline="") as f: rows=list(csv.DictReader(f))
    if a.split and rows and "split" in rows[0]: rows=[r for r in rows if r["split"]==a.split]
    if not rows: raise ValueError("No rows selected")
    result=[]
    for i,r in enumerate(rows):
        ip=(manifest.parent/r["image"]).resolve(); mp=(manifest.parent/r["mask"]).resolve()
        _,evidence,_=run_trace_x(ip,out/f"sample_{i:05d}")
        mask=cv2.imread(str(mp),cv2.IMREAD_GRAYSCALE)
        if mask is None: raise ValueError(f"Cannot read mask {mp}")
        pred=cv2.resize(evidence,(mask.shape[1],mask.shape[0]))
        result.append({"image":str(ip),"source_id":r.get("source_id",""),**binary_metrics(pred,mask,a.threshold)})
    with (out/"metrics.csv").open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=result[0]); w.writeheader(); w.writerows(result)
    for k in ["precision","recall","f1","iou","false_positive_rate"]: print(f"Mean {k}: {np.mean([x[k] for x in result]):.4f}")
    print("Saved",out/"metrics.csv")
if __name__=="__main__":main()
