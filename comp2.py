import numpy as np
from PIL import Image

def encode_sort_indices(arr):
    encoded = ''
    for num in arr:
        # 各インデックスを0パディングした文字列に変換
        encoded += str(num).zfill(5)
    return int(encoded)

def decode_sort_indices(encoded):
    encoded_str = str(encoded)
    return [int(encoded_str[i:i + 5]) for i in range(0, len(encoded_str), 5)]

def compress_image(image_path):
    image = Image.open(image_path)
    img_array = np.array(image).flatten()

    sorted_indices = np.argsort(img_array)
    sorted_array = img_array[sorted_indices]

    encoded_sort_indices = encode_sort_indices(sorted_indices)
    
    return sorted_array, encoded_sort_indices

def decompress_image(sorted_array, encoded_sort_indices, original_shape):
    sorted_indices = decode_sort_indices(encoded_sort_indices)
    img_array = np.zeros_like(sorted_array)
    img_array[sorted_indices] = sorted_array

    img_array = img_array.reshape(original_shape)
    decompressed_image = Image.fromarray(img_array)
    return decompressed_image

# Example usage
image_path = "path/image.png"
compressed_data = compress_image(image_path)
original_shape = Image.open(image_path).size[::-1]  # height, width

# Save compressed image and encoded sort indices
compressed_image = Image.fromarray(compressed_data[0].reshape(original_shape))
compressed_image.save("path/compressed_image.png")
with open("path/to/your/encoded_sort_indices.txt", "w") as f:
    f.write(str(compressed_data[1]))

# Load encoded sort indices
with open("path/encoded_sort_indices.txt", "r") as f:
    loaded_encoded_sort_indices = int(f.read())

# Decompress image
decompressed_img = decompress_image(compressed_data[0], loaded_encoded_sort_indices, original_shape)
decompressed_img.save("path/decompressed_image.png")
