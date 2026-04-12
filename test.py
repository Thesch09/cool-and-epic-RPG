import math
import pygame
pygame.init()
screenWidth = 640
screenHeight = 480
screen = pygame.display.set_mode((screenWidth,screenHeight))
'''
x = 0
for i in range(64):
    print(math.modf(i/32))
    x+=1

for i in range(64):
    tempVar = math.modf(x/32)
    print(tempVar[1])
    x+=1
'''
x = 0
for i in range(96):
    tempVar = math.fmod(i, 32)
    print(tempVar)

dictTest = {"value":0, "val2":"egg"}
for i in dictTest:
    print(i)
    print(dictTest[i])

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
            
egg = sprite("dirtV3.png","tiles")
print(egg.baseSize)
egg.resize(2)
print(egg.sprite.get_width(), egg.sprite.get_height())
egg.resize("base")
print(egg.sprite.get_width(), egg.sprite.get_height())

dicty = {"dirtV3":sprite("dirtV3.png","tiles"),
         "dirtBackground":sprite("dirtBackground.png", "tiles")}
for i in dicty:
    print(dicty[i].baseSize)