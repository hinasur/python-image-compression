import numpy as np
from PIL import Image
from hilbertcurve.hilbertcurve import HilbertCurve

def map_image_to_hilbert_curve(img_array):
    side_len = img_array.shape[0]
    p = int(np.log2(side_len))
    hilbert_curve = HilbertCurve(p, 2)
    mapped_img_array = np.zeros_like(img_array)

    for i in range(side_len):
        for j in range(side_len):
            distance = hilbert_curve.distance_from_coordinates([i, j])
            mapped_img_array[i, j] = img_array[distance]

    return mapped_img_array

def map_image_from_hilbert_curve(mapped_img_array):
    side_len = mapped_img_array.shape[0]
    p = int(np.log2(side_len))
    hilbert_curve = HilbertCurve(p, 2)
    img_array = np.zeros_like(mapped_img_array)

    for i in range(side_len):
        for j in range(side_len):
            coords = hilbert_curve.coordinates_from_distance(i * side_len + j)
            img_array[i, j] = mapped_img_array[coords[0], coords[1]]

    return img_array

def compress_image(input_image_path, compressed_image_path):
    image = Image.open(input_image_path).convert('L')
    img_array = np.array(image)
    mapped_img_array = map_image_to_hilbert_curve(img_array)
    compressed_image = Image.fromarray(np.uint8(mapped_img_array))
    compressed_image.save(compressed_image_path, 'PNG')

def restore_image(compressed_image_path, output_image_path):
    compressed_image = Image.open(compressed_image_path).convert('L')
    mapped_img_array = np.array(compressed_image)
    img_array = map_image_from_hilbert_curve(mapped_img_array)
    restored_image = Image.fromarray(np.uint8(img_array))
    restored_image.save(output_image_path)

if __name__ == '__main__':
    input_image_path = 'input_image.png'
    compressed_image_path = 'compressed_image.png'
    output_image_path = 'restored_image.png'

    compress_image(input_image_path, compressed_image_path)
    restore_image(compressed_image_path, output_image_path)
