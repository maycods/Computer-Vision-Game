import cv2
import numpy as np

def prewitt_filter(image, direction='horizontal'):
    # Define Prewitt filters
    if direction == 'horizontal':
        kernel = np.array([[-1, 0, 1],
                           [-1, 0, 1],
                           [-1, 0, 1]])
    elif direction == 'vertical':
        kernel = np.array([[-1, -1, -1],
                           [0, 0, 0],
                           [1, 1, 1]])
    else:
        raise ValueError("Invalid direction. Use 'horizontal' or 'vertical'.")

    # Get image dimensions
    rows, cols = image.shape

    # Initialize result image
    result = np.zeros(image.shape, dtype=np.float32)

    # Initialize loop variables
    i = 1
    while i < rows - 1:
        j = 1
        while j < cols - 1:
            # Apply convolution
            result[i, j] = np.sum(image[i-1:i+2, j-1:j+2] * kernel)

            # Increment column index
            j += 1

        # Increment row index
        i += 1

    # Ensure result is in the valid range [0, 255]
    result[result < 0] = 0
    result[result > 255] = 255


    # Convert to uint8 (8-bit image)
    result = np.uint8(result)
    # result = result % 256

    return result

# Example
image = cv2.imread('univer.jpg', cv2.IMREAD_GRAYSCALE)

# Apply Prewitt filter for horizontal edge detection
prewitt_horizontal = prewitt_filter(image, direction='horizontal')

# Apply Prewitt filter for vertical edge detection
prewitt_vertical = prewitt_filter(image, direction='vertical')

# Display the original, horizontal, and vertical edge-detected images
cv2.imshow('Original Image', image)
cv2.imshow('Prewitt Horizontal Edge', prewitt_horizontal)
cv2.imshow('Prewitt Vertical Edge', prewitt_vertical)

cv2.waitKey(0)
cv2.destroyAllWindows()
