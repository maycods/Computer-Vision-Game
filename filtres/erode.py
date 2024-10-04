import cv2
import numpy as np

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
image = cv2.imread('univer.jpg', cv2.IMREAD_GRAYSCALE)

# Définir un élément structurant (kernel) de test
kernel = np.array([[55, 55, 55],
                   [55, 55, 55],
                   [55, 55, 55]], dtype=np.uint8)

# Appliquer la fonction erode
result_erode = erode(image, kernel)


# Afficher les résultats
cv2.imshow('Image originale', image)
cv2.imshow('Résultat de erosion', result_erode)

cv2.waitKey(0)
cv2.destroyAllWindows()
