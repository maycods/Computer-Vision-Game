import cv2
import numpy as np
import Myfonctions

def gradient_filter(img, kernel_size):
    rows, cols, channels = img.shape
    gradient_img = np.zeros(img.shape, img.dtype)

    half_kernel = kernel_size // 2

    i = half_kernel
    while i < rows - half_kernel:
        j = half_kernel
        while j < cols - half_kernel:
            k = 0
            while k < channels:
                # Collecter les valeurs des pixels dans la fenêtre du noyau
                values = []
                m = -half_kernel
                while m <= half_kernel:
                    n = -half_kernel
                    while n <= half_kernel:
                        values.append(img[i + m, j + n, k])
                        n += 1
                    m += 1

                # Calculer le gradient en utilisant les valeurs collectées
                gradient_value = Myfonctions.my_max2(values) - Myfonctions.my_min2(values)

                # Mettre à jour la valeur du pixel avec le gradient calculé
                gradient_img[i, j, k] = gradient_value
                k += 1

            j += 1

        i += 1

    return gradient_img

# Execution
# Lire l'image
image = cv2.imread('univer.jpg')

# Spécifier la taille du noyau
kernel_size = 3

# Appliquer le filtre de gradient
gradient_image = gradient_filter(image, kernel_size)

# Afficher l'image originale et l'image avec le filtre de gradient
cv2.imshow('Image Originale', image)
cv2.imshow('Image avec Filtre de Gradient', gradient_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
