import cv2
import numpy as np

def analyze_noise(image, sigma=1.0):
    if sigma <= 0: raise ValueError("sigma must be positive")
    f=image.astype(np.float32)
    residual=f-cv2.GaussianBlur(f,(0,0),sigmaX=sigma,sigmaY=sigma)
    gray=cv2.cvtColor(residual,cv2.COLOR_BGR2GRAY); mag=np.abs(gray)
    return {"map":mag,"mean_residual":float(gray.mean()),"std_residual":float(gray.std()),
            "mean_magnitude":float(mag.mean()),"max_magnitude":float(mag.max())}
