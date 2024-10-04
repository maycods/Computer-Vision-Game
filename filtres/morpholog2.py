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


image = cv2.imread('xfordNB.jpg', cv2.IMREAD_GRAYSCALE)
# Apply the closing operation
result_closing = closing(image, closing_kernel)

# Display the results
#cv2.imshow('Original Image', image)
cv2.imshow('Result of Closing', result_closing)




def opening(image, kernel):
    # Apply dilation first
    dilated_image = Myfonctions.dilation(image, kernel)
    # Apply erosion on the dilated image
    opened_image = Myfonctions.erode(dilated_image, kernel)
    return opened_image


# Define a kernel for closing
# Define a kernel for closing
opening_kernel = np.array([[190, 190, 190],
                           [190, 190, 190],
                           [190, 190, 190]], dtype=np.uint8)

image = cv2.imread('xford.jpg', cv2.IMREAD_GRAYSCALE)
# Apply the closing operation
result_opening = opening(image, opening_kernel)

# Display the results
cv2.imshow('Original Image', image)
cv2.imshow('Result of Opening', result_opening)



cv2.waitKey(0)
cv2.destroyAllWindows()