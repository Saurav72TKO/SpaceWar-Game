import pygame
import random
import math
from pygame import mixer

#initialize pygame
pygame.init()

#screen
WIDTH = 800
HEIGHT = 600


#create screen
screen = pygame.display.set_mode((WIDTH,HEIGHT))

# clock for FPS - THIS FIXES THE STUCK ISSUE
clock = pygame.time.Clock()



#title and icon
pygame.display.set_caption("Space-War")
icon = pygame.image.load("space.png")
pygame.display.set_icon(icon)

#BACKGROUND

background_img = pygame.image.load("space_bg_2.png")  
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))  # resize to screen

# Optional: makes it faster
background_img = background_img.convert()

#BG Music
mixer.music.load("GameMusic.mp3")
mixer.music.play(-1)



#player info

player_img = pygame.image.load("space-invaders-1.png")
player_x = random.randint(100,700)
player_y = 500
vel = 7
score = 0
font = pygame.font.Font("freesansbold.ttf",32)
text_x = 15

text_y = 15

#enemies info
enemy_img = []
enemy_x = []
enemy_y = []
enemy_xchange = []
enemy_ychange = []
num_of_enemies = 6
 
for i in range (num_of_enemies): 
    enemy_img.append(pygame.image.load(f"enemy-{i}.png"))
    enemy_x.append(random.randint(0,400)) 
    enemy_y.append(random.randint(0,60)) 
    enemy_xchange.append(2.5) 
    enemy_ychange.append(50) 

#bullet info
bullet_img = pygame.image.load("bullet.png")

bullet_x = player_x
bullet_y = player_y
bullet_change = 10


bullet_state = "ready"




#player function
def player (x,y):
    screen.blit(player_img, (x,y))
    
#enemy function
def enemy (x,y,i):
    screen.blit(enemy_img[i], (x,y))

#bullet function    
def fire_bullet (x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img,(x+16,y+10))

def is_collision (Ex,Ey,Bx,By):
    distance = math.sqrt((math.pow(Ex-Bx,2) + math.pow(Ey-By,2)))

    if distance < 35:
        return True
    else:
        return False

def score_show(x,y):
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (x, y))

                         
             
                         

running = True

#game loop
while running :
    
    #screen bg
    screen.fill((5, 5, 15))
    screen.blit(background_img, (0, 0))
    
    for event in pygame.event.get():  #all the events on the keyboard etc
        if event.type == pygame.QUIT: #check the close button
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("Shot_1.mp3")
                    bullet_sound.play()
                    bullet_x = player_x
                    print("Fire")
                    fire_bullet(bullet_x,bullet_y)
            
        
    keys = pygame.key.get_pressed() 
    
    if keys[pygame.K_LEFT]:
        player_x -= vel
    if keys[pygame.K_RIGHT]:
        player_x += vel
#     if keys[pygame.K_UP]:
#         player_y -= vel
#     if keys[pygame.K_DOWN]:
#         player_y += vel
    
    
     
    img_width = player_img.get_width()
    img_height = player_img.get_height()

    if player_x < 0:
        hit_sides = mixer.Sound("Warning.mp3")
        hit_sides.play()
        player_x = 0
    if player_x > WIDTH - img_width:
        hit_sides = mixer.Sound("Warning.mp3")
        hit_sides.play()
        player_x = WIDTH - img_width
        
    base_speed = 2.5 + score * 0.05 # 0.05 not 1, otherwise too fast

    for j in range(num_of_enemies):
        if enemy_xchange[j] > 0:
            enemy_xchange[j] = base_speed # was going right, keep right
        else:
            enemy_xchange[j] = -base_speed # was going left, keep left
    
    #enemy movement
    for i in range(num_of_enemies):
        #enemy player 
        enemy(enemy_x[i],enemy_y[i],i)
        
        enemy_x[i] += enemy_xchange[i] 
        
        #check collision   
        collision = is_collision(enemy_x[i],enemy_y[i],bullet_x,bullet_y)
        
        if enemy_x[i] < 0:
            enemy_x[i] = 0
            enemy_xchange[i] = -(enemy_xchange[i])
            enemy_y[i] += enemy_ychange[i]
            
        if enemy_x[i] > WIDTH - img_width:
            enemy_x[i] = WIDTH - img_width
            enemy_xchange[i] = -(enemy_xchange[i])
            enemy_y[i] += enemy_ychange[i]
        
        if collision:
            hit_sound = mixer.Sound("EnemyCrash.mp3")
            hit_sound.play()
            bullet_x = player_x + 16
            bullet_y = player_y + 10
            enemy_xchange[i] = 2.5
            score += 1
            
            enemy_x[i] = random.randint(0,400)
            enemy_y[i] = random.randint(0,60)
            bullet_state = "ready"
        
    
    if bullet_y <= 0 :
        bullet_state = "ready"
        bullet_w = bullet_img.get_width()
        player_w = player_img.get_width()
        bullet_x = player_x + (player_w // 2) - (bullet_w // 2)
        bullet_y = player_y
        bullet_x = player_x
        
    if bullet_state == "fire":
        fire_bullet(bullet_x,bullet_y)
        bullet_y -= bullet_change
    
    
      
    #calling player 
    player (player_x,player_y)
    score_show(text_x , text_y)
   
    pygame.display.update() #update the screen (must be added like the pygame.init())
    clock.tick(60)  # FIX: Limit to 60 FPS, stops 100% CPU usage
    
pygame.quit() 
   