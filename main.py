import pygame
import math
from tiles import setupSprites, drawSprites
from mapStuff import newMap, loadMap

pygame.init()
screenWidth = 640
screenHeight = 480
flags = pygame.SCALED | pygame.RESIZABLE
screen = pygame.display.set_mode((screenWidth,screenHeight),flags)
running = True
clock = pygame.time.Clock()
deltaTime = 0.1
menuType = "overworld"

tileList = setupSprites()

playerX = 320
playerY = 240
playerSpeed = 48
keyRightDirection = False
keyLeftDirection = False
keyUpDirection = False
keyDownDirection = False
keySprint = False

camX = 0
camY = 0
bgX = 0
bgY = 0
#currentMap = newMap(21,16, "tiledBackground")
newMap(20,15, "tiledBackground", "smallMap")
newMap(100,100,"tiledBackground", "hugeMap")
currentMap, sizeX, sizeY = loadMap("hugeMap")
print(type(currentMap))

def playerMovement():
    global playerX, playerY, sizeX, sizeY
    joyX = 0
    joyY = 0
    joyDist = 0
    if keyRightDirection:
        joyX = 1
    if keyLeftDirection:
        joyX = -1
    if keyUpDirection:
        joyY = -1
    if keyDownDirection:
        joyY = 1

    joyDist = math.sqrt(joyX*joyX+joyY*joyY)

    if joyDist > 0:

        joyX = joyX/joyDist
        joyY = joyY/joyDist

        if keySprint:
            playerX += (playerSpeed*2) * deltaTime * joyX
            playerY += (playerSpeed*2) * deltaTime * joyY
        else:
            playerX += playerSpeed * deltaTime * joyX
            playerY += playerSpeed * deltaTime * joyY
        if playerX < 0:
            playerX = 0
        if playerY < 0:
            playerY = 0
        if playerX > sizeX*32-32:
            playerX = sizeX*32-32
        if playerY > sizeY*32-32:
            playerY = sizeY*32-32
        #print(joyDist)
def camera(X, Y):
    global camX, camY, bgX, bgY, sizeX, sizeY
    camX = X-320
    camY = Y-240
    if camX < 0:
        camX = 0
    if camY < 0:
        camY = 0
    if camX > sizeX*32-640:
        camX = sizeX*32-640
    if camY > sizeY*32-480:
        camY = sizeY*32-480


while running:
    screen.fill((0,0,0))
    if menuType == "overworld":
        playerMovement()
        camera(playerX,playerY)

    playerHitbox = pygame.Rect(playerX-camX, playerY-camY, 32,32)

    drawSprites(tileList, currentMap, camX, camY, sizeX, sizeY)
    pygame.draw.rect(screen, (255, 0, 255), playerHitbox)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                keyRightDirection = True
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                keyLeftDirection = True
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                keyUpDirection = True
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                keyDownDirection = True
            if event.key == pygame.K_LSHIFT:
                keySprint = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                keyRightDirection = False
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                keyLeftDirection = False
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                keyUpDirection = False
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                keyDownDirection = False
            if event.key == pygame.K_LSHIFT:
                keySprint = False


    pygame.display.flip()

    deltaTime = clock.tick(60) / 1000
    deltaTime = max(0.001, min(0.1, deltaTime))

pygame.quit()