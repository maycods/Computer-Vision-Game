import numpy as np
import cv2
import Myfonctions

def closing(image, kernel):
    # Apply erosion first
    eroded_image = Myfonctions.erode(image, kernel)
    # Apply dilation on the eroded image
    closed_image = Myfonctions.dilation(eroded_image, kernel)
    return closed_image


# Define a kernel for closing
closing_kernel = np.array([[55, 55, 55],
                           [55, 55, 55],
                           [55, 55, 55]], dtype=np.uint8)


image = cv2.imread('univerNB.jpg', cv2.IMREAD_GRAYSCALE)
# Apply the closing operation
result_closing = closing(image, closing_kernel)

# Display the results
cv2.imshow('Original Image', image)
cv2.imshow('Result of Closing', result_closing)

cv2.waitKey(0)
cv2.destroyAllWindows()