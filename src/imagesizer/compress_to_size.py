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

def compress_to_size(input_image_path, output_image_path, max_size, unit="mb", compression_steps = 5):

    if unit not in BYTES_CONVERSION:
        raise ValueError(f"Invalid unit '{unit}'. Must be one of: {list(BYTES_CONVERSION.keys())}")

    if max_size <= 0:
        raise ValueError(f"Invalid max_size '{max_size}. Must be larger that 0.'")

    if not isinstance(compression_steps, int):
        raise ValueError(f"Invalid compression_steps '{compression_steps}. Must be an integer.'")

    if compression_steps <= 0:
        raise ValueError(f"Invalid compression_steps '{compression_steps}. Must be larger that 0.'")

    max_size_bytes = max_size * BYTES_CONVERSION[unit]

    try:
        with Image.open(input_image_path) as im:
            im.verify()
            file_format = im.format
    except Exception as e:
        raise ValueError(f"Exception: Uploaded file is broken or not an image. Details: {e}")

    if file_format.lower() == "png" and compression_steps >= 9:
        raise ValueError(f"Invalid compression_steps '{compression_steps}. Compression steps for png must be lower or equal to 8.")  

    with open(input_image_path, "rb") as im:
        original_filesize = get_file_size(im)

    filesize = original_filesize

    if filesize <= max_size_bytes:
        shutil.copyfile(input_image_path, output_image_path)          
        
    else:
        with Image.open(input_image_path) as im:

            if file_format.lower() != "png":
                quality_level = 85
                min_quality = 10
                while quality_level >= min_quality:
                    byte_arr = io.BytesIO()
                    im.save(byte_arr, format=file_format, quality=quality_level)
                    filesize = get_file_size(byte_arr)

                    if filesize <= max_size_bytes:
                        break

                    quality_level -= compression_steps
                else:
                    raise ValueError("Could not compress image below max_size_bytes")
        
                im.save(output_image_path, format=file_format, quality=quality_level)

            else:
                compression_level = 1
                max_compression = 9
                while compression_level <= max_compression:
                    byte_arr = io.BytesIO()
                    im.save(byte_arr, format=file_format, compress_level=compression_level, optimize=True)
                    filesize = get_file_size(byte_arr)

                    if filesize <= max_size_bytes:
                        break

                    compression_level += compression_steps
                else:
                    raise ValueError("Could not compress png image below max_size_bytes")

                im.save(output_image_path, format=file_format, compress_level=compression_level, optimize=True)