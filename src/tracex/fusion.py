import cv2
import numpy as np

WEIGHTS={"unknown":(.25,.25,.25,.25),"jpeg":(.15,.20,.20,.45),
         "resize":(.20,.35,.25,.20),"crop":(.20,.30,.30,.20),
         "screenshot":(.20,.25,.35,.20)}

def normalize(x):
    x=np.asarray(x,np.float32); lo,hi=np.percentile(x,[1,99])
    return np.clip((x-lo)/(hi-lo+1e-8),0,1)

def fuse_maps(maps, profile="unknown"):
    keys=("ela","dct","noise","jpeg_grid"); shape=maps["ela"].shape
    stack=[]
    for k in keys:
        a=np.asarray(maps[k],np.float32)
        if a.shape!=shape: a=cv2.resize(a,(shape[1],shape[0]))
        stack.append(normalize(a))
    weights=np.asarray(WEIGHTS.get(profile,WEIGHTS["unknown"]),np.float32); weights/=weights.sum()
    stack=np.stack(stack)
    return np.tensordot(weights,stack,axes=(0,0)).astype(np.float32), np.std(stack,axis=0), dict(zip(keys,weights.tolist()))
