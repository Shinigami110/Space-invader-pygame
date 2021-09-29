import pygame
import random 
import math
pygame.init()

# screen
screen = pygame.display.set_mode((1000,800))

# tilte and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)
 
# background
background = pygame.image.load("background.jpg")

# score
scoreCount = 0
font = pygame.font.Font("freesansbold.ttf",32)
scoreX = 10
scoreY = 10

def score(x,y):
    sc = font.render("Score : " + str(scoreCount), True, (255,255,255))
    screen.blit(sc,(x,y))

# player
playerImage = pygame.image.load("player.png")
playerX = 468
playerY = 720
playerDelta = 0
playerDeltaChange = 0.8

# enemy
enemyNumber = 5
enemyImage = []
enemyX = []
enemyY = []
enemyDelta = 0.25
enemyState = []

for i in range(enemyNumber):
    enemyImage.append(pygame.image.load("enemy.png"))
    enemyX.append(0)
    enemyY.append(-100)
    enemyState.append("Ready")

# bullet
bulletImage = pygame.image.load("bullet.png")
bulletX = -100
bulletY = -32
bulletDelta = 1
bulletState = "Ready"

def player(x,y):
    screen.blit(playerImage,(x,y))

def enemy(x,y,i):
    screen.blit(enemyImage[i],(x[i],y[i]))

def bullet(x,y):
    screen.blit(bulletImage,(x,y))

def shoot(x,y):
    global bulletState, bulletX, bulletY
    bulletState = "Going"
    bulletX = x + 16
    bulletY = y - 32

def isCollide_forBullet(eneX,eneY,bullX,bullY):
    if bullY + 32 < eneY or eneY + 64 < bullY :
        return False
    if bullX + 32 < eneX or eneX + 64 < bullX :
        return False
    return True 

def isCollide_forPlayer(eneX,eneY,playX,playY):
    if eneY + 64 < playY or playY + 64 < eneY:
        return False
    if eneX + 64 < playX or playX + 64 < eneX:
        return False
    return True

def resetBullet():
    global bulletX,bulletY,bulletState
    bulletX = -100
    bulletY = -32
    bulletState = "Ready"

# main loop
running = True
while running:
# background
    screen.fill((0,0,0))
    screen.blit(background,(0,0))
# quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
# player movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerDelta = - playerDeltaChange
            if event.key == pygame.K_RIGHT:
                playerDelta = playerDeltaChange
            
            if event.key == pygame.K_SPACE:
                if bulletState == "Ready":
                    shoot(playerX,playerY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT: 
                playerDelta = 0       

    playerX += playerDelta

# border
    if playerX < 0:
        playerX = 0
    if playerX > 936:
        playerX = 936

# enemy spawn
    if (random.randint(0,3000) == 1):
        for i in range(enemyNumber):
            if enemyState[i] == "Ready":
                enemyState[i] = "Going"
                enemyX[i] = random.randint(0,936)
                enemyY[i] = 0
                break
    
# bullet despawn
    if bulletY < 0 and bulletState == "Going":
        resetBullet()

# enemy movement 
    for i in range(enemyNumber):
        if enemyState[i] == "Going":
            enemyY[i] += enemyDelta
            
    for i in range(enemyNumber):
        if enemyY[i] > 800:
            enemyY[i] = -100
            enemyState[i] = "Ready"

# bullet movement
    if (bulletState == "Going"):
        bulletY -= bulletDelta

# enemy hit
    for i in range(enemyNumber):
        if isCollide_forBullet(enemyX[i],enemyY[i],bulletX,bulletY):
            enemyY[i] = -100
            enemyState[i] = "Ready"
            resetBullet()
            scoreCount += 1
             
# player hit
    for i in range(enemyNumber):
        if isCollide_forPlayer(enemyX[i],enemyY[i],playerX,playerY):
            playerX = -64
            playerY = -64

    for i in range(enemyNumber):
        enemy(enemyX,enemyY,i)    
    bullet(bulletX,bulletY)
    player(playerX,playerY)

    score(scoreX,scoreY)
    pygame.display.update()

