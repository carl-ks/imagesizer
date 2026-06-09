from imagesizer import compress_to_size

import pytest
import io
import tempfile
from PIL import Image

class TestBasicFunctions:
    def test_jpeg(self):        
        output_path = io.BytesIO()
        compress_to_size("tests/images/test_image.jpg", output_path, max_size=1)
        output_size = output_path.tell()
        assert output_size <= 1_000_000

    def test_jpeg_kb(self):        
        output_path = io.BytesIO()
        compress_to_size("tests/images/test_image.jpg", output_path, max_size=1_000, unit="kb")
        output_size = output_path.tell()
        assert output_size <= 1_000_000

    def test_jpeg_small_compression(self):        
        output_path = io.BytesIO()
        compress_to_size("tests/images/test_image.jpg", output_path, max_size=1, compression_steps=1)
        output_size = output_path.tell()
        assert output_size <= 1_000_000

    def test_jpeg_large_compression(self):        
        output_path = io.BytesIO()
        compress_to_size("tests/images/test_image.jpg", output_path, max_size=1, compression_steps=25)
        output_size = output_path.tell()
        assert output_size <= 1_000_000

    def test_jpeg_no_compression(self):        
        output_file = tempfile.NamedTemporaryFile()
        compress_to_size("tests/images/test_image.jpg", output_file.name, max_size=10)
        output_size = output_file.tell()
        assert output_size <= 10_000_000

    def test_png(self):        
        output_path = io.BytesIO()
        compress_to_size("tests/images/test_image.png", output_path, max_size=18)
        output_size = output_path.tell()
        assert output_size <= 18_000_000

    def test_webp(self):        
        output_path = io.BytesIO()
        compress_to_size("tests/images/test_image.webp", output_path, max_size=1)
        output_size = output_path.tell()
        assert output_size <= 1_000_000


def test_no_image():
    output_path = io.BytesIO()
    with pytest.raises(ValueError):
        compress_to_size("tests/images/test_image.pdf", output_path, max_size=1)

    with pytest.raises(ValueError):
        compress_to_size("tests/images/test_image.txt", output_path, max_size=1)

def test_wrong_unit():
    output_path = io.BytesIO()
    with pytest.raises(ValueError):
        compress_to_size("tests/images/test_image.jpg", output_path, max_size=1, unit="megabyte")

def test_max_size_not_possible():
    output_path = io.BytesIO()
    with pytest.raises(ValueError):
        compress_to_size("tests/images/test_image.jpg", output_path, max_size=0.01)

    with pytest.raises(ValueError):
        compress_to_size("tests/images/test_image.jpg", output_path, max_size=0)

    with pytest.raises(ValueError):
        compress_to_size("tests/images/test_image.jpg", output_path, max_size=-1)


def test_compression_steps():
    output_path = io.BytesIO()
    with pytest.raises(ValueError):
        compress_to_size("tests/images/test_image.jpg", output_path, max_size=1, compression_steps=5.5)

    with pytest.raises(ValueError):
            compress_to_size("tests/images/test_image.jpg", output_path, max_size=1, compression_steps=-1)

    with pytest.raises(ValueError):
            compress_to_size("tests/images/test_image.jpg", output_path, max_size=1, compression_steps=0)

def test_output_is_image():
    output_path = io.BytesIO()
    compress_to_size("tests/images/test_image.jpg", output_path, max_size=1)
    with Image.open(output_path) as im:
            assert im.size[0] > 0
            assert im.size[1] > 0

# compress_to_size("tests/images/test_image.png", "tests/images/test_image_test.png", max_size=17, compression_steps=1)