import numpy as np
import matplotlib.pyplot as plt
from hilbertcurve.hilbertcurve import HilbertCurve

# Create a 50x50 matrix with random values
matrix = np.random.rand(50, 50)

# Define the Hilbert Curve
hilbert_curve = HilbertCurve(6, 2)

# Flatten the matrix and map the values to a Hilbert Curve index
flattened_matrix = matrix.flatten()
hilbert_indices = hilbert_curve.coordinates_to_distance(np.array([(i % 50, i // 50) for i in range(50*50)]))

# Sort the flattened matrix according to the Hilbert Curve indices
sorted_matrix = flattened_matrix[np.argsort(hilbert_indices)]

# Reshape the sorted matrix back to the original shape
sorted_matrix = sorted_matrix.reshape((50, 50))

# Visualize the original matrix and the sorted matrix
fig, axs = plt.subplots(1, 2, figsize=(10, 5))
axs[0].imshow(matrix, cmap='gray')
axs[0].set_title('Original matrix')
axs[1].imshow(sorted_matrix, cmap='gray')
axs[1].set_title('Sorted matrix')
plt.show()
