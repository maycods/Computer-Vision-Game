import numpy as np
import cv2

def seuillage_binaire(image_path, seuil):
    # Charger l'image en niveaux de gris
    image_gris = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    # Appliquer le seuillage binaire
    pixels_seuilles = (image_gris > seuil) * 255
    result_affichage = np.uint8(pixels_seuilles)

    return result_affichage  # Retourner result_affichage, pas pixels_seuilles

# Spécifier le chemin de l'image et le seuil
image_path = 'univer.jpg'
seuil = 128

# Appliquer le filtre de seuillage binaire
result = seuillage_binaire(image_path, seuil)

# Afficher l'image originale et l'image seuillée
cv2.imshow('Image originale', cv2.imread(image_path, cv2.IMREAD_COLOR))
cv2.imshow('Image seuillee', result)
cv2.waitKey(0)
cv2.destroyAllWindows()
