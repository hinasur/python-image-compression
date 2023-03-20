import numpy as np
from PIL import Image

def image_to_grayscale(image):
    return image.convert('L')

def sort_pixels_and_create_index_map(grayscale_image):
    img_array = np.array(grayscale_image)
    index_map = np.argsort(img_array, axis=None)
    sorted_img_array = np.sort(img_array, axis=None)
    return sorted_img_array.reshape(grayscale_image.size[::-1]), index_map.reshape(grayscale_image.size[::-1])

def unsort_pixels(sorted_image, index_map):
    unsorted_img_array = np.zeros_like(sorted_image)
    flat_sorted_img = sorted_image.flatten()

    for i, pixel_value in enumerate(flat_sorted_img):
        unsorted_img_array.flat[index_map.flat[i]] = pixel_value

    return unsorted_img_array

def compress_image(input_image_path, sorted_image_path, index_map_path):
    image = Image.open(input_image_path)
    grayscale_image = image_to_grayscale(image)
    sorted_image, index_map = sort_pixels_and_create_index_map(grayscale_image)

    sorted_image = Image.fromarray(sorted_image)
    sorted_image.save(sorted_image_path, 'PNG')

    index_map_image = Image.fromarray((index_map / np.max(index_map) * 255).astype(np.uint8))
    index_map_image.save(index_map_path, 'PNG')

def restore_image(sorted_image_path, index_map_path, output_image_path):
    sorted_image = Image.open(sorted_image_path)
    index_map_image = Image.open(index_map_path)

    sorted_image = np.array(sorted_image)
    index_map = np.array(index_map_image) * (sorted_image.size // 255)

    restored_image_array = unsort_pixels(sorted_image, index_map)
    restored_image = Image.fromarray(restored_image_array)
    restored_image.save(output_image_path)

if __name__ == '__main__':
    input_image_path = 'input_image.png'
    sorted_image_path = 'sorted_image.png'
    index_map_path = 'index_map.png'
    output_image_path = 'restored_image.png'

    compress_image(input_image_path, sorted_image_path, index_map_path)
    restore_image(sorted_image_path, index_map_path, output_image_path)
