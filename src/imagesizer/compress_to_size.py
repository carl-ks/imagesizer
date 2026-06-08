from PIL import Image
import io
import shutil

BYTES_CONVERSION = {
    "gb": 1_000_000_000,
    "mb": 1_000_000,
    "kb": 1_000,
    "byte": 1,
}

def get_file_size(file):
    file.seek(0, 2)
    filesize = file.tell()
    file.seek(0)
    return filesize

def compress_to_size(input_image_path, output_image_path, max_size, size_unit="mb", compression_steps = 5):

    if size_unit not in BYTES_CONVERSION:
            raise ValueError(f"Invalid size_unit '{size_unit}'. Must be one of: {list(BYTES_CONVERSION.keys())}")

    max_size_bytes = max_size * BYTES_CONVERSION[size_unit]

    try:
        with Image.open(input_image_path) as im:
            im.verify()
            file_format = im.format
    except Exception as e:
        raise ValueError(f"Exception: Uploaded file is broken or not an image. Details: {e}")

    with open(input_image_path, "rb") as im:
        original_filesize = get_file_size(im)

    filesize = original_filesize

    if filesize <= max_size_bytes:
        shutil.copyfile(input_image_path, output_image_path)          
        
    else:

        compression_factor = 85
        min_quality = 10

        with Image.open(input_image_path) as im:

            while compression_factor >= min_quality:
                byte_arr = io.BytesIO()
                im.save(byte_arr, format=file_format, quality=compression_factor)
                filesize = get_file_size(byte_arr)

                if filesize <= max_size_bytes:
                    break

                compression_factor -= compression_steps
            
            else:
                raise ValueError("Could not compress image below max_size_bytes")
        
            im.save(output_image_path, format=file_format, quality=compression_factor)