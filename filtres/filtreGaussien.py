import cv2
import math
import numpy as np
import Myfonctions

def gaussian(x, y, sigma):
    return (1.0 / (2 * math.pi * sigma ** 2)) * math.exp(-(x ** 2 + y ** 2) / (2 * sigma ** 2))

def generate_gaussian_kernel(size, sigma):
    half_size = size // 2
    kernel = []

    i = -half_size
    while i <= half_size:
        row = []
        j = -half_size
        while j <= half_size:
            row.append(gaussian(i, j, sigma))
            j += 1
        kernel.append(row)
        i += 1

    # Normalize the kernel
    kernel_sum = Myfonctions.my_sum(Myfonctions.my_sum(row) for row in kernel)
    normalized_kernel = [[element / kernel_sum for element in row] for row in kernel]

    return normalized_kernel

def convolve(image, kernel):
    rows, cols, channels = image.shape
    filtered_img = np.zeros(image.shape, image.dtype)

    half_kernel = len(kernel) // 2

    i = half_kernel
    while i < rows - half_kernel:
        j = half_kernel
        while j < cols - half_kernel:
            k = 0
            while k < channels:
                # Calculate the weighted sum in the kernel window
                sum_pixels = 0
                m = -half_kernel
                while m <= half_kernel:
                    n = -half_kernel
                    while n <= half_kernel:
                        sum_pixels += image[i + m, j + n, k] * kernel[m + half_kernel][n + half_kernel]
                        n += 1
                    m += 1

                # Update the pixel value with the weighted sum
                filtered_img[i, j, k] = int(sum_pixels)
                k += 1

            j += 1

        i += 1

    return filtered_img

# Execution
# Read the image
image = cv2.imread('noisy.jpg')

# Specify the kernel size and sigma
kernel_size = 5
sigma = 1.0

# Generate the Gaussian kernel
gaussian_kernel_2d = generate_gaussian_kernel(kernel_size, sigma)

# Apply the Gaussian filter
filtered_image = convolve(image, gaussian_kernel_2d)

# Display the original and filtered images
cv2.imshow('Image Originale', image)
cv2.imshow('Image Filtree (Gaussien)', filtered_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
