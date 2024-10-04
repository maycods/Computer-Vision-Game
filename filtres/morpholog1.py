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

image = cv2.imread('xfordNB.jpg', cv2.IMREAD_GRAYSCALE)

# Apply dilation function
dilated_image = dilation(image, dilation_kernel)

# Display the original and dilated images
#cv2.imshow('Original Image', image)
cv2.imshow('Dilated Image', dilated_image)






def erode(mask,kernel):
    y=0
    ym,xm=kernel.shape
    m=int((xm-1)/2)
    mask2=255*np.ones(mask.shape,mask.dtype)
    while y<mask.shape[0]:
        x=0
        while x<mask.shape[1]:
            
             if  not( y<m or y>(mask.shape[0]-1-m) or x<m or x>(mask.shape[1]-1-m)):
                v=mask[y-m:y+m+1,x-m:x+m+1] 
           
                h=0
                while(h<ym):
                     w=0
                     while(w<xm): 
                        if(v[h,w]<kernel[h,w]):
                             mask2[y,x]=0
                             break
                        w+=1
                     if(mask2[y,x]==0): 
                         break
                     h+=1
             x+=1
        y+=1

    return mask2



# Charger une image en niveaux de gris
image = cv2.imread('xford.jpg', cv2.IMREAD_GRAYSCALE)

# Définir un élément structurant (kernel) de test
kernel = np.array([[55, 55, 55],
                   [55, 55, 55],
                   [55, 55, 55]], dtype=np.uint8)

# Appliquer la fonction erode
result_erode = erode(image, kernel)

# Afficher les résultats
cv2.imshow('Image originale', image)
cv2.imshow('Resultat de erosion', result_erode)


cv2.waitKey(0)
cv2.destroyAllWindows()
