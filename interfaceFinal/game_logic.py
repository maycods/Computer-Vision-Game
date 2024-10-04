import cv2
import numpy as np
import random
import time


lo = np.array([43,50,50]) # HSV (teinte, saturation, valeur)
hi = np.array([85,255,255])#couleur choisis : vert

def erode(mask,kernel):
    ym,xm=kernel.shape
    yi,xi=mask.shape
    m=xm//2
    mask2=mask.copy()#pr optimiser de base mask2 est une copy de mask
    for y in range(yi):
        for x in range(xi):
            if mask[y,x]==255:# vu que c erode et que kernel 1 au milieu on change que si le pixel est blanc
                if  ( y<m or y>(yi-1-m) or x<m or x>(xi-1-m)):
                    mask2[y,x]=0# si il appartient au pixel de bords (considerant taille de kernel)on le rend noir
                else:
                    v=mask[y-m:y+m+1,x-m:x+m+1] 
                    for h in range(0,ym):
                        for w in range(0,xm): 
                            if(v[h,w]<kernel[h,w]):
                                mask2[y,x]=0 # erode fonctionne avec "et" donc il suffit d un 0 dans le voisinage la ou y a 1 dans le kernel pour qu il devienne noir
                                break
                        if(mask2[y,x]==0): #dans ce cas sortir des 2 boucles ameliorant ainsi la complexité
                            break
    return mask2

def inRange(img,lo,hi):
    mask=np.zeros((img.shape[0],img.shape[1]))
    for y in range(img.shape[0]):
         for x in range(img.shape[1]):
              if(img[y,x,0]<=hi[0] and img[y,x,0]>=lo[0] and img[y,x,2]<=hi[2] and img[y,x,2]>=lo[2] and img[y,x,1]<=hi[1] and img[y,x,1]>=lo[1] ):
                    mask[y,x]=255
    return mask
def center(img):
    b=True
    c=True
    dernierx=None
    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            if(b and img[y,x]==255):# on verifie si on a atteind permier pixel blanc de l axe y
                b=False
                premiery=y
            if( c and img[img.shape[0]-y-1,x]==255):# on verifie si on a atteind dernier pixel blanc de l axe y
                c=False
                derniery=img.shape[0]-y-1
            if(not b and not c):
                break
        if(not b and not c):
            break    
    b=True
    c=True
    for x in range(img.shape[1]):
        for y in range(img.shape[0]):#2 verification en paralelle pr ameliorer encore le temps d execution
            if(img[y,x]==255 and b):# on verifie si on a atteind permier pixel blanc de l axe x
                b=False
                premierx=x
            if(img[y,img.shape[1]-x-1]==255 and c):# on verifie si on a atteind dernier pixel blanc de l axe x
                c=False
                dernierx=img.shape[1]-x-1
            if(not b and not c):
                break
        if(not b and not c):
            break
    if dernierx==None:# le cas ou on a rien de vert dans le frame
        return None
    else:
        x=((dernierx-premierx)/2)+ premierx# milieu sur l axe x
        y=((derniery-premiery)/2)+ premiery#milieu sur l axe y
        return (int(x),int(y))

def detect_inrange(image):
    image = cv2.cvtColor(image,cv2.COLOR_BGR2HSV) #bgr to hsv
    mask = inRange(image,lo,hi)#binarisation selon intervale vert
    mask = erode(mask,kernel=np.ones((5,5)))#erosionavec kernel 5*5
    return mask
def resize(img):
     img2=np.zeros(((int(img.shape[0]/2.5))+1,(int(img.shape[1]//2.5))+1,3),img.dtype)
     for y in range(0,int(img.shape[0]/2.5)):
         for x in range(0,int(img.shape[1]/2.5)):
             img2[y,x,:]=img[int(y*2.5),int(x*2.5),:]#diminuer la taille de l image de x2.5
     return img2


class Player:
    def __init__(self, width, height):
        self.w = 40
        self.h = 40
        self.x = width // 2
        self.y = height - self.h
        self.player_character = cv2.imread("interfaceFinal\\game images\\chicken.png", cv2.IMREAD_UNCHANGED)  


    def move_left(self):
        self.x = max(0, self.x - 20)  # Ensure the player stays within the left border

    def move_right(self, width):
        self.x = min(width - self.w, self.x + 20)  # Ensure the player stays within the right border


    def display(self, img):
        player_character_rgb = self.player_character[:, :, :3]
        y_start = max(0, self.y)
        y_end = min(img.shape[0], self.y + self.h)
        x_start = max(0, self.x)
        x_end = min(img.shape[1], self.x + self.w)

        img[y_start:y_end, x_start:x_end, :] = player_character_rgb[:y_end - y_start, :x_end - x_start, :]

class Enemy:
    def __init__(self, width, speed):
        self.w = 40
        self.h = 40
        self.x = random.randint(28, width - 28)
        self.y = 0 - self.h
        self.speed = speed
        self.enemy_character = cv2.imread("interfaceFinal\\game images\\fox.png", cv2.IMREAD_UNCHANGED)

    def collision(self, obj):
        x_overlap = max(0, min(obj.x + obj.w, self.x + self.w) - max(obj.x, self.x))
        y_overlap = max(0, min(obj.y + obj.h, self.y + self.h) - max(obj.y, self.y))
        overlap_area = x_overlap * y_overlap
        return overlap_area > 0

    def out_of_bounds(self, height):
        if self.y > height:
            return True
        return False

    def display(self, img):
        self.y += self.speed  

        # Check if the updated position is still within the valid range of the image
        if 0 <= self.y < img.shape[0]:
            enemy_character_rgb = self.enemy_character[:, :, :3]
            y_start = max(0, self.y)
            y_end = min(img.shape[0], self.y + self.h)
            x_start = max(0, self.x)
            x_end = min(img.shape[1], self.x + self.w)

            img[y_start:y_end, x_start:x_end, :] = enemy_character_rgb[:y_end - y_start, :x_end - x_start, :]

class BorderEnemy:
    def __init__(self, x, speed):
        self.w = 28
        self.h = 28
        self.x = x
        self.y = random.randint(-height, 0)
        self.speed = speed
        self.border_enemy_character = cv2.imread("interfaceFinal\\game images\\tree.png", cv2.IMREAD_UNCHANGED)

    def collision(self, obj):
        x_overlap = max(0, min(obj.x + obj.w, self.x + self.w) - max(obj.x, self.x))
        y_overlap = max(0, min(obj.y + obj.h, self.y + self.h) - max(obj.y, self.y))
        overlap_area = x_overlap * y_overlap
        return overlap_area > 0

    def out_of_bounds(self, height):
        if self.y > height:
            return True
        return False

    def display(self, img):
        self.y += self.speed  

        # Check if the updated position is still within the valid range of the image
        if 0 <= self.y < img.shape[0]:
            border_enemy_character_rgb = self.border_enemy_character[:, :, :3]
            y_start = max(0, self.y)
            y_end = min(img.shape[0], self.y + self.h)
            x_start = max(0, self.x)
            x_end = min(img.shape[1], self.x + self.w)

            img[y_start:y_end, x_start:x_end, :] = border_enemy_character_rgb[:y_end - y_start, :x_end - x_start, :]   

class KalmanFilter(object):
    def __init__(self, dt, point):
        self.dt=dt

        # Vecteur d'etat initial
        self.E=np.matrix([[point[0]], [point[1]], [0], [0]])

        # Matrice de transition
        self.A=np.matrix([[1, 0, self.dt, 0],
                          [0, 1, 0, self.dt],
                          [0, 0, 1, 0],
                          [0, 0, 0, 1]])

        # Matrice d'observation, on observe que x et y
        self.H=np.matrix([[1, 0, 0, 0],
                          [0, 1, 0, 0]])

        self.Q=np.matrix([[1, 0, 0, 0],
                          [0, 1, 0, 0],
                          [0, 0, 1, 0],
                          [0, 0, 0, 1]])

        self.R=np.matrix([[1, 0],
                          [0, 1]])

        self.P=np.eye(self.A.shape[1])

    def predict(self):
        self.E=np.dot(self.A, self.E)
        # Calcul de la covariance de l'erreur
        self.P=np.dot(np.dot(self.A, self.P), self.A.T)+self.Q
        return self.E

    def update(self, z):
        # Calcul du gain de Kalman
        S=np.dot(self.H, np.dot(self.P, self.H.T))+self.R
        K=np.dot(np.dot(self.P, self.H.T), np.linalg.inv(S))

        # Correction / innovation
        self.E=np.round(self.E+np.dot(K, (z-np.dot(self.H, self.E))))
        I=np.eye(self.H.shape[1])
        self.P=(I-(K*self.H))*self.P

        return self.E

# Initialize game parameters
width, height = 257, 480
player = Player(290, height)
enemies = []
game_mode = False
score = 0

VideoCap = cv2.VideoCapture(0)
KF=KalmanFilter(0.1, [int(width/2),int(193)])
speed = 5

last_enemy_time = 0  # Variable to track the time when the last enemy was displayed
enemy_delay = 0.8

nbr_enemies = 30
vision = False
game_over = False
vv=False

while True:

    ret, frame = VideoCap.read()
    frame=resize(frame)
    cv2.flip(frame,1, frame)

    img = cv2.imread("interfaceFinal\\game images\\bg.png") 

    # Si le jeu est activé
    if game_mode:
        # A ffichage du score et de la vitesse en haut de l'interface
        cv2.putText(img, "Score: {}".format(score), (10, 20), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 2, 29), 1, cv2.LINE_AA)
        cv2.putText(img, "Speed: {}".format(speed), (10, 40), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 2, 29), 1, cv2.LINE_AA)
        # Génération aléatoire des ennemies (centre et bors)
        if random.randint(0, nbr_enemies) == 0 and time.time() - last_enemy_time > enemy_delay:
            border_enemy_left = BorderEnemy(0, speed)
            border_enemy_right = BorderEnemy(width - border_enemy_left.w, speed)
            enemies.append(Enemy(width - border_enemy_left.w - border_enemy_right.w, speed))
            enemies.append(border_enemy_left)
            enemies.append(border_enemy_right)
            last_enemy_time = time.time()  

        # Affichage des ennemies
        for enemy in enemies:
            enemy.display(img)

        # verifier les collision ou les ennemi qui sont hors bord verticalement 
        for enemy in enemies:
            if enemy.collision(player):
                enemies = []
                game_over = True
                game_mode = False
            elif enemy.out_of_bounds(height):
                enemies.remove(enemy)
                score += 1              # Augmenter le score de 1 pour chaque ennemi éliminé
                if score % 10 == 0:           # Augmentation de la vitesse et du nombre d'ennemies si le score dépasse un certain seuil 
                    speed += 1
                    if nbr_enemies > 5:
                        nbr_enemies -= 2
                    for enemy in enemies:
                        enemy.speed = speed

        player.display(img)

    # Si le jeu est désactive (game over ou bien on a pas encore commencer)
    else:
        
        if game_over:  
            cv2.putText(img, "GAME OVER !", (80, 240), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 2, 29), 1, cv2.LINE_AA)
        else:
            cv2.putText(img, "BRICK RACING GAME", (16, 180), cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 2, 29), 1, cv2.LINE_AA)
            cv2.putText(img, "Press <SPACE> to start", (50, 300), cv2.FONT_HERSHEY_DUPLEX, 0.4, (0, 2, 29), 1, cv2.LINE_AA)


    
    if vision:#mode ou la poule bouge horizontalement 
        mask = detect_inrange(frame)
        centre=center(mask)
        cv2.circle(frame, centre, 5, (0, 0, 255),-1)
        if centre is not None:#position poule mode 2
            player.x=centre[0]
        
    if vv:# mode ou la poule bouge verticalement et horizontalement avec prediction
        mask = detect_inrange(frame)
        centre=center(mask)

        etat=KF.predict().astype(np.int32)
        cv2.arrowedLine(frame,
                        (int(etat[0]), int(etat[1])), (int(etat[0]+etat[2]), 
                        int(etat[1]+etat[3])),
                        color=(0, 255, 0),
                        thickness=3,
                        tipLength=0.2)
        
        if (centre is not None):
            KF.update(np.expand_dims(np.array([centre[0],centre[1]]), axis=-1))
        else:
            centre=(int(etat[0]), int(etat[1]))#centre predit

        cv2.circle(frame, centre, 5, (0, 0, 255),-1)
        #position poule dans ce mode
        player.x=centre[0]
        player.y=height-40-int(((frame.shape[0]- centre[1])/frame.shape[0])*(height-40))

     #Concatenate jeu et camera verticall   
    concatenated_image = cv2.vconcat([img, frame])
    cv2.imshow('Game Interface', concatenated_image)

    key = cv2.waitKey(10)
    if key == ord('e'):
        break
    elif key == ord(' '):  # ESPACE pour débuter le jeu 
        # Re-Initialisation des parametres du jeu apres game over
        score = 0
        speed = 10
        game_mode = True
        nbr_enemies = 30
        vision=False
        vv=False
        player.x=int(width/2)
        player.y=height-40

    if key == ord('2'):#mode horizontale game
        vision=True
    elif key == ord('3'):#mode vertical+horizontal game
        vv=True
    else: 
        if key == ord('q'):#deplacer gauche
            player.move_left()
        elif key == ord('d'):#deplacer droite
            player.move_right(width)

cv2.destroyAllWindows()