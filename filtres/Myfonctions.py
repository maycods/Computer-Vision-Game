import numpy as np


def my_sum(seq):
    total = 0

    # Convertir le générateur en liste
    seq_list = list(seq)

    # Utiliser la longueur de la liste
    length = len(seq_list)

    index = 0
    while index < length:
        total += seq_list[index]
        index += 1

    return total


def my_max(arg1, arg2):
    seq = [arg1, arg2]
    
    if not seq:
        # Gérer le cas où la séquence est vide
        raise ValueError("my_max() arg is an empty sequence")

    current_max = float('-inf')  # initialiser à l'infini négatif
    index = 0
    length = len(seq)

    while index < length:
        if seq[index] > current_max:
            current_max = seq[index]
        index += 1

    return current_max


def my_min(arg1, arg2):
    seq = [arg1, arg2]

    if not seq:
        # Gérer le cas où la séquence est vide
        raise ValueError("my_min() arg is an empty sequence")

    current_min = float('inf')  # initialiser à l'infini positif
    index = 0
    length = len(seq)

    while index < length:
        if seq[index] < current_min:
            current_min = seq[index]
        index += 1

    return current_min


def my_abs(num):
    if num < 0:
        return -num
    return num

def my_max2(seq):
    if not seq:
        # Gérer le cas où la séquence est vide
        raise ValueError("my_max() arg is an empty sequence")

    current_max = float('-inf')  # initialiser à l'infini négatif
    index = 0
    length = len(seq)

    while index < length:
        if seq[index] > current_max:
            current_max = seq[index]
        index += 1

    return current_max


def my_min2(seq):
    if not seq:
        # Gérer le cas où la séquence est vide
        raise ValueError("my_min() arg is an empty sequence")

    current_min = float('inf')  # initialiser à l'infini positif
    index = 0
    length = len(seq)

    while index < length:
        if seq[index] < current_min:
            current_min = seq[index]
        index += 1

    return current_min




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
                    min_val = my_max(min_val, pixel_value)

                    n += 1 

                m += 1 

            result[i, j] = min_val

            j += 1 

        i += 1  

    return result



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

