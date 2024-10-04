import cv2
import numpy as np
import Myfonctions

def sobel(image, kernel):
    # Taille de l'image et du noyau
    img_height, img_width = image.shape
    kernel_size = len(kernel)

    # Demi-taille du noyau pour le padding
    kernel_half = kernel_size // 2

    # Image résultante de la convolution
    result = np.zeros_like(image, dtype=np.float64)

    # Appliquer la convolution
    y = kernel_half
    while y < img_height - kernel_half:
        x = kernel_half
        while x < img_width - kernel_half:
            roi = image[y - kernel_half:y + kernel_half + 1, x - kernel_half:x + kernel_half + 1]
            result[y, x] = np.sum(roi * kernel)
            x += 1
        y += 1

    return result

# Charger l'image en niveaux de gris
image = cv2.imread("univerNB.jpg", cv2.IMREAD_GRAYSCALE)

# Définir le noyau Sobel pour la détection des contours horizontaux
sobel_x_kernel = [
    [-1, 0, 1],
    [-2, 0, 2],
    [-1, 0, 1]
]

# Définir le noyau Sobel pour la détection des contours verticaux
sobel_y_kernel = [
    [-1, -2, -1],
    [0, 0, 0],
    [1, 2, 1]
]

# Appliquer la convolution pour le filtre de Sobel en direction horizontale (sobel_x)
sobel_x = sobel(image, sobel_x_kernel)

# Appliquer la convolution pour le filtre de Sobel en direction verticale (sobel_y)
sobel_y = sobel(image, sobel_y_kernel)

# Calculer le gradient total
gradient_magnitude = np.sqrt(sobel_x**2 + sobel_y**2)  # magnitude du gradient

# Afficher l'image d'origine
cv2.imshow('Image Originale', image)

# Afficher le résultat du filtre de Sobel en direction horizontale (sobel_x)
cv2.imshow('Sobel X', (sobel_x))

# Afficher le résultat du filtre de Sobel en direction verticale (sobel_y)
cv2.imshow('Sobel Y', (sobel_y))

# Afficher le gradient total
cv2.imshow('Gradient total', gradient_magnitude)
cv2.waitKey(0)
cv2.destroyAllWindows()
