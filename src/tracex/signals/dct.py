import cv2
import numpy as np

def analyze_dct(image, block=8, threshold=6):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY).astype(np.float32)
    h, w = gray.shape
    gray = np.pad(gray, ((0, (block-h%block)%block), (0, (block-w%block)%block)), mode="reflect")
    mask = np.fromfunction(lambda u,v: u+v >= threshold, (block,block), dtype=int)
    rows = []
    for y in range(0, gray.shape[0], block):
        row=[]
        for x in range(0, gray.shape[1], block):
            c=cv2.dct(gray[y:y+block,x:x+block]); ac=c.copy(); ac[0,0]=0
            row.append(float(np.sum(c[mask]**2)/(np.sum(ac**2)+1e-8)))
        rows.append(row)
    bm=np.asarray(rows,dtype=np.float32)
    return {"map":cv2.resize(bm,(w,h)), "mean_high_frequency_ratio":float(bm.mean()),
            "std_high_frequency_ratio":float(bm.std()), "blocks_processed":int(bm.size)}
