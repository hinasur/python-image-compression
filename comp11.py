from PIL import Image
import numpy as np
import math

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

# 元の画像をロード
image_path = "path/image.png"
image = Image.open(image_path)
original_data = np.array(image)

# 圧縮画像とソートインデックスを計算
compressed_data, sort_indices = compress_image(image_path)

# ソートインデックスを符号化
encoded_sort_indices = encode_sort_indices(sort_indices)

# 符号化されたソートインデックスをテキスト形式で保存
with open("path/encoded_sort_indices.txt", "w") as file:
    file.write(str(encoded_sort_indices))

# 圧縮画像をpng形式で保存
compressed_image = Image.fromarray(compressed_data.astype(np.uint8))
compressed_image.save("path/compressed_image.png")

# 圧縮画像をロード
compressed_image = Image.open("path/compressed_image.png")
compressed_data = np.array(compressed_image)

# 符号化されたソートインデックスをテキスト形式で読み込み
with open("path/encoded_sort_indices.txt", "r") as file:
    encoded_sort_indices = int(file.read().strip())

# ソートインデックスを復元
sort_indices = decode_sort_indices(encoded_sort_indices, len(original_data.flatten()))

# 元の画像を復元
restored_data = restore_image(compressed_data, sort_indices)

# 復元された画像を表示
restored_image = Image.fromarray(restored_data.astype(np.uint8))
restored_image.show()
