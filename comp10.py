import numpy as np
from PIL import Image
import gzip
import io

def compress_image(image_path):
    image = Image.open(image_path).convert("L")
    img_array = np.array(image).flatten()

    sorted_indices = np.argsort(img_array)
    sorted_array = img_array[sorted_indices]

    return sorted_array, sorted_indices

def decompress_image(sorted_array, sorted_indices, original_shape):
    img_array = np.zeros_like(sorted_array)
    img_array[sorted_indices] = sorted_array

    img_array = img_array.reshape(original_shape)
    decompressed_image = Image.fromarray(img_array, mode="L")
    return decompressed_image

def lehmer_code_to_permutation(lehmer_code):
    lehmer_code = lehmer_code.copy()
    n = len(lehmer_code)
    remaining_elements = list(range(n))
    permutation = []
    
    for code in lehmer_code:
        permutation.append(remaining_elements.pop(code))
    
    return permutation

def permutation_to_lehmer_code(permutation):
    n = len(permutation)
    remaining_elements = list(range(n))
    lehmer_code = []
    
    for value in permutation:
        index = remaining_elements.index(value)
        lehmer_code.append(index)
        remaining_elements.pop(index)
    
    return lehmer_code

def encode_sort_indices(sort_indices):
    lehmer_code = permutation_to_lehmer_code(sort_indices)
    rank = sum(code * math.factorial(i) for i, code in enumerate(lehmer_code))
    return rank

def decode_sort_indices(rank, size):
    lehmer_code = []
    for i in range(size - 1, -1, -1):
        factorial = math.factorial(i)
        code = rank // factorial
        rank %= factorial
        lehmer_code.append(code)
    
    sort_indices = lehmer_code_to_permutation(list(reversed(lehmer_code)))
    return sort_indices


# Example usage
image_path = "path/image.png"
compressed_data = compress_image(image_path)
original_shape = Image.open(image_path).convert("L").size[::-1]  # height, width

# Save compressed image and encoded sort indices
compressed_image = Image.fromarray(compressed_data[0].reshape(original_shape).astype(np.uint8), mode="L")
compressed_image.save("path/compressed_image.png")

with gzip.open("path/sorted_indices.gz", "wb") as f:
    np.save(f, compressed_data[1])

# Load compressed image and encoded sort indices
loaded_compressed_image = np.array(Image.open("path/compressed_image.png")).flatten()

with gzip.open("path/sorted_indices.gz", "rb") as f:
    loaded_sorted_indices = np.load(f)

# Decompress image
decompressed_img = decompress_image(loaded_compressed_image, loaded_sorted_indices, original_shape)
decompressed_img.save("path/decompressed_image.png")
