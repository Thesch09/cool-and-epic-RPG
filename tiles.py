import os
import random
import pygame
import math

pygame.init()
screenWidth = 640
screenHeight = 480
screen = pygame.display.set_mode((screenWidth,screenHeight))
def setupSprites():
    sprites = []
    folders = os.listdir("img")
    for subFolder in folders:
        print(subFolder)
        folderSubFolders = os.listdir(f"img/{subFolder}")
        for file in folderSubFolders:
            print(f"\t{file}")
            sprite = pygame.image.load(f"img/{subFolder}/{file}").convert_alpha()
            if subFolder == "backgrounds" or subFolder == "tiles":
                sprite = pygame.transform.scale(sprite,
                                    (sprite.get_width() * 2,
                                    sprite.get_height() * 2))
            file = (f"{file}", sprite)
            sprites.append(file)
        #print(f"{subFolder}: {os.listdir(f"img/{subFolder}")}")
    print(sprites)
    return sprites


def drawSprites(sprites, map, camX, camY, mapX, mapY):
    bgX = math.fmod(camX,32)
    bgY = math.fmod(camY,32)
    if map[0] == "tiledBackground":
        screen.blit(sprites[0][1], (-bgX,-bgY))
    
    idx = 1 + math.floor(camX/32)
    idx += mapX*math.floor(camY/32)
    for y in range(16):
        for x in range(21):
            if map[idx] != -1:
                X = x*32-math.fmod(camX,32)
                Y = y*32-math.fmod(camY,32)
                screen.blit(sprites[map[idx][0]][1], (X,Y))
            idx += 1
        idx += mapX-21

        

sprites = setupSprites()
for i in sprites:
    print(i[0])
    screen.blit(i[1])

tempMap = [(1, 0, 0), (2,0,32)]
print()
#drawSprites(sprites, tempMap, 0, 0,0,0)