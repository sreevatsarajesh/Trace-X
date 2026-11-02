from pathlib import Path
from PIL import Image

def profile_image(path):
    with Image.open(path) as im:
        w,h=im.size; fmt=(im.format or Path(path).suffix[1:]).lower()
    return {"format":fmt,"width":w,"height":h,"aspect_ratio":w/max(h,1),
            "profile":"jpeg" if fmt in ("jpeg","jpg") else "unknown",
            "limitation":"Metadata heuristic only; does not recover image processing history."}
