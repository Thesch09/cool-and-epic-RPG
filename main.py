import pygame
import math

pygame.init()
screen = pygame.display.set_mode((640,480))
running = True
clock = pygame.time.Clock()
deltaTime = 0.1

tileList = []
class tiles:
    def __init__(self, name, image):
        self.name = name
        self.sprite = pygame.image.load(image).convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite,
                                (self.sprite.get_width() * 2,
                                self.sprite.get_height() * 2))
        tileList.append(self)

dirt = tiles("dirt", "img/dirtV3.png")
dirt2 = tiles("dirt2", "img/dirtBackground.png")

playerX = 0
playerY = 0
playerSpeed = 48
keyRightDirection = False
keyLeftDirection = False
keyUpDirection = False
keyDownDirection = False
keySprint = False

def playerMovement():
    global playerX
    global playerY
    joyX = 0
    joyY = 0
    joyDist = 0
    if keyRightDirection:
        joyX = 1
    if keyLeftDirection:
        joyX = -1
    if keyUpDirection:
        joyY = 1
    if keyDownDirection:
        joyY = -1

    joyDist = math.sqrt(joyX*joyX+joyY*joyY)

    if joyDist > 0:

        joyX = joyX/joyDist
        joyY = joyY/joyDist

        if keySprint:
            playerX += (playerSpeed+24) * deltaTime * joyX
            playerY += (playerSpeed+24) * deltaTime * joyY
        else:
            playerX += playerSpeed * deltaTime * joyX
            playerY += playerSpeed * deltaTime * joyY
        print(joyDist)

while running:
    screen.fill((0,0,0))
    playerMovement()
    camX = playerX
    camY = playerY

    screen.blit(dirt.sprite, (32-camX,camY))
    screen.blit(dirt2.sprite, (64-camX,32+camY))

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