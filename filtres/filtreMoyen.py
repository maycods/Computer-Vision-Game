import cv2
import numpy as np
 
def mean_filter(img, kernel_size):
    rows, cols, channels = img.shape
    filtered_img = np.zeros(img.shape, img.dtype)

    half_kernel = kernel_size // 2

    i = half_kernel
    while i < rows - half_kernel:
        j = half_kernel
        while j < cols - half_kernel:
            k = 0
            while k < channels: # traiter le cas des image GRAYSCALE ou COLOR
                # Calculer la moyenne dans la fenêtre du noyau
                sum_pixels = 0
                m = -half_kernel
                while m <= half_kernel:
                    n = -half_kernel
                    while n <= half_kernel:
                        sum_pixels += img[i + m, j + n, k]
                        n += 1
                    m += 1

                # Mettre à jour la valeur du pixel avec la moyenne calculée
                filtered_img[i, j, k] = sum_pixels // (kernel_size ** 2)
                k += 1

            j += 1

        i += 1

    return filtered_img


# Execution
# lire l'image
image = cv2.imread('noisy.jpg')

# Spécifier la taille du noyau
kernel_size = 5

# Appliquer le filtre moyen
filtered_image = mean_filter(image, kernel_size)

# Afficher l'image originale et l'image filtrée
cv2.imshow('Image Originale', image)
cv2.imshow('Image Filtree (Moyen)', filtered_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
