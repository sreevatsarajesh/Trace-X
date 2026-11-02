import numpy as np
from PIL import Image
from src.tracex.fusion import fuse_maps
from src.tracex.metrics import binary_metrics
from src.tracex.transformations import apply_transformations

def test_fusion():
    x=np.arange(64,dtype=np.float32).reshape(8,8)
    fused,disagreement,weights=fuse_maps({k:x for k in ["ela","dct","noise","jpeg_grid"]})
    assert fused.shape==x.shape and disagreement.shape==x.shape
    assert abs(sum(weights.values())-1)<1e-6

def test_metrics():
    x=np.array([[0,1],[1,0]],dtype=np.uint8)
    assert binary_metrics(x,x)["f1"]==1

def test_transforms(tmp_path):
    source=tmp_path/"a.jpg"; Image.new("RGB",(128,128)).save(source)
    assert len(apply_transformations(source,tmp_path/"variants"))==6
