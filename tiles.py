import os
import random
import pygame
import math

pygame.init()
screenWidth = 640
screenHeight = 480
screen = pygame.display.set_mode((screenWidth,screenHeight))

class sprite:
    def __init__(self, image, family): # Family is the subfolder
        self.sprite = pygame.image.load(f"img/{family}/{image}").convert_alpha()
        self.baseSize = (self.sprite.get_width(),self.sprite.get_height())
        self.family = family
    def resize(self, sizeModifier, sizeModifierY = None):
        if sizeModifier == "base":
            self.sprite = pygame.transform.scale(self.sprite,
                (self.baseSize[0],
                self.baseSize[1]))
            return
        if sizeModifierY == None:
            self.sprite = pygame.transform.scale(self.sprite,
                (self.sprite.get_width() * sizeModifier,
                self.sprite.get_height() * sizeModifier))
        else:
            self.sprite = pygame.transform.scale(self.sprite,
                (self.sprite.get_width() * sizeModifier,
                self.sprite.get_height() * sizeModifierY))

def setupSprites():
    global sprite
    sprites = {}
    folders = os.listdir("img")
    for subFolder in folders:
        folderSubFolders = os.listdir(f"img/{subFolder}")
        for file in folderSubFolders:
            sprites.update({f"{file.split(".png")[0]}":sprite(f"{file}", f"{subFolder}")})
    return sprites

def resizeSprites(sprites, scale):
    for thing in sprites:
        if sprites[thing].family == "tiles" or sprites[thing].family == "_backgrounds":
            print(thing, scale)
            sprites[thing].resize(scale)

def drawSprites(sprites, map, camX, camY, mapX, edit):
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
    screen.blit(sprites[map[0]].sprite, (-bgX,-bgY))
    
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
                    screen.blit(sprites[map[idx]].sprite, (X,Y))
            except IndexError:
                pass
            idx += 1
        idx += mapX-21

        

sprites = setupSprites()
for i in sprites:
    print(i)
    print(sprites[i])
    screen.blit(sprites[i].sprite)