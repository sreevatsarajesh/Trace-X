from PIL import Image
from src.tracex.transformations import apply_transformations


def test_transformations_create_files(tmp_path):
    image = Image.new("RGB", (128, 128), (120, 80, 40))
    source = tmp_path / "source.jpg"
    image.save(source)
    outputs = apply_transformations(source, tmp_path / "variants")
    assert len(outputs) == 5
    assert all((tmp_path / "variants" / f"{name}.jpg").exists() for name in outputs)
