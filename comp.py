import numpy as np
from PIL import Image

def run_length_encoding(arr):
    values = []
    counts = []
    prev = arr[0]
    count = 1
    for elem in arr[1:]:
        if elem == prev:
            count += 1
        else:
            values.append(prev)
            counts.append(count)
            prev = elem
            count = 1
    values.append(prev)
    counts.append(count)
    return values, counts

def run_length_decoding(values, counts):
    arr = []
    for value, count in zip(values, counts):
        arr.extend([value] * count)
    return arr

def compress_image(image_path):
    image = Image.open(image_path)
    img_array = np.array(image).flatten()

    sorted_indices = np.argsort(img_array)
    sorted_array = img_array[sorted_indices]

    sorted_indices_values, sorted_indices_counts = run_length_encoding(sorted_indices)
    
    return sorted_array, sorted_indices_values, sorted_indices_counts

def decompress_image(sorted_array, sorted_indices_values, sorted_indices_counts, original_shape):
    sorted_indices = np.array(run_length_decoding(sorted_indices_values, sorted_indices_counts))
    img_array = np.zeros_like(sorted_array)
    img_array[sorted_indices] = sorted_array

    img_array = img_array.reshape(original_shape)
    decompressed_image = Image.fromarray(img_array)
    return decompressed_image

# Example usage
image_path = "input_image.png"
compressed_data = compress_image(image_path)
original_shape = Image.open(image_path).size[::-1]  # height, width
decompressed_img = decompress_image(*compressed_data, original_shape)
decompressed_img.save("restored_image.png")
