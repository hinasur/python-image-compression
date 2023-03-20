import numpy as np
from PIL import Image
import math

def compress_image(image_data):
    flattened_data = image_data.flatten()
    sort_indices = np.argsort(flattened_data)
    print("flatten")
    print(flattened_data)
    print("img")
    print(image_data)
    compressed_data = flattened_data[sort_indices]
    return compressed_data.reshape(image_data.shape), sort_indices

def restore_image(compressed_data, sort_indices):
    flattened_data = compressed_data.flatten()
    restored_data = np.zeros_like(flattened_data)
    restored_data[sort_indices] = flattened_data
    return restored_data.reshape(compressed_data.shape)

def encode_sort_indices(sort_indices):
    n = len(sort_indices)
    print("n=")
    print(n)
    print(sort_indices)
    encoded = 0
    for i in range(n):
        coef = sort_indices[i]
        for j in range(i):
            if sort_indices[j] < sort_indices[i]:
                coef -= 1
        encoded += coef * math.factorial(n - i - 1)
    return encoded

def decode_sort_indices(encoded, n):
    remaining_values = list(range(n))
    sort_indices = []
    for i in range(n - 1, -1, -1):
        f = math.factorial(i)
        idx = encoded // f
        sort_indices.append(remaining_values[idx])
        remaining_values.pop(idx)
        encoded %= f
    return np.array(sort_indices)

# 元の画像をロード
image_path = "path2/image.png"
image = Image.open(image_path)
original_data = np.array(image)

# 圧縮画像とソートインデックスを計算
compressed_data, sort_indices = compress_image(original_data)

# 圧縮画像をpng形式で保存
compressed_image = Image.fromarray(compressed_data.astype(np.uint8))
compressed_image.save("path2/compressed_image.png")

# ソートインデックスを符号化
encoded_sort_indices = encode_sort_indices(sort_indices)

print ("ここは？")

# 符号化されたソートインデックスをテキスト形式で保存
with open("path2/encoded_sort_indices.txt", "w") as file:
    file.write(str(encoded_sort_indices))

# 圧縮画像をロード
compressed_image = Image.open("path2/compressed_image.png")
compressed_data = np.array(compressed_image)

print ("ここは？ロード")

# 符号化されたソートインデックスをテキスト形式で読み込み
with open("path2/encoded_sort_indices.txt", "r") as file:
    encoded_sort_indices = int(file.read().strip())

print ("ここは？ソートインデックスロード")

# ソートインデックスを復元
sort_indices = decode_sort_indices(encoded_sort_indices, len(original_data.flatten()))

print ("ここは？復元")

# 元の画像を復元
restored_data = restore_image(compressed_data, sort_indices)

# 復元された画像を表示
restored_image = Image.fromarray(restored_data.astype(np.uint8))
restored_image.save("path2/restored_image.png")
# restored_image.show()
