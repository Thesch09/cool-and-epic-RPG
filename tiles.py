import os
import random
import pygame
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


def drawSprites(sprites, map, camX, camY):
    for i in map:
        #screen.blit(sprites[where in the map list[sprite ID]][the sprites list's sprite slot], (where in the map list[X position]-camX to account for the camera, where in the map[Y position]-camY to account for the camera))
        screen.blit(sprites[i[0]][1], (i[1]-camX,i[2]-camY))
        print(f"Drew {sprites[i[0]][0]} at {i[1]},{i[2]}")
        

sprites = setupSprites()
for i in sprites:
    print(i[0])
    screen.blit(i[1])

tempMap = [(1, 0, 0), (2,0,32)]
print()
drawSprites(sprites, tempMap, 0, 0)