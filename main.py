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
writing = "false"

tileList = setupSprites("setup")

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
currentMap, sizeX, sizeY = loadMap("newMap")
print(type(currentMap))

def playerMovement(menuType):
    global playerX, playerY, sizeX, sizeY

    if menuType == "edit":
        menuType = 2
    else:
        menuType = 1

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
            playerX += (playerSpeed*2) * deltaTime * joyX * menuType
            playerY += (playerSpeed*2) * deltaTime * joyY * menuType
        else:
            playerX += playerSpeed * deltaTime * joyX * menuType
            playerY += playerSpeed * deltaTime * joyY * menuType
        
        if menuType == 2:
            if playerX > sizeX*16:
                playerX = sizeX*16
            if playerY > sizeY*16:
                playerY = sizeY*16
            if playerX < 16:
                playerX = 16
            if playerY < 16:
                playerY = 16
        else:
            if playerX > sizeX*32-32:
                playerX = sizeX*32-32
            if playerY > sizeY*32-32:
                playerY = sizeY*32-32
            if playerX < 0:
                playerX = 0
            if playerY < 0:
                playerY = 0
        #print(joyDist)
def camera(X, Y):
    global camX, camY, bgX, bgY, sizeX, sizeY, menuType
    if menuType == "edit":
        camX = X-160
        camY = Y-120
    else:
        camX = X-320
        camY = Y-240
    if camX < 0:
        camX = 0
    if camY < 0:
        camY = 0
    if menuType == "edit":
        if camX > sizeX*16-320:
            camX = sizeX*16-320
        if camY > sizeY*16-240:
            camY = sizeY*16-240
    else:
        if camX > sizeX*32-640:
            camX = sizeX*32-640
        if camY > sizeY*32-480:
            camY = sizeY*32-480


while running:
    screen.fill((0,0,0))
    if menuType == "overworld" or menuType == "edit":
        playerMovement(menuType)
        camera(playerX,playerY)

    if menuType == "edit":
        playerHitbox = pygame.Rect(playerX-camX, playerY-camY, 16,16)
    else:
        playerHitbox = pygame.Rect(playerX-camX, playerY-camY, 32,32)

    drawSprites(tileList, currentMap, camX, camY, sizeX, menuType)
    pygame.draw.rect(screen, (255, 0, 255), playerHitbox)
    if menuType == "edit":
        screen.blit(tileList[3][1], (0,0))

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
            if event.key == pygame.K_BACKSLASH:
                if menuType == "overworld":
                    tileList = setupSprites("edit")
                    menuType = "edit"
                    playerX = playerX / 2
                    playerY = playerY / 2
                    print("edit")
                elif menuType == "edit":
                    tileList = setupSprites("setup")
                    menuType = "overworld"
                    playerX = playerX * 2
                    playerY = playerY * 2
                    print("not edit")
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