# imagesizer

A python package to resize images to maximum file size.

## Installation

`imagesizer` can be installed by running `pip install imagesizer`. It requires Python 3.9+ to run.

## Usage

Import `compress_to_size` to your file, and use it to compress your image:

```python
from imagesizer import compress_to_size
# Basic Example
compress_to_size("path/to/input/image.jpg", "path/to/output/image.jpg", max_size=1)

# Advanced Example
compress_to_size("path/to/input/image.jpg", "path/to/output/image.jpg", max_size=1000, unit="kb", compression_steps=1)
```

## Parameters
- `input_image_path`: Path to input image.
- `output_image_path`: Path to output image.
- `max_size`: Maximum size of output image (default in mb).
- `unit`: Unit for max_size (default is mb). Options are 'gb', 'mb', 'kb', 'byte'.
- `compression_steps`: Compression steps to take per iteration (integer, default 5). Larger steps are faster but might overcompress. Max 75 for non-PNG image, max 8 for PNG.

## Limitations
- PNG compression is limited: PNG is lossless so compression only affects how hard the algorithm works, not image quality. Large PNG files may not compress significantly below their original size.
- Non-PNG formats use lossy compression: image quality is reduced at each compression step, so aggressive compression will visibly degrade the image.
- `compression_steps` is a tradeoff: larger steps are faster but the output may end up smaller than necessary, since the algorithm cannot go back a step once it overshoots the target size.

## Development
To quickly get started, run `uv sync`. This will automatically create a `.venv` directory and installs all dependencies including development dependencies. To run tests use `uv run pytest tests/`. For code formatting use `uv run black .`.