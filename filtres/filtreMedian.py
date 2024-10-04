import cv2
import numpy as np

#========================TRI===========================
def heapify(arr, n, i):
    largest = i
    left_child = 2 * i + 1
    right_child = 2 * i + 2

    while left_child < n or right_child < n:
        if left_child < n and arr[left_child] > arr[largest]:
            largest = left_child

        if right_child < n and arr[right_child] > arr[largest]:
            largest = right_child

        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            i = largest
            left_child = 2 * i + 1
            right_child = 2 * i + 2
        else:
            break

def heap_sort(arr):
    n = len(arr)

    # Construire un tas (heapify) en partant du dernier nœud non feuille
    i = n // 2 - 1
    while i >= 0:
        heapify(arr, n, i)
        i -= 1

    # Extraire les éléments un par un du tas
    i = n - 1
    while i > 0:
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)
        i -= 1

#===============================================================
def median_filter(img, kernel_size):
    rows, cols, channels = img.shape
    filtered_img = np.zeros(img.shape, img.dtype)

    half_kernel = kernel_size // 2

    i = half_kernel
    while i < rows - half_kernel:
        j = half_kernel
        while j < cols - half_kernel:
            k = 0
            while k < channels:   # traiter le cas des image GRAYSCALE ou COLOR
                # Collecter les valeurs des pixels dans la fenêtre du noyau
                values = []
                m = -half_kernel
                while m <= half_kernel:
                    n = -half_kernel
                    while n <= half_kernel:
                        values.append(img[i + m, j + n, k])
                        n += 1
                    m += 1

                # Calculer la médiane des valeurs collectées
                heap_sort(values)
                median_value = values[len(values) // 2]

                # Mettre à jour la valeur du pixel avec la médiane calculée
                filtered_img[i, j, k] = median_value
                k += 1

            j += 1

        i += 1

    return filtered_img

# Execution
# lire l'image 
image = cv2.imread('noisy.jpg')

# Spécifier la taille du noyau
kernel_size = 5

# Appliquer le filtre médian
filtered_image = median_filter(image, kernel_size)

# Afficher l'image originale et l'image filtrée
cv2.imshow('Image Originale', image)
cv2.imshow('Image Filtree (Median)', filtered_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
