import cv2
import numpy as np
import Myfonctions

def dilation(image, kernel):
    rows, cols = image.shape
    result = np.zeros(image.shape, image.dtype)


    k_rows = len(kernel)
    k_cols = len(kernel[0])


    i = 1
    while i < rows - 1:
        j = 1
        while j < cols - 1:
            # Initial value is set to 255 (white)
            min_val = 0

            m = 0
            while m < k_rows:
                n = 0
                while n < k_cols:
                    # Multiply corresponding pixel value with the kernel value
                    pixel_value = image[i - 1 + m, j - 1 + n] * kernel[m][n]
                    # Find the minimum value
                    min_val = Myfonctions.my_max(min_val, pixel_value)

                    n += 1 

                m += 1 

            result[i, j] = min_val

            j += 1 

        i += 1  

    return result



# Example 

# Define a kernel for dilation
dilation_kernel = [
    [1, 0, 1],
    [0, 1, 0],
    [1, 0, 1]
]

image = cv2.imread('univerNB.jpg', cv2.IMREAD_GRAYSCALE)

# Apply dilation function
dilated_image = dilation(image, dilation_kernel)

# Display the original and dilated images
cv2.imshow('Original Image', image)
cv2.imshow('Dilated Image', dilated_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
