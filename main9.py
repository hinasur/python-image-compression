import numpy as np
from PIL import Image

def image_to_grayscale(image):
    return image.convert('L')

def sort_pixels_and_create_index_map(grayscale_image):
    img_array = np.array(grayscale_image)
    sorted_img_array = np.sort(img_array, axis=None)
    index_map = np.argsort(img_array, axis=None)
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

    np.savetxt(index_map_path, index_map, fmt='%d', delimiter=',')  # Save the index_map as a text file

def restore_image(sorted_image_path, index_map_path, output_image_path):
    sorted_image = Image.open(sorted_image_path)
    index_map = np.loadtxt(index_map_path, dtype=np.int64, delimiter=',')  # Load the index_map from the text file

    sorted_image = np.array(sorted_image)

    restored_image_array = unsort_pixels(sorted_image, index_map)
    restored_image = Image.fromarray(restored_image_array)
    restored_image.save(output_image_path)

if __name__ == '__main__':
    input_image_path = 'input_image.png'
    sorted_image_path = 'sorted_image.png'
    index_map_path = 'index_map.txt'
    output_image_path = 'restored_image.png'

    compress_image(input_image_path, sorted_image_path, index_map_path)
    restore_image(sorted_image_path, index_map_path, output_image_path)
