import numpy as np
from PIL import Image

def to_factoradic(num):
    factoradic = []
    i = 1
    while num > 0:
        num, remainder = divmod(num, i)
        factoradic.append(remainder)
        i += 1
    return factoradic[::-1]

def from_factoradic(factoradic):
    num = 0
    for i, coef in enumerate(factoradic[::-1]):
        num += coef * np.math.factorial(i)
    return num

def encode_sort_indices(arr):
    perm = np.argsort(arr)
    return from_factoradic(perm)

def decode_sort_indices(encoded, size):
    perm = to_factoradic(encoded)
    perm = [0] * (size - len(perm)) + perm
    arr = [0] * size
    elements = list(range(size))
    for i, p in enumerate(perm):
        arr[i] = elements.pop(p)
    return arr

def compress_image(image_path):
    image = Image.open(image_path)
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
    decompressed_image = Image.fromarray(img_array)
    return decompressed_image

# Example usage
image_path = "path/image.png"
compressed_data = compress_image(image_path)
original_shape = Image.open(image_path).size[::-1]  # height, width

# Save compressed image and encoded sort indices
compressed_image = Image.fromarray(compressed_data[0].reshape(original_shape).astype(np.uint8))
compressed_image.save("path/compressed_image.png")
with open("path/encoded_sort_indices.txt", "w") as f:
    f.write(str(compressed_data[1]))

# Load compressed image and encoded sort indices
loaded_compressed_image = np.array(Image.open("path/compressed_image.png")).flatten()
with open("path/encoded_sort_indices.txt", "r") as f:
    loaded_encoded_sort_indices = int(f.read())

# Decompress image
decompressed_img = decompress_image(loaded_compressed_image, loaded_encoded_sort_indices, original_shape)
decompressed_img.save("path/decompressed_image.png")
