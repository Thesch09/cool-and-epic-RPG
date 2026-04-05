import random
import os
import pygame
from tiles import setupSprites, firstIMGs

setupSprites("setup")
print(firstIMGs[1])

def newMap(sizeX, sizeY, background, name):
    if sizeX < 20:
        sizeX = 20
    if sizeY < 15:
        sizeY = 15

    makingMap = [f"{sizeX},{sizeY}",f"{background}"]
    for i in range(sizeX):
        makingMap.append(f"0,{i*32},0")
    for i in range(sizeY-2):
        makingMap.append(f"0,0,{(i+1)*32}")
        for o in range(sizeX-2):
            if random.randint(1,10) == 1:
                makingMap.append(f"1,{(o+1)*32},{(i+1)*32}")
            else:
                makingMap.append(-1)
        makingMap.append(f"0,{sizeX*32-32},{(i+1)*32}")
    for i in range(sizeX):
        makingMap.append(f"0,{i*32},{sizeY*32-32}")
    
    with open(f"maps/{name}.txt", "w") as maps:
        for i in makingMap:
            maps.write(f"{i}\n")
            
    return makingMap

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
                    tempSTR = i.split()
                    loadingMap.append(int(tempSTR[0]))
                else:
                    tempSTR = i.strip().split(",")
                    tempSTR = (int(tempSTR[0]), int(tempSTR[1]), int(tempSTR[2]))
                    loadingMap.append(tempSTR)
                    #loadingMap.append(i.split())
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
    
def showResultsMap(results, sprites, screen, startX, startY):
    for map in results:
        print(map.split(".txt")[0])
        with open(f"maps/{map}") as mapFile:
            idx = 0
            for mapFileLine in mapFile:
                if idx == 1:
                    if mapFileLine == "tiledBackground\n":
                        screen.blit(sprites[firstIMGs[1]+1][1], (0,0))
                    print(mapFileLine)
                    break
                idx+=1


mapSearching("ner")
newMap(21,16, "tiledBackground", "newMap")
result = mapSearching("map")
if type(result) == str:
    print("egg")
else:
    pass
    #showResultsMap(result, 0,0)
loadMap("newMap")
#print(loadMap("newMap"))
'''
running = False
while running:
    screen.fill((0,0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
'''