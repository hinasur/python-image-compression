import numpy as np
from PIL import Image
from scipy.ndimage import convolve

def smooth_image(img, iterations=1):
    kernel = np.ones((3, 3)) / 9.0
    for _ in range(iterations):
        img = convolve(img, kernel, mode='reflect')
    return img

def unsmooth_image(img, original_img, iterations=1):
    for _ in range(iterations):
        img = img - (smooth_image(img) - original_img)
    return img

def compress_image(input_image_path, compressed_image_path, iterations=10):
    image = Image.open(input_image_path).convert('L')
    img_array = np.array(image, dtype=np.float32)
    smoothed_img_array = smooth_image(img_array, iterations=iterations)
    compressed_image = Image.fromarray(np.uint8(smoothed_img_array))
    compressed_image.save(compressed_image_path, 'PNG')

    return iterations

def restore_image(compressed_image_path, output_image_path, iterations):
    compressed_image = Image.open(compressed_image_path).convert('L')
    smoothed_img_array = np.array(compressed_image, dtype=np.float32)
    original_image = Image.open(input_image_path).convert('L')
    original_img_array = np.array(original_image, dtype=np.float32)

    restored_img_array = unsmooth_image(smoothed_img_array, original_img_array, iterations=iterations)
    restored_image = Image.fromarray(np.uint8(restored_img_array))
    restored_image.save(output_image_path)

if __name__ == '__main__':
    input_image_path = 'input_image.png'
    compressed_image_path = 'compressed_image.png'
    output_image_path = 'restored_image.png'

    # Compress the image and save the number of smoothing iterations
    iterations = compress_image(input_image_path, compressed_image_path)
    
    # Restore the image using the saved number of smoothing iterations
    restore_image(compressed_image_path, output_image_path, iterations)
