import os
import random
import pygame
import math

pygame.init()
screenWidth = 640
screenHeight = 480
screen = pygame.display.set_mode((screenWidth,screenHeight))
def setupSprites(mode):
    global firstBackground
    firstBackground = -1
    sprites = []
    folders = os.listdir("img")
    idx = 0
    for subFolder in folders:
        print(subFolder)
        folderSubFolders = os.listdir(f"img/{subFolder}")
        for file in folderSubFolders:
            print(f"\t{file}")
            if subFolder == "_backgrounds" and firstBackground == -1:
                firstBackground = idx
            sprite = pygame.image.load(f"img/{subFolder}/{file}").convert_alpha()
            if mode == "setup":
                if subFolder == "_backgrounds" or subFolder == "tiles":
                    sprite = pygame.transform.scale(sprite,
                                        (sprite.get_width() * 2,
                                        sprite.get_height() * 2))
            file = (f"{file}", sprite)
            sprites.append(file)
            idx += 1
        #print(f"{subFolder}: {os.listdir(f"img/{subFolder}")}")
    print(sprites)
    return sprites

def drawSprites(sprites, map, camX, camY, mapX, edit):
    global firstBackground
    if edit == "edit":
        bgX = math.fmod(camX,16)-16
        bgY = math.fmod(camY,16)-16
        idx = 1 + math.floor(camX/16)
        idx += mapX*math.floor(camY/16)
    else:
        bgX = math.fmod(camX,32)
        bgY = math.fmod(camY,32)
        idx = 1 + math.floor(camX/32)
        idx += mapX*math.floor(camY/32)
    if map[0] == "tiledBackground":
        screen.blit(sprites[firstBackground][1], (-bgX,-bgY))
    
    for y in range(16):
        for x in range(21):
            try:
                if map[idx] != -1:
                    if edit == "edit":
                        X = x*16-math.fmod(camX,16)+16
                        Y = y*16-math.fmod(camY,16)+16
                    else:
                        X = x*32-math.fmod(camX,32)
                        Y = y*32-math.fmod(camY,32)
                    screen.blit(sprites[map[idx][0]][1], (X,Y))
            except IndexError:
                pass
            idx += 1
        idx += mapX-21

        

sprites = setupSprites("setup")
for i in sprites:
    print(i[0])
    screen.blit(i[1])

tempMap = [(1, 0, 0), (2,0,32)]
print()
#drawSprites(sprites, tempMap, 0, 0,0,0)