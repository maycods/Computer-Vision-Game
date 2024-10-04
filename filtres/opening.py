import numpy as np
import cv2
import Myfonctions

def opening(image, kernel):
    # Apply dilation first
    dilated_image = Myfonctions.dilation(image, kernel)
    # Apply erosion on the dilated image
    opened_image = Myfonctions.erode(dilated_image, kernel)
    return opened_image


# Define a kernel for closing
closing_kernel = np.array([[15, 15, 15],
                           [15, 15, 15],
                           [15, 15, 15]], dtype=np.uint8)


image = cv2.imread('univerNB.jpg', cv2.IMREAD_GRAYSCALE)
# Apply the closing operation
result_closing = opening(image, closing_kernel)

# Display the results
cv2.imshow('Original Image', image)
cv2.imshow('Result of Opening', result_closing)

cv2.waitKey(0)
cv2.destroyAllWindows()