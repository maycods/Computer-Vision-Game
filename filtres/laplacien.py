import cv2
import numpy as np
import Myfonctions

def filtre_laplacien(image):
    # Définir le noyau du filtre laplacien
    kernel = [[0, 1, 0],
              [1, -4, 1],
              [0, 1, 0]]

    # Obtenir la taille de l'image
    rows, cols = len(image), len(image[0])

    # Initialiser une liste pour le résultat avec une boucle while
    resultat = []
    i = 0
    while i < rows:
        j = 0
        row = []
        while j < cols:
            row.append(0)
            j += 1
        resultat.append(row)
        i += 1


    # Appliquer la convolution manuellement avec une boucle while
    i = 1
    while i < rows - 1:
        j = 1
        while j < cols - 1:
            roi = [row[j-1:j+2] for row in image[i-1:i+2]]
            resultat[i][j] = Myfonctions.my_sum(roi_val * kernel_val for roi_row, kernel_row in zip(roi, kernel) for roi_val, kernel_val in zip(roi_row, kernel_row))
            j += 1
        i += 1

    # Convertir le résultat en valeurs absolues et en entier 8 bits
    resultat_uint8 = [[Myfonctions.my_min(255, Myfonctions.my_max(0, int(Myfonctions.my_abs(val)))) for val in row] for row in resultat]

    return np.array(resultat_uint8, dtype=np.uint8)

# Exemple d'utilisation
image = cv2.imread("univer.jpg", cv2.IMREAD_GRAYSCALE).tolist()
resultat = filtre_laplacien(image)

# Afficher l'image originale et l'image après le filtre laplacien
cv2.imshow("Image originale", cv2.imread("univer.jpg", cv2.IMREAD_COLOR))
cv2.imshow("Filtre Laplacien Manuel", resultat)
cv2.waitKey(0)
cv2.destroyAllWindows()
