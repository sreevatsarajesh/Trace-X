import numpy as np

def analyze_jpeg_grid(image, period=8):
    gray=image.astype(np.float32).mean(axis=2); h,w=gray.shape
    dx=np.abs(np.diff(gray,axis=1)); dy=np.abs(np.diff(gray,axis=0))
    xs=dx.mean(axis=0); ys=dy.mean(axis=1)
    xb=np.arange(len(xs))%period==period-1; yb=np.arange(len(ys))%period==period-1
    xscore=float(xs[xb].mean()) if xb.any() else 0.0
    yscore=float(ys[yb].mean()) if yb.any() else 0.0
    m=np.zeros((h,w),np.float32); m[:,1:]+=np.tile(xs,(h,1)); m[1:,:]+=np.tile(ys[:,None],(1,w))
    return {"map":m,"mean_boundary_strength":(xscore+yscore)/2}
