import argparse,csv
from pathlib import Path
from .pipeline import run_trace_x
from .transformations import apply_transformations,infer_transformation

def main():
    p=argparse.ArgumentParser(); sub=p.add_subparsers(dest="cmd",required=True)
    a=sub.add_parser("analyze"); a.add_argument("image"); a.add_argument("--output",default="results/demo")
    a.add_argument("--transformation",default="auto",choices=["auto","unknown","jpeg","resize","crop","screenshot"])
    a.add_argument("--threshold",type=float,default=.65)
    t=sub.add_parser("transform"); t.add_argument("image"); t.add_argument("--output",default="data/transformed")
    r=sub.add_parser("robustness"); r.add_argument("image"); r.add_argument("--variants",default="data/transformed"); r.add_argument("--output",default="results/robustness")
    args=p.parse_args()
    if args.cmd=="analyze": print(run_trace_x(args.image,args.output,args.transformation,args.threshold)[0])
    elif args.cmd=="transform": print(apply_transformations(args.image,args.output))
    else:
        out=Path(args.output); out.mkdir(parents=True,exist_ok=True); items=[("original",Path(args.image))]
        items += [(x.stem,x) for x in sorted(Path(args.variants).glob("*")) if x.suffix.lower() in (".jpg",".jpeg",".png")]
        rows=[]
        for name,path in items:
            rep,_,_=run_trace_x(path,out/name,infer_transformation(name))
            rows.append({"image":name,"profile":rep["fusion_profile"],**rep["signals"],"mean_evidence":rep["fusion"]["mean_relative_evidence"]})
        with (out/"robustness.csv").open("w",newline="") as f:
            writer=csv.DictWriter(f,fieldnames=rows[0]); writer.writeheader(); writer.writerows(rows)
        print(out/"robustness.csv")

if __name__=="__main__":main()
