import numpy as np
from PIL import Image

def image_to_grayscale(image):
    # Convert the input image to grayscale
    return image.convert('L')

def sort_pixels_and_create_index_map(grayscale_image):
    img_array = np.array(grayscale_image)  # Convert the image to a numpy array
    sorted_img_array = np.sort(img_array, axis=None)  # Sort the pixel values in the array
    index_map = np.argsort(img_array, axis=None).argsort()  # Create an index map that records the sorted order
    # print(img_array)
    # print(sorted_img_array)
    print(index_map)
    return sorted_img_array.reshape(grayscale_image.size[::-1]), index_map.reshape(grayscale_image.size[::-1])

def unsort_pixels(sorted_image, index_map):
    unsorted_img_array = np.zeros_like(sorted_image)  # Create an empty array with the same shape as sorted_image
    flat_sorted_img = sorted_image.flatten()  # Flatten the sorted_image array

    # Loop through the flattened sorted_image array and assign each pixel value back to its original position using the index_map
    for i, pixel_value in enumerate(flat_sorted_img):
        unsorted_img_array.flat[index_map.flat[i]] = pixel_value

    return unsorted_img_array

def compress_image(input_image_path, sorted_image_path, index_map_path):
    image = Image.open(input_image_path)  # Load the input image
    grayscale_image = image_to_grayscale(image)  # Convert the image to grayscale
    sorted_image, index_map = sort_pixels_and_create_index_map(grayscale_image)  # Sort the pixels and create the index map

    sorted_image = Image.fromarray(sorted_image)  # Convert the sorted_image array back to an image
    sorted_image.save(sorted_image_path, 'PNG')  # Save the sorted_image as a PNG

    # Normalize the index_map to the range [0, 255] and convert it to a uint8 type
    index_map_image = Image.fromarray((index_map / np.max(index_map) * 255).astype(np.uint8))
    index_map_image.save(index_map_path, 'PNG')  # Save the index_map_image as a PNG

def restore_image(sorted_image_path, index_map_path, output_image_path):
    sorted_image = Image.open(sorted_image_path)  # Load the sorted_image
    index_map_image = Image.open(index_map_path)  # Load the index_map_image

    sorted_image = np.array(sorted_image)  # Convert the sorted_image to a numpy array
    index_map = np.array(index_map_image)  # Convert the index_map_image to a numpy array

    # print(sorted_image)
    # print(index_map)

    # Restore the original index_map from the normalized one
    index_map = (index_map * np.max(index_map) / 255).astype(np.int64)

    restored_image_array = unsort_pixels(sorted_image, index_map)  # Unsort the pixels using the index_map
    restored_image = Image.fromarray(restored_image_array)  # Convert the restored_image_array back to an image
    restored_image.save(output_image_path)  # Save the restored_image as a PNG

if __name__ == '__main__':
    input_image_path = 'input_image.png'  # Path to the input image
    sorted_image_path = 'sorted_image.png'  # Path to the sorted image
    index_map_path = 'index_map.png'  # Path to the index map image
    output_image_path = 'restored_image.png'  # Path to the output image

    compress_image(input_image_path, sorted_image_path, index_map_path)  # Compress the input image
    restore_image(sorted_image_path, index_map_path, output_image_path)  # Restore the image from the compressed data
