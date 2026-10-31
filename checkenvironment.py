import platform 
import cv2
import numpy as np
import torch 
print("TRACE-X Environment Check")
print("-" * 35)
print("Architecture:", platform.machine())
print("Python:", platform.python_version())
print("OpenCV:", cv2.__version__)
print("NumPy:", np.__version__)
print("PyTorch:", torch.__version__)
print("MPS Available:", torch.backends.mps.is_available())
if torch.backends.mps.is_available():
    device = torch.device("mps")
else:
    device = torch.device("cpu")
x = torch.randn(1000, 1000, device=device)
y = torch.matmul(x, x)
print("Selected Device:", device)
print("Tensor Test:", y.shape)
print("Environment Ready!")