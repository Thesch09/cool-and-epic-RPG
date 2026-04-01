import random
import os

def newMap(sizeX, sizeY, background):
    makingMap = [f"{sizeX},{sizeY}",f"{background}"]
    for i in range(sizeX):
        makingMap.append(f"1,{i*32},0")
    for i in range(sizeY-2):
        makingMap.append(f"1,0,{(i+1)*32}")
        for o in range(sizeX-2):
            if random.randint(1,10) == 1:
                makingMap.append(f"2,{(o+1)*32},{(i+1)*32}")
            else:
                makingMap.append(-1)
        makingMap.append(f"1,{sizeX*32-32},{(i+1)*32}")
    for i in range(sizeX):
        makingMap.append(f"1,{i*32},{sizeY*32-32}")
    
    with open("maps/newMap.txt", "w") as maps:
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
        return loadingMap,sizeX, sizeY
    except FileNotFoundError:
        print(f"File {selectMap} does not exist in this folder!")


newMap(21,16, "tiledBackground")
print(loadMap("newMap"))