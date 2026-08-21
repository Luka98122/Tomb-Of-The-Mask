import pygame
import json

cx = 0
cy = 0
koja = "1"+".json"
BS = 14

MW,MH = 60,60
zoom = 1


f = open("maps/1.json")
grid = json.loads(f.read())
f.close()


#grid = []
#for i in range(MW):
#    l = []
#    for j in range(MH):
#        l.append(-1)
#    grid.append(l)
MW,MH = len(grid),len(grid[0])
window = pygame.display.set_mode(((MW/zoom+10)*BS,(MH/zoom+10)*BS))

mode = 0

#Purple = #CC01DE
#Black = #000000
#PLAYER = #FDF500
#COIN = #F1BF23

wall = pygame.Color(204,1,222)
coin = pygame.Color(241,191,35)


wallRect = pygame.Rect(BS*MW,0,BS*10,BS*MH/5)
starRect = pygame.Rect(BS*MW,MW/5*BS,BS*10,BS*MH/5)
coinRect = pygame.Rect(BS*MW,MW/5*2*BS,BS*10,BS*MH/5)
startRect = pygame.Rect(BS*MW,MW/5*3*BS,BS*10,BS*MH/5)
endRect = pygame.Rect(BS*MW,MW/5*4*BS,BS*10,BS*MH/5)

directionRect = pygame.Rect(0,BS*MH,BS*MW,BS*MW)
clock = pygame.time.Clock()

wallImg = pygame.image.load("cont/wall1.png")
squareImg = pygame.image.load("cont/square.png")
squareImg = pygame.transform.scale(squareImg,(BS,BS))
wallImg = pygame.transform.scale(wallImg,(BS,BS))

deathWallImg = pygame.image.load("cont/deathwall.png")
deathWallImg = pygame.transform.scale(deathWallImg,(BS*0.5,BS))
trapwallImg = pygame.image.load("cont/trapwall.png")
trapwallImg = pygame.transform.scale(trapwallImg,(BS,BS))


h_deathWallImg = pygame.transform.rotate(deathWallImg,90)

wallImg = pygame.transform.scale(wallImg,(BS,BS))

w_up = pygame.transform.rotate(wallImg,180)
w_down = wallImg
w_left = pygame.transform.rotate(wallImg,270)
w_right = pygame.transform.rotate(wallImg,90)

walls = [w_up,w_right,w_down,w_left,squareImg,deathWallImg,h_deathWallImg,trapwallImg]

while True:
    window.fill("black")
    events = pygame.event.get()
    for event in events:
        if event.type==pygame.QUIT:
            f = open("maps/"+koja,"w")
            f.write(json.dumps(grid))
            f.close()
            exit()
            
    mouseState = pygame.mouse.get_pressed()        
    
            
    keys = pygame.key.get_pressed()
    mx,my = pygame.mouse.get_pos()
    if (mx//BS<=MW) and my//BS<=MH:
        pygame.draw.rect(window,pygame.Color(255,0,0,128),pygame.Rect(mx//BS*BS,my//BS*BS,BS,BS))
        cellX = mx//BS
        cellY = my//BS
        if mouseState[0]:
            try:
                grid[cellY][cellX] = mode
            except Exception as e:
                print(e)
        
        if mouseState[2]:
            try:
                grid[cellY][cellX] = -1
            except Exception as e:
                print(e)
    

    
    for y in range(MW):
        for x in range(MH):
            if grid[y][x]==-2:
                window.blit(w_up,(x*BS,y*BS))
            if grid[y][x]==-3:
                window.blit(w_right,(x*BS,y*BS))
            
            if grid[y][x]==-4:
                window.blit(w_down,(x*BS,y*BS))
            if grid[y][x]==-5:
                window.blit(w_left,(x*BS,y*BS))
            if grid[y][x]==-6:
                window.blit(squareImg,(x*BS,y*BS))
            if grid[y][x]==-7:
                window.blit(deathWallImg,(x*BS+BS/4,y*BS))
            if grid[y][x]==-8:
                window.blit(h_deathWallImg,(x*BS,y*BS+BS/4))
            if grid[y][x]==-9:
                window.blit(trapwallImg,(x*BS,y*BS))
            
            
            
            else:
                pass
            if grid[y][x]==1:
                pygame.draw.circle(window,coin,(x*BS+BS/2,y*BS+BS/2),BS/10)
            if grid[y][x]==2:
                pygame.draw.circle(window,pygame.Color("Cyan"),(x*BS+BS/2,y*BS+BS/2),BS/5)
            if grid[y][x]==3:
                pygame.draw.rect(window,pygame.Color("Yellow"),pygame.Rect(x*BS,y*BS,BS,BS))
            if grid[y][x]==4:
                pygame.draw.rect(window,pygame.Color("green"),pygame.Rect(x*BS,y*BS,BS,BS))
            
    else:
        if mouseState[0] and mx>=0 and my>=0:
            if wallRect.collidepoint(mx,my):
                mode = 0
            if starRect.collidepoint(mx,my):
                mode = 1
            if coinRect.collidepoint(mx,my):
                mode = 2
            if startRect.collidepoint(mx,my):
                mode = 3
            if endRect.collidepoint(mx,my):
                mode = 4
            
        
        pass
    

        
    pygame.draw.rect(window,pygame.Color("Brown"),wallRect)
    pygame.draw.rect(window,pygame.Color("Gold"),starRect)
    pygame.draw.rect(window,pygame.Color("Cyan"),coinRect)
    pygame.draw.rect(window,pygame.Color("Yellow"),startRect)
    pygame.draw.rect(window,pygame.Color("Green"),endRect)
    
    pygame.draw.rect(window,pygame.Color("Green"),directionRect)
    
        
    for i in range(len(walls)):
        wal = walls[i]
        wal = pygame.transform.scale(wal,(BS*3,BS*3))
        rec = pygame.Rect(i*BS*MW/(len(walls)-1),MH*BS,BS*MW/(len(walls)-1),MH*BS)
        window.blit(wal,rec)
        if mouseState[0] and mx>=0 and my>=0:
            if rec.collidepoint(mx,my):
                mode = -2-i
                print(mode)
    
    if keys[pygame.K_SPACE]:
        for x in range(MW/2):
            pygame.draw.line(window,pygame.Color("White"),(x*BS,0),(x*BS,MH*BS),3)
        for y in range(MH/2):
            pygame.draw.line(window,pygame.Color("White"),(0,y*BS),(MW*BS,y*BS),3)
    
    for x in range(8):
        pygame.draw.line(window,pygame.Color("Red"),(x*BS*MW/(len(walls)-1),MH*BS),(x*BS*MW/(len(walls)-1),(MH+10)*BS),3)
    
    pygame.display.update()
    

    
    clock.tick(120)