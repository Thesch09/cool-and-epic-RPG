import pygame
import math
from tiles import setupSprites, drawSprites, resizeSprites
from mapStuff import newMap, loadMap, mapSearching, showResultsMap, checkForDifferencesMap

pygame.init()
screenWidth = 640
screenHeight = 480
flags = pygame.SCALED | pygame.RESIZABLE
screen = pygame.display.set_mode((screenWidth,screenHeight),flags)
running = True
clock = pygame.time.Clock()
deltaTime = 0.1
# Fonts
smallFont = pygame.font.Font("fonts/Game Font Small.ttf", 8)
normalFont = pygame.font.Font("fonts/Game Font Normal.ttf", 8)
fontNormalColour = (0,0,0)

menuType = "overworld"
writing = False
mapName = "newMap"

tileList = setupSprites()
resizeSprites(tileList, 2)

playerX = 320
playerY = 240
playerSpeed = 48

def resetButtons():
    global keyDownDirection,keyLeftDirection,keyRightDirection,keySprint,keyUpDirection,ctrlDown, LMBpressed, RMBpressed, MMBpressed
    keyRightDirection = False
    keyLeftDirection = False
    keyUpDirection = False
    keyDownDirection = False
    keySprint = False
    ctrlDown = False
    LMBpressed = False
    RMBpressed = False
    MMBpressed = False
resetButtons()
clickCooldown = 0
mapSearchText = smallFont.render("This is a temp text. Let's", False, (120,120,120))
noMapSearchResults = smallFont.render("", False, fontNormalColour)
result = ""
mapSearch = ""
dialogue = normalFont.render("This is a temp Text. Let's", False, (120, 120,255))
mapDifferenceExists = True

camX = 0
camY = 0
bgX = 0
bgY = 0
#currentMap = newMap(21,16, "tiledBackground")
currentMap, sizeX, sizeY = loadMap(mapName)
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
        if playerX > sizeX*16-16:
            playerX = sizeX*16-16
        if playerY > sizeY*16-16:
            playerY = sizeY*16-16
        if playerX < 0:
            playerX = 0
        if playerY < 0:
            playerY = 0
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



editSearchBox1 = pygame.Rect(376,48,200,100)
editSearchBox2 = pygame.Rect(378,50,196,14)
mapDifferencePopupSize = 100
mapDifferencePopup = pygame.Rect(screenWidth/2-mapDifferencePopupSize,screenHeight/2-mapDifferencePopupSize,mapDifferencePopupSize*2,mapDifferencePopupSize-25)
mapDifferencePopupInside = pygame.Rect(screenWidth/2-(mapDifferencePopupSize-2),screenHeight/2-mapDifferencePopupSize+2,mapDifferencePopupSize*2-4,mapDifferencePopupSize-29)
mapDifferenceSave = pygame.Rect(screenWidth/2-mapDifferencePopupSize*1.3,screenHeight/2-25, 50,50)
while running:
    mousePos = pygame.mouse.get_pos()
    mouseHitbox = pygame.rect.Rect(mousePos[0]-2, mousePos[1]-2, 8,8)

    screen.fill((0,0,0))
    if menuType == "overworld" or menuType == "edit":
        playerMovement(menuType)
        camera(playerX,playerY)
    if menuType == "edit":
        playerHitbox = pygame.Rect(playerX-camX+16, playerY-camY+16, 16,16)       
    else:
        playerHitbox = pygame.Rect(playerX-camX, playerY-camY, 32,32)

    drawSprites(tileList, currentMap, camX, camY, sizeX, menuType)
    pygame.draw.rect(screen, (255, 0, 255), playerHitbox)
    
    if menuType == "edit":
        screen.blit(tileList["editMode"].sprite, (0,0))
        pygame.draw.rect(screen, (217,201,163), editSearchBox1)
        pygame.draw.rect(screen, (220,220,220), editSearchBox2)
        #pygame.draw.rect(screen, (220,220,220), editSearchBox3)
        if mapSearch == "":
            mapSearchText = smallFont.render(f"Search", False, (120,120,120))
        else:
            mapSearchText = smallFont.render(f"{mapSearch}", False, fontNormalColour)
        if type(result) != str: # I want the maps to always show, as long as the query matched a map name.
            searchResultHitboxes = showResultsMap(result, tileList,screen, 70, smallFont)
            idx = 0
            for i in searchResultHitboxes:
                mouseCollidesWithMaps = searchResultHitboxes[i].colliderect(mouseHitbox)
                if mouseCollidesWithMaps:
                    if LMBpressed and clickCooldown <= 0:
                        clickCooldown = 0.5
                        if not checkForDifferencesMap(currentMap,mapName, sizeX, sizeY):
                            mapName = i.split(".txt")[0]
                            currentMap, sizeX, sizeY = loadMap(mapName)
                            print(mapName)
                            print(f"loaded {i}")
                            #mapDifferenceExists = False
                        else:
                            mapDifferenceExists = True
                    break
                idx += 1
        screen.blit(mapSearchText, (382,52))
        screen.blit(noMapSearchResults, (382,70))
        #screen.blit(dialogue,(0,32))
        pygame.draw.rect(screen, (0,0,0), mouseHitbox)

        if mapDifferenceExists:
            mapNotSavedText = smallFont.render(f"Map '{mapName}' has not been saved!", False, (0,0,0))
            pygame.draw.rect(screen,(217,201,163), mapDifferencePopup)
            pygame.draw.rect(screen,(255,255,255), mapDifferencePopupInside)
            pygame.draw.rect(screen,(0,255,0), mapDifferenceSave)
            screen.blit(mapNotSavedText, (screenWidth/2-mapNotSavedText.get_width()/2,screenHeight/2-95))

        clickCooldown -= 1*deltaTime

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and menuType == "edit":
            if editSearchBox2.collidepoint(event.pos):
                writing = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            #print(pygame.mouse.get_pressed(num_buttons=5))
            if event.button == 1:
                LMBpressed = True
            if event.button == 3:
                RMBpressed = True
        if event.type == pygame.MOUSEBUTTONUP:
            #print(pygame.mouse.get_pressed(num_buttons=5))
            if event.button == 1:
                LMBpressed = False
            if event.button == 3:
                RMBpressed = False

        if event.type == pygame.KEYDOWN:
            if not writing:
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
                        tileList = setupSprites()
                        resizeSprites(tileList,"base")
                        menuType = "edit"
                        playerX = playerX / 2
                        playerY = playerY / 2
                        result = mapSearching("")
                        print("edit")
                    elif menuType == "edit":
                        tileList = setupSprites()
                        resizeSprites(tileList, 2)
                        menuType = "overworld"
                        playerX = playerX * 2
                        playerY = playerY * 2
                        print("not edit")
            elif writing:
                if event.key == pygame.K_ESCAPE:
                    writing = False
                elif event.key == pygame.K_BACKSPACE:
                    if ctrlDown:
                        mapSearch = ""
                    else:
                        mapSearch = mapSearch[:-1]
                elif event.key == pygame.K_LCTRL:
                    ctrlDown = True
                else:
                    mapSearch += event.unicode

                if writing: # To make it so that the map search code doesn't run always, it is in here. It checks if writing is still true so that it doesn't run if the player stopped searching (by pressing escape)
                    result = mapSearching(mapSearch)
                    if type(result) == str:
                        noMapSearchResults = smallFont.render("No results...", False, fontNormalColour)
                    else:
                        noMapSearchResults = smallFont.render("", False, fontNormalColour)
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
            if event.key == pygame.K_LCTRL:
                ctrlDown = False


    pygame.display.flip()

    deltaTime = clock.tick(60) / 1000
    deltaTime = max(0.001, min(0.1, deltaTime))

pygame.quit()