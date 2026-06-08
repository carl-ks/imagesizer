from imagesizer import compress_to_size

compress_to_size("./data/test_image11.jpg", "./data/test_image11_test.jpg", max_size=1.5, size_unit="mb", compression_steps=5)