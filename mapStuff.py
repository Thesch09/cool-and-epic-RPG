import random
import os
import pygame
from tiles import setupSprites, firstIMGs

setupSprites("setup")
print(firstIMGs[1])

def writeFile(text,file): #write to a file
    text = text+"\n"
    file.write(text)

def newMap(sizeX, sizeY, name, background = "tiledBackground"):
    if sizeX < 20:
        sizeX = 20
    if sizeY < 15:
        sizeY = 15
    
    with open(f"maps/{name}.txt","w") as maps:
        writeFile(f"{sizeX},{sizeY}", maps)
        writeFile(f"{background}",maps)
        for i in range(sizeX):
            writeFile("dirtBackground",maps)
        for i in range(sizeY-2):
            writeFile("dirtBackground",maps)
            for o in range(sizeX-2):
                if random.randint(1,10) == 1:
                    writeFile("dirtV3",maps)
                else:
                    maps.write("-1\n")
            writeFile("dirtBackground",maps)
        for i in range(sizeX):
            writeFile("dirtBackground",maps)
    return

def loadMap(selectMap):
    loadingMap = []
    try:
        with open(f"maps/{selectMap}.txt") as maps:
            idx = 0
            for i in maps:
                if idx == 0:
                    position = i.split(",")
                    sizeX = int(position[0])
                    sizeY = int(position[1])
                elif idx == 1:
                    loadingMap.append(i.split()[0])
                elif i == "-1\n":
                    loadingMap.append(-1)
                else:
                    tempSTR = i.strip()
                    loadingMap.append(tempSTR)
                idx += 1
        print(type(loadingMap))
        return loadingMap,sizeX, sizeY
    except FileNotFoundError:
        print(f"File {selectMap} does not exist in this folder!")

def mapSearching(input):
    searchResults = []
    for map in os.listdir(f"maps"):
        if input.lower() in map.lower().split(".txt")[0]:
            searchResults.append(map)
    if searchResults == []:
        return "No maps found..."
    else:
        return searchResults
    
def showResultsMap(results, sprites, screen, startY, font):
    entry = 0
    hitboxes = {}
    for map in results:
        hitbox = pygame.rect.Rect(378, startY+13*entry-2, 196, 13)
        pygame.draw.rect(screen, (220,220,220), hitbox)
        hitboxes.update({map:hitbox})
        with open(f"maps/{map}") as mapFile:
            idx = 0
            for mapFileLine in mapFile:
                if idx == 0:
                    lineSplit = mapFileLine.split(",")
                    sizeX = lineSplit[0]
                    sizeY = lineSplit[1].split()[0]
                    text = font.render(f"{sizeX}x{sizeY}", False, (0,0,0))
                    screen.blit(text,(574-text.get_width(),startY+12*entry))
                elif idx == 1:
                    if mapFileLine == "tiledBackground\n":
                        screen.blit(sprites["mapIconTiled"], (382,startY+12*entry))
                else:
                    break
                idx += 1
            text = font.render(f"{map.split(".txt")[0]}", False, (0,0,0))
            screen.blit(text, (392,startY+12*entry))
        entry += 1
    return hitboxes

def checkForDifferencesMap(updatedMap, mapAsFile, sizeX, sizeY):
    with open(f"maps/{mapAsFile}.txt") as map:
        idx = 0
        mapList = [f"{sizeX},{sizeY}"]
        for index in updatedMap:
            mapList.append(index)
        print(mapList)
        #print(updatedMap)
        print(len(mapList))
        for line in map:
            try:
                if str(mapList[idx]) != line.split()[0]:  
                    print("different")
                    return True
                idx += 1
            except IndexError:
                print("nothing different")
                return False

mapSearching("ner")
result = mapSearching("map")
if type(result) == str:
    print("egg")
else:
    pass
loadMap("newMap")
'''
running = False
while running:
    screen.fill((0,0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
'''