import cv2
import numpy as np
import math
import numpy as np



#========================TRI PAR TAS===========================
def heapify(arr, n, i):
    # Initialisation des indices
    largest = i
    left_child = 2 * i + 1
    right_child = 2 * i + 2

    # Parcours des nœuds du tas
    for _ in range(n):
        # Comparaison avec le nœud gauche
        if left_child < n and arr[left_child] > arr[largest]:
            largest = left_child

        # Comparaison avec le nœud droit
        if right_child < n and arr[right_child] > arr[largest]:
            largest = right_child

        # Échange si le plus grand n'est pas le nœud actuel
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]

            # Mettre à jour l'indice du nœud actuel
            i = largest

            # Mettre à jour les indices des nœuds enfants
            left_child = 2 * i + 1
            right_child = 2 * i + 2
        else:
            # Si le plus grand est déjà le nœud actuel, arrêter la boucle
            break


def heap_sort(arr):
    n = len(arr)

    # Construire un tas (heapify) en partant du dernier nœud non feuille
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    # Extraire les éléments un par un du tas
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)

#========================================================================

#================================FILTRES==================================
def mean_filter(img, kernel_size):
    # Obtention des dimensions de l'image
    rows, cols, channels = img.shape
    
    # Initialisation de l'image filtrée
    filtered_img = np.zeros(img.shape, img.dtype)

    # Calcul de la demi-taille du noyau
    half_kernel = kernel_size // 2

    # Parcours des pixels de l'image (en évitant les bords où le noyau ne rentre pas complètement)
    for i in range(half_kernel, rows - half_kernel):
        for j in range(half_kernel, cols - half_kernel):
            for k in range(channels):
                # Calcul de la moyenne dans la fenêtre du noyau
                mean_value = np.mean(img[i - half_kernel:i + half_kernel + 1, j - half_kernel:j + half_kernel + 1, k])

                # Mise à jour de la valeur du pixel avec la moyenne calculée
                filtered_img[i, j, k] = mean_value

    return filtered_img

def median_filter(img, kernel_size):
    # Obtention des dimensions de l'image
    rows, cols, channels = img.shape
    
    # Initialisation de l'image filtrée
    filtered_img = np.zeros(img.shape, img.dtype)

    # Calcul de la demi-taille du noyau
    half_kernel = kernel_size // 2

    # Parcours des pixels de l'image (en évitant les bords où le noyau ne rentre pas complètement)
    for i in range(half_kernel, rows - half_kernel):
        for j in range(half_kernel, cols - half_kernel):
            for k in range(channels):
                # Collecter les valeurs des pixels dans la fenêtre du noyau
                values = [img[i + m, j + n, k] for m in range(-half_kernel, half_kernel + 1) for n in range(-half_kernel, half_kernel + 1)]

                # Utiliser heap_sort pour obtenir la médiane
                heap_sort(values)
                median_index = len(values) // 2
                median_value = values[median_index]

                # Mise à jour de la valeur du pixel avec la médiane calculée
                filtered_img[i, j, k] = median_value

    return filtered_img


def gradient_filter(img, kernel_size):
    # Obtention des dimensions de l'image
    rows, cols, channels = img.shape
    # Initialisation de l'image filtrée
    gradient_img = np.zeros(img.shape, img.dtype)

    # Calcul de la demi-taille du noyau
    half_kernel = kernel_size // 2

    # Parcours des pixels de l'image (en évitant les bords où le noyau ne rentre pas complètement)
    for i in range(half_kernel, rows - half_kernel):
        for j in range(half_kernel, cols - half_kernel):
            for k in range(channels):
                # Collecter les valeurs des pixels dans la fenêtre du noyau
                values = [img[i + m, j + n, k] for m in range(-half_kernel, half_kernel + 1) for n in range(-half_kernel, half_kernel + 1)]

                # Calculer le gradient en utilisant les valeurs collectées
                gradient_value = max(values) - min(values)

                # Mettre à jour la valeur du pixel avec le gradient calculé
                gradient_img[i, j, k] = gradient_value

    return gradient_img

# Application de la formule de Gauss
def gaussian(x, y, sigma):
    return (1.0 / (2 * math.pi * sigma ** 2)) * math.exp(-(x ** 2 + y ** 2) / (2 * sigma ** 2))

def generate_gaussian_kernel(size, sigma):
    half_size = size // 2
    kernel = []

    for i in range(-half_size, half_size + 1):
        row = []
        for j in range(-half_size, half_size + 1):
            row.append(gaussian(i, j, sigma))
        kernel.append(row)

    # Normalize the kernel
    kernel_sum = sum(sum(row) for row in kernel)
    normalized_kernel = [[element / kernel_sum for element in row] for row in kernel]

    return normalized_kernel

def convolve(image, kernel):
    rows, cols, channels = image.shape
    filtered_img = np.zeros(image.shape, image.dtype)

    half_kernel = len(kernel) // 2

    for i in range(half_kernel, rows - half_kernel):
        for j in range(half_kernel, cols - half_kernel):
            for k in range(channels):
                # Calculate the weighted sum in the kernel window
                sum_pixels = 0
                for m in range(-half_kernel, half_kernel + 1):
                    for n in range(-half_kernel, half_kernel + 1):
                        sum_pixels += image[i + m, j + n, k] * kernel[m + half_kernel][n + half_kernel]

                # Update the pixel value with the weighted sum
                filtered_img[i, j, k] = int(sum_pixels)

    return filtered_img

def filtre_laplacien(image):
    # Définir le noyau du filtre laplacien
    kernel = [[0, 1, 0],
              [1, -4, 1],
              [0, 1, 0]]

    # Obtenir la taille de l'image
    rows, cols = len(image), len(image[0])

    # Initialiser une liste pour le résultat avec une boucle for et list comprehension
    resultat = [[0 for _ in range(cols)] for _ in range(rows)]

    # Appliquer la convolution manuellement avec des boucles for
    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            roi = [row[j-1:j+2] for row in image[i-1:i+2]]
            resultat[i][j] = sum(roi_val * kernel_val for roi_row, kernel_row in zip(roi, kernel) for roi_val, kernel_val in zip(roi_row, kernel_row))

    # Convertir le résultat en valeurs absolues et en entier 8 bits
    resultat_uint8 = np.array([[min(255, max(0, int(abs(val)))) for val in row] for row in resultat], dtype=np.uint8)

    return resultat_uint8

def erode(mask, kernel):
    # Obtention des dimensions du noyau et du masque
    ym, xm = kernel.shape
    yi, xi = mask.shape
    
    # Calcul de la moitié du noyau
    m = xm // 2
    
    # Copie du masque original pour éviter de modifier l'original
    mask2 = mask.copy()
    
    # Parcours de chaque pixel du masque
    for y in range(yi):
        for x in range(xi):
            # Si le pixel est blanc dans le masque original (255)
            if mask[y, x] == 255:
                # Vérifier si le pixel est sur le bord du masque, si oui, le mettre à 0 dans le masque résultant
                if y < m or y > (yi - 1 - m) or x < m or x > (xi - 1 - m):
                    mask2[y, x] = 0
                else:
                    # Extraire la région du masque correspondant à la taille du noyau
                    v = mask[y - m:y + m + 1, x - m:x + m + 1] 
                    
                    # Comparer chaque élément de la région avec le noyau
                    for h in range(0, ym):
                        for w in range(0, xm):
                            if v[h, w] < kernel[h, w]:
                                # Si une valeur est inférieure à celle du noyau, mettre à 0 dans le masque résultant
                                mask2[y, x] = 0
                                break
                        if mask2[y, x] == 0:
                            break
    return mask2


def dilation(mask, kernel):
    # Obtention des dimensions du noyau
    ym, xm = kernel.shape
    m = xm // 2
    
    # Initialisation du masque résultant
    mask2 = np.zeros(mask.shape, mask.dtype)
    
    # Parcours de chaque ligne du masque
    for y in range(mask.shape[0]):
        # Parcours de chaque colonne du masque
        for x in range(mask.shape[1]):
            # Vérifier si le pixel ne se trouve pas sur le bord du masque
            if not(y < m or y > (mask.shape[0] - 1 - m) or x < m or x > (mask.shape[1] - 1 - m)):
                # Extraire la région du masque correspondant à la taille du noyau
                v = mask[y - m:y + m + 1, x - m:x + m + 1]
                
                # Parcours de chaque élément de la région du masque
                for h in range(ym):
                    for w in range(xm):
                        # Si le produit du noyau et de la valeur du masque n'est pas égal à zéro
                        if not kernel[h, w] * v[h, w] == 0:
                            # Mettre à 255 dans le masque résultant
                            mask2[y, x] = 255
                            break
                    if mask2[y, x] == 255:
                        break

    return mask2

def seuillage_binaire(image_path, seuil):
    # Charger l'image en niveaux de gris
    image_gris = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    # Appliquer le seuillage binaire
    pixels_seuilles = (image_gris > seuil) * 255
    result_affichage = np.uint8(pixels_seuilles)

    return result_affichage  # Retourner result_affichage, pas pixels_seuilles

def closing(image, kernel):
    # Apply erosion first
    dilate_image = dilation(image, kernel)
    # Apply dilation on the eroded image
    closed_image = erode(dilate_image, kernel)
    return closed_image

def opening(image, kernel):
    # Apply dilation first
    erode_image = erode(image, kernel)
    # Apply erosion on the dilated image
    opened_image = dilation(erode_image, kernel)
    return opened_image

#============================================FILTRES PROPOSE======================================
def prewitt_filter(image, direction='horizontal'):
    # Define Prewitt filters
    if direction == 'horizontal':
        kernel = np.array([[-1, 0, 1],
                           [-1, 0, 1],
                           [-1, 0, 1]])
    elif direction == 'vertical':
        kernel = np.array([[-1, -1, -1],
                           [0, 0, 0],
                           [1, 1, 1]])
    else:
        raise ValueError("Invalid direction. Use 'horizontal' or 'vertical'.")

    # Get image dimensions
    rows, cols = image.shape

    # Initialize result image
    result = np.zeros(image.shape, dtype=np.float32)

    # Apply convolution with nested for loops
    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            # Apply convolution
            result[i, j] = np.sum(image[i-1:i+2, j-1:j+2] * kernel)

    # Ensure result is in the valid range [0, 255]
    result[result < 0] = 0
    result[result > 255] = 255

    # Convert to uint8 (8-bit image)
    result = np.uint8(result)

    return result

def sobel(image, kernel):
    # Taille de l'image et du noyau
    img_height, img_width = image.shape
    kernel_size = len(kernel)

    # Demi-taille du noyau pour le padding
    kernel_half = kernel_size // 2

    # Image résultante de la convolution
    result = np.zeros_like(image, dtype=np.float64)

    # Appliquer la convolution
    for y in range(kernel_half, img_height - kernel_half):
        for x in range(kernel_half, img_width - kernel_half):
            roi = image[y - kernel_half:y + kernel_half + 1, x - kernel_half:x + kernel_half + 1]
            result[y, x] = np.sum(roi * kernel)

    return result

#============================PARTIE GAME=====================================
lo = np.array([43,50,50]) # HSV (teinte, saturation, valeur)
hi = np.array([85,255,255])

def inRange(img, lo, hi):
    # Initialisation du masque
    mask = np.zeros((img.shape[0], img.shape[1]))

    # Parcours de chaque ligne de l'image
    for y in range(img.shape[0]):
        # Parcours de chaque colonne de l'image
        for x in range(img.shape[1]):
            # Vérification si la valeur du pixel est dans la plage spécifiée
            if (
                lo[0] <= img[y, x, 0] <= hi[0] and
                lo[1] <= img[y, x, 1] <= hi[1] and
                lo[2] <= img[y, x, 2] <= hi[2]
            ):
                # Mettre à 255 dans le masque si la condition est vraie
                mask[y, x] = 255

    return mask

def center(img):
    # Initialisation des indicateurs
    b = True
    c = True

    # Initialisation des coordonnées du rectangle englobant
    premiery = 0
    derniery = img.shape[0]
    premierx = 0
    dernierx = img.shape[1]

    # Recherche de la première ligne non nulle en partant du haut
    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            if b and img[y, x] == 255:
                b = False
                premiery = y
            if c and img[img.shape[0] - y - 1, x] == 255:
                c = False
                derniery = img.shape[0] - y - 1
            if not b and not c:
                break
        if not b and not c:
            break

    # Réinitialisation des indicateurs
    b = True
    c = True

    # Recherche de la première colonne non nulle en partant de la gauche
    for x in range(img.shape[1]):
        for y in range(img.shape[0]):
            if img[y, x] == 255 and b:
                b = False
                premierx = x
            if img[y, img.shape[1] - x - 1] == 255 and c:
                c = False
                dernierx = img.shape[1] - x - 1
            if not b and not c:
                break
        if not b and not c:
            break

    # Calcul du centre du rectangle englobant
    x = ((dernierx - premierx) / 2) + premierx
    y = ((derniery - premiery) / 2) + premiery

    return (int(x), int(y))

def detect_inrange(image):
    # Conversion de l'image en espace de couleur HSV
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Application de la fonction inRange pour créer un masque
    mask = inRange(image, lo, hi)

    # Application de l'érosion sur le masque avec un noyau 5x5
    mask = erode(mask, kernel=np.ones((5, 5)))

    return mask


def resize(img):
    # Initialisation d'une nouvelle image avec une taille réduite
    img2 = np.zeros(((int(img.shape[0] / 2.5)) + 1, (int(img.shape[1] // 2.5)) + 1, 3), img.dtype)
    
    # Parcours de chaque pixel de la nouvelle image
    for y in range(0, int(img.shape[0] / 2.5)):
        for x in range(0, int(img.shape[1] / 2.5)):
            # Copie de la valeur du pixel de l'image originale vers la nouvelle image
            img2[y, x, :] = img[int(y * 2.5), int(x * 2.5), :]

    return img2


def dilateV(frame, background, mask, kernel):
    # Obtention des dimensions du noyau
    ym, xm = kernel.shape
    m = xm // 2

    # Copie de l'image originale
    image = frame[:, :]

    # Parcours de chaque ligne du masque
    for y in range(mask.shape[0]):
        # Parcours de chaque colonne du masque
        for x in range(mask.shape[1]):
            # Si le pixel dans le masque est à 255, copier la valeur correspondante depuis l'arrière-plan
            if mask[y, x] == 255:
                image[y, x] = background[y, x]
            else:
                # Vérification si le pixel ne se trouve pas sur le bord du masque
                if not (y < m or y > (mask.shape[0] - 1 - m) or x < m or x > (mask.shape[1] - 1 - m)):
                    # Extraire la région du masque correspondant à la taille du noyau
                    v = mask[y - m:y + m + 1, x - m:x + m + 1]

                    # Parcours de chaque élément de la région du masque
                    for h in range(ym):
                        for w in range(xm):
                            # Si le produit du noyau et de la valeur du masque n'est pas égal à zéro
                            if not kernel[h, w] * v[h, w] == 0:
                                # Copier la valeur correspondante depuis l'arrière-plan
                                image[y, x] = background[y, x]
                                break
                        if not kernel[h, w] * v[h, w] == 0:
                            break
