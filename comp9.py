import numpy as np
from PIL import Image

def encode_sort_indices(arr):
    perm = np.argsort(arr)
    inv = np.zeros_like(perm)
    for i, p in enumerate(perm):
        inv[p] = i
    return inv

def decode_sort_indices(encoded, size):
    perm = np.zeros_like(encoded)
    for i, inv in enumerate(encoded):
        perm[inv] = i
    return perm

def compress_image(image_path):
    image = Image.open(image_path).convert("L")
    img_array = np.array(image).flatten()

    sorted_indices = np.argsort(img_array)
    sorted_array = img_array[sorted_indices]

    encoded_sort_indices = encode_sort_indices(sorted_indices)
    
    return sorted_array, encoded_sort_indices

def decompress_image(sorted_array, encoded_sort_indices, original_shape):
    sorted_indices = decode_sort_indices(encoded_sort_indices, len(sorted_array))
    img_array = np.zeros_like(sorted_array)
    img_array[sorted_indices] = sorted_array

    img_array = img_array.reshape(original_shape)
    decompressed_image = Image.fromarray(img_array, mode="L")
    return decompressed_image

# Example usage
image_path = "path/image.png"
compressed_data = compress_image(image_path)
original_shape = Image.open(image_path).convert("L").size[::-1]  # height, width

# Save compressed image and encoded sort indices
compressed_image = Image.fromarray(compressed_data[0].reshape(original_shape).astype(np.uint8), mode="L")
compressed_image.save("path/compressed_image.png")
np.save("path/encoded_sort_indices.npy", compressed_data[1])

# Load compressed image and encoded sort indices
loaded_compressed_image = np.array(Image.open("path/compressed_image.png")).flatten()
loaded_encoded_sort_indices = np.load("path/encoded_sort_indices.npy")

# Decompress image
decompressed_img = decompress_image(loaded_compressed_image, loaded_encoded_sort_indices, original_shape)
decompressed_img.save("path/decompressed_image.png")
