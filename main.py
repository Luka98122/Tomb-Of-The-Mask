import pygame
import json

BS = 32
MW, MH = 60, 60

WS = 800

trueWindow = pygame.display.set_mode((WS,WS))
xShake,yShake =0,0


shakeTarget = -5


window = pygame.Surface((WS,WS))

wall = pygame.Color(204, 1, 222)
coin = pygame.Color(241, 191, 35)

coins = 0
stars = 0

class Particle():
    def __init__(self,x,y,dx,dy,timeleft,color):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.ddy = dy/10
        self.timeleft = timeleft
        self.color = color
        self.initTime = timeleft
        self.size = 4
    
    def update(self):
        self.x+=self.dx
        self.y+=self.dy
        

        
        
        if self.type=="goldfall":
            self.dy-=self.dy/5
            self.dx-=self.dx/5
            self.dy+=0.2
        elif self.type=="agf":
            self.dy+=0.08
            self.dx-=self.dx/3
            pass
        else:
            self.dy+=self.ddy
            self.dx-=self.dx/10
        
        self.timeleft-=1
        
        pass
    
    def draw(self):
        if self.type=="agf":
            self.size=2
        
        s = pygame.Surface((self.size,self.size))
        if self.timeleft/self.initTime>0.5:
            s.set_alpha(255)
        else:
            s.set_alpha(int(self.timeleft/self.initTime*254))
        pygame.draw.rect(s,self.color,pygame.Rect(0,0,self.size,self.size))
        window.blit(s,(self.x+cx*zoom,self.y+cy*zoom))
    
    
import random

class ParticleEmitter():
    def __init__(self,x,y,color,timeleft,frequency = 2):
        self.x = x
        self.y = y
        self.timeleft = timeleft
        self.color = color
        self.frequency = frequency
        self.rects = []
        self.type = "fall"
        self.tag = "none"
    
    def update(self):
        self.timeleft-=1
        if self.timeleft%self.frequency==0 and self.timeleft>0:
            if self.type=="fall":
                self.rects.append(Particle(self.x+BS/2,self.y+BS/2,random.randint(-3,3),random.randint(-3,3)/3,29,self.color))
                self.rects[-1].type=self.type
            if self.type=="goldfall":
                self.rects.append(Particle(self.x+BS/2,self.y+BS/2,random.randint(-7,7),random.randint(-7,7),25,self.color))
                self.rects[-1].type=self.type
            if self.type=="agf":
                self.rects.append(Particle(self.x+BS/2,self.y+BS/2,random.randint(-4,4),random.randint(-1,4),120,self.color))
                self.rects[-1].type=self.type
            
        
        
        try:
            print(self.rects[0].timeleft)
        except Exception as e:
            pass
        j = 0 
        while j <len(self.rects):
            em = self.rects[j]
            if em.timeleft<0:
                del self.rects[j]
                continue
            j+=1
            
        for part in self.rects:
            part.update()
            part.draw()
        

shakeFor = 0
            

# Particle emitter gets killed off prematurely and then the particles do too.

class ParticleManager():
    def __init__(self):
        self.emitters = []

    def update(self):
        i = 0
        while i <len(self.emitters):
            em = self.emitters[i]
            if em.timeleft<0 and len(em.rects)==0:
                del self.emitters[i]
                continue
            i+=1
        
        for em in self.emitters:
            em.update()
            
    def add(self, emitter:ParticleEmitter):
        self.emitters.append(emitter)



class Player:
    def __init__(self, x, y):
        self.frame = 0
        textures = []
        self.posses = [pygame.Vector2(x,y),pygame.Vector2(x,y),pygame.Vector2(x,y),pygame.Vector2(x,y),pygame.Vector2(x,y),pygame.Vector2(x,y),pygame.Vector2(x,y),pygame.Vector2(x,y)]
        for i in range(6):
            img = pygame.image.load(f"cont/playerAnim/{i}.png")
            img = pygame.transform.scale(img,(BS*zoom,BS*zoom))
            textures.append([])
            for i in range(4):
                textures[-1].append(pygame.transform.rotate(img,90*i))
        
        self.textures = textures
        self.x = x
        self.y = y
        self.size = BS
        self.landed = True
        self.dx = 0
        self.dy = 0
        self.mcd = 20
        self.done = False
        self.facing = 0
        self.cxleft = 5
        self.pcnt = 1

    def move(self, keys, grid):
        global cx
        global cy
        global screen
        global coins,stars
        global tCoins,tStars
        global shakeFor
        global waitCusDead
        
        self.mcd -= 1
        self.frame+=1
        try:
            if keys[pygame.K_LEFT] and self.landed and self.mcd <= 0:
                if grid[self.y][self.x - 1] >= -1:
                    self.dx = -1
                    self.facing = 270
                    self.landed = False
                    self.mcd = 20
                    self.frame = 0
            if keys[pygame.K_RIGHT] and self.landed and self.mcd <= 0:
                if grid[self.y][self.x + 1] >= -1:
                    self.dx = 1
                    self.facing = 90
                    self.landed = False
                    self.mcd = 20
                    self.frame = 0
            if keys[pygame.K_DOWN] and self.landed and self.mcd <= 0:
                if grid[self.y + 1][self.x] >= -1:
                    self.dy = 1
                    self.facing = 0
                    self.landed = False
                    self.mcd = 20
                    self.frame = 0
            if keys[pygame.K_UP] and self.landed and self.mcd <= 0:
                if grid[self.y - 1][self.x] >= -1:
                    self.dy = -1
                    self.facing = 180
                    self.landed = False
                    self.mcd = 20
                    self.frame = 0  

            y = self.y
            x = self.x

            try:
                if grid[y][x-1]==-9 and grid[y][x]<9999:
                    grid[y][x]=10199
                    
            except Exception as e: pass
            
            try:
                if grid[y][x+1]==-9 and grid[y][x]<9999:
                    grid[y][x]=10199
            except Exception as e: pass
            
            try:
                if grid[y-1][x]==-9 and grid[y][x]<9999:
                    grid[y][x]=10199
            except Exception as e: pass
            
            try:
                if grid[y+1][x]==-9 and grid[y][x]<9999:
                    grid[y][x]=10199
            except Exception as e: pass

            if grid[self.y + self.dy][self.x + self.dx] < 0 and grid[self.y + self.dy][self.x + self.dx] != -1:
                if grid[self.y+self.dy][self.x+self.dx] in [-7,-8] and waitCusDead==-1:
                    pm.add(ParticleEmitter((self.x+self.dx/2)*BS,(self.y+self.dy/2)*BS,coin,33,0.5))
                    pm.emitters[-1].type="goldfall"
                    
                    waitCusDead = 30
                    return
                self.landed = True
                
                shakeFor = 8
                pm.add(ParticleEmitter((self.x+self.dx/2)*BS,(self.y+self.dy/2)*BS,pygame.Color(72, 14, 255),48,5))
                pm.emitters[-1].type="fall"
                self.dx = 0
                self.dy = 0
                self.mcd = 6
            else:
                if waitCusDead==-1:
                    self.x += self.dx
                    self.y += self.dy
                    self.posses[0] = pygame.Vector2(self.x,self.y)
                    
                    cx -= self.dx * BS
                    cy -= self.dy * BS

            for i in range(1,len(self.posses)):
                cur = len(self.posses)-i
                self.posses[cur]=self.posses[cur-1]
                

            if grid[self.y][self.x] == 1:
                tCoins+=1
                grid[self.y][self.x] = -1
            if grid[self.y][self.x] == 2:
                tStars+=1
                pm.add(ParticleEmitter((self.x+self.dx/2)*BS,(self.y+self.dy/2)*BS,coin,33,1))
                pm.emitters[-1].type="goldfall"
                grid[self.y][self.x] = -1
        except IndexError as e:
            print("Out of bounds!")
            screen=0
        

    def draw(self):
        if waitCusDead==-1:
            if self.frame>=60:
                self.frame=0
            
            img = self.textures[self.frame//10][self.facing//90]
            
            for i in range(1,len(self.posses)):
                for j in range(1,4):
                    if self.posses[i].x==self.x and self.posses[i].y==self.y:
                        break
                    coord = pygame.Vector2((self.posses[i].x*BS+10)*zoom+cx*zoom,(self.posses[i].y*BS)*zoom+cy*zoom)
                    coord2 = pygame.Vector2((self.posses[i-1].x*BS+10)*zoom+cx*zoom,(self.posses[i-1].y*BS)*zoom+cy*zoom)
                    coord2.y+=BS/3.8*zoom*j
                    coord.y +=BS/3.8*zoom*j
                    
                    if j==1 or j==3:
                        coord.x+=self.dx*0.3*BS
                        coord2.x+=self.dx*0.3*BS
                        
                    
                    if coord2.x!=coord.x:
                        pygame.draw.line(window,pygame.Color(255,255,0),coord,coord2,3)
                    
                    coord = pygame.Vector2((self.posses[i].x*BS+2)*zoom+cx*zoom,(self.posses[i].y*BS)*zoom+cy*zoom)
                    coord2 = pygame.Vector2((self.posses[i-1].x*BS+2)*zoom+cx*zoom,(self.posses[i-1].y*BS)*zoom+cy*zoom)
                    coord2.x+=BS/3.8*zoom*j
                    coord.x +=BS/3.8*zoom*j
                    
                    if coord2.y!=coord.y:
                        pygame.draw.line(window,pygame.Color(255,255,0),coord,coord2,3)
            
                
            if self.dx==0 and self.dy==0:
                window.blit(img,((self.x * BS) * zoom + cx * zoom, (self.y * BS) * zoom + cy * zoom))
            else:
                self.frame = 0
                window.blit(self.ball,((self.x * BS) * zoom + cx * zoom, (self.y * BS) * zoom + cy * zoom))
            pass
            #pygame.draw.circle(window, pygame.Color("Red"), 
            #                   ((self.x * BS + BS / 2) * zoom + cx * zoom, 
            #                    (self.y * BS + BS / 2) * zoom + cy * zoom), BS * zoom / 3)


def initLevel(lvl):
    global grid
    global p
    global cx
    global cy
    global MH
    global MW
    global tStars
    global waitCusDead
    global tCoins
    tStars = 0
    tCoins = 0
    f = open(f"levels/{lvl}.json")
    grid = json.loads(f.read())
    f.close()
    px = 0
    py = 0

    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x]==3:
                py = y
                px = x
                break
    MH,MW = len(grid),len(grid[0])
    zoom = 1
    divisor = 2
    
    if selectedLevel==1:
        divisor=4
    
    print(f"Level {lvl} init")
    print(f"{px} {py}")
    cx = (-px+MW//divisor) * BS*zoom-2*BS*zoom
    cy = (-py+MH//divisor) * BS*zoom-2*BS*zoom
    print(f"{cx} {cy}")
    p.x = px
    p.y = py
    p.dx = 0
    p.dy = 0
    p.facing = 0
    p.landed = True
    p.posses = [pygame.Vector2(p.x,p.y)]*8
    waitCusDead = -1
    pm.emitters = []


pm = ParticleManager()


f = open("maps/1.json")
grid = json.loads(f.read())
f.close()
clock = pygame.time.Clock()


px = 0
py = 0

for y in range(len(grid)):
    for x in range(len(grid[y])):
        if grid[y][x]==3:
            py = y
            px = x
            break

zoom = 1

cx = (-px+MW//4) * BS*zoom#-5*BS*zoom
cy = (-py+MH//4) * BS*zoom#+8*BS*zoom

p = Player(px, py)

wall = pygame.Color(204, 1, 222)
coin = pygame.Color(241, 191, 35)




wallRect = pygame.Rect(BS * MW, 0, BS * 10, BS * MH / 3)
starRect = pygame.Rect(BS * MW, MW / 3 * BS, BS * 10, BS * MH / 3)
coinRect = pygame.Rect(BS * MW, MW / 3 * 2 * BS, BS * 10, BS * MH / 3)

directionRect = pygame.Rect(0, BS * MH, BS * MW, BS * MW)
clock = pygame.time.Clock()

wallImg = pygame.image.load("cont/wall1.png")
squareImg = pygame.image.load("cont/square.png")
exitImg = pygame.image.load("cont/exit.png")
starImg = pygame.image.load("cont/star.png")
playerImg = pygame.image.load("cont/playeridle.png")
ballImg = pygame.image.load("cont/ball.png")
ballImg=pygame.transform.scale(ballImg,(BS*zoom,BS*zoom))
playerImg = pygame.transform.scale(playerImg,(BS*zoom,BS*zoom))
p.ball = ballImg
p.img = playerImg
starImg = pygame.transform.scale(starImg,(BS*zoom,BS*zoom*0.9))
exitImg = pygame.transform.scale(exitImg,(BS*zoom,BS*zoom))
squareImg = pygame.transform.scale(squareImg, (BS * zoom, BS * zoom))
wallImg = pygame.transform.scale(wallImg, (BS * zoom, BS * zoom))

wallImg = pygame.transform.scale(wallImg, (BS * zoom, BS * zoom))

w_up = pygame.transform.rotate(wallImg, 180)
w_down = wallImg
w_left = pygame.transform.rotate(wallImg, 270)
w_right = pygame.transform.rotate(wallImg, 90)

walls = [w_up, w_right, w_down, w_left, squareImg]

screen = 0

TOTM = pygame.image.load("cont/totm.png")
TOTM = pygame.transform.scale(TOTM,(TOTM.get_width()*0.9,TOTM.get_height()*0.9))
purple = pygame.Color(207,5,255)
locked = pygame.image.load("cont/lockedlevel.png")
locked = pygame.transform.scale(locked,(locked.get_width()*1.2,locked.get_height()*1.2))

unlocked = pygame.image.load("cont/unlocked.png")
unlocked = pygame.transform.scale(unlocked,(locked.get_width()*1.2,locked.get_height()*1.2))

wallImg = pygame.image.load("cont/wall1.png")
squareImg = pygame.image.load("cont/square.png")
squareImg = pygame.transform.scale(squareImg,(BS,BS))
wallImg = pygame.transform.scale(wallImg,(BS,BS))

trapwallImg = pygame.image.load("cont/trapwall.png")
trapwallImg = pygame.transform.scale(trapwallImg,(BS,BS))

deathWallImg = pygame.image.load("cont/deathwall.png")
deathWallImg = pygame.transform.scale(deathWallImg,(BS*0.5,BS))

h_deathWallImg = pygame.transform.rotate(deathWallImg,90)

wallImg = pygame.transform.scale(wallImg,(BS,BS))

w_up = pygame.transform.rotate(wallImg,180)
w_down = wallImg
w_left = pygame.transform.rotate(wallImg,270)
w_right = pygame.transform.rotate(wallImg,90)

walls = [w_up,w_right,w_down,w_left,squareImg,deathWallImg,h_deathWallImg]

level = 1
pygame.init()
font_stars = pygame.font.Font("cont/font.ttf",30)

level_stats = {}

spikeImg = pygame.transform.scale(pygame.image.load("cont/spike.png"),(BS,BS))

prespikes= []

for i in range(1,6):
    f = open(f"levels/{i}.json","r")
    grid2 = json.loads(f.read())
    f.close()
    
    thisStars = 0
    thisCoins = 0
    
    for row in grid2:
        thisStars+=row.count(2)
        thisCoins+=row.count(1)
    
    
    
    level_stats[i] = {2: [0,thisStars],1: [0,thisCoins]}
    
    
prespikeImg = pygame.transform.scale(pygame.image.load("cont/prespike.png"),(BS,BS))
    
spikes = []
for i in range(4):
    spikes.append(pygame.transform.rotate(spikeImg,90*i))

for i in range(4):
    prespikes.append(pygame.transform.rotate(prespikeImg,90*i))


menuManager = ParticleManager()
menuManager.type="agf"


pygame.mixer.init()
pygame.mixer.music.load("cont/music.mp3")
pygame.mixer.music.play(-1)


# Muzika
# Promeni boju exita
# Menu ( Reset, etc)
# Speedrun

igt = 0
tgt = 0


waitCusDead = -1

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            exit()
    
    mouseState = pygame.mouse.get_pressed()
    keys = pygame.key.get_pressed()
    mx, my = pygame.mouse.get_pos()
    
    
    if shakeFor>0:
        shakeFor-=1
        xShake+=random.randint(-3,3)
        yShake+=random.randint(-3,3)
        
        xShake = max(xShake,-20)
        xShake = min(xShake,20)
        
        yShake = max(yShake,-20)
        yShake = min(yShake,20)
    else:
        xShake=0
        yShake=0
    
    
    tgt+=1
    if screen==0:
        window.fill("black")
        window.blit(TOTM,(20,10))
        cx,cy = 0,0
        textTime = font_stars.render(f"{igt//(60*60)}:{(igt%3600)//60}:{int(igt%60*1.6)}",True,pygame.Color("Green"))
        window.blit(textTime,(630,150))
        if stars>=15:
            if len(menuManager.emitters)==1:
                if menuManager.emitters[0].tag == "left_eye":
                    newEmitter = ParticleEmitter(160,90,coin,100000,1)
                    newEmitter.tag="right_eye"
                    newEmitter.type="agf"
                    menuManager.add(newEmitter)
                elif menuManager.emitters[0].tag == "right_eye":
                    newEmitter = ParticleEmitter(120,90,coin,100000,1)
                    newEmitter.tag="left_eye"
                    newEmitter.type="agf"
                    menuManager.add(newEmitter)
                    pass
            if len(menuManager.emitters)==0:
                newEmitter = ParticleEmitter(160,90,coin,100000,1)
                newEmitter.tag="right_eye"
                newEmitter.type="agf"
                menuManager.add(newEmitter)
                newEmitter = ParticleEmitter(120,90,coin,100000,1)
                newEmitter.tag="left_eye"
                newEmitter.type="agf"
                menuManager.add(newEmitter)
                pass
        textStars = font_stars.render(f"{stars}/15",True,coin)
        window.blit(textStars,(330,150))
        window.blit(pygame.transform.scale(starImg,(starImg.get_width()*1.1,starImg.get_height()*1.1)),(400+30*(stars//10),160))
        
        for i in range(5):
            curRect = pygame.Rect(WS/2-locked.get_width()//2,WS/8*i+250,locked.get_width(),locked.get_height())
            if mouseState[0] and curRect.collidepoint((mx,my)) and (5-i)<=level:
                selectedLevel = (5-i)
                screen = 1
                initLevel(selectedLevel)
            if (5-i)>level:
                window.blit(locked,(WS/2-locked.get_width()//2,WS/8*i+250))
                pygame.draw.line(window,purple,(WS/2-locked.get_width()//2+locked.get_width()//2,  WS/8*i+250+locked.get_height()),(WS/2-locked.get_width()//2+locked.get_width()//2,WS/8*i+250+locked.get_height()*2+20),2)
            elif (5-i)==level:
                window.blit(locked,(WS/2-locked.get_width()//2,WS/8*i+250))
                pygame.draw.line(window,pygame.Color(255,255,0),(WS/2-unlocked.get_width()//2+unlocked.get_width()//2,  WS/8*i+250+unlocked.get_height()),(WS/2-unlocked.get_width()//2+unlocked.get_width()//2,WS/8*i+250+unlocked.get_height()*2+20),2)

            else:
                window.blit(unlocked,(WS/2-unlocked.get_width()//2,WS/8*i+250))
                pygame.draw.line(window,pygame.Color(255,255,0),(WS/2-unlocked.get_width()//2+unlocked.get_width()//2,  WS/8*i+250+unlocked.get_height()),(WS/2-unlocked.get_width()//2+unlocked.get_width()//2,WS/8*i+250+unlocked.get_height()*2+20),2)

        pygame.draw.line(window,pygame.Color(255,255,0),(WS/2-locked.get_width()//2+locked.get_width()//2,WS*0.92),(WS/2-locked.get_width()//2+locked.get_width()//2,WS+2),2)
        menuManager.update()
        trueWindow.blit(window,(xShake,yShake))
        pygame.display.update()
            
    else:
        window.fill("black")
        igt+=1
        


        for y in range(MW):
            for x in range(MH):
                tile_x = (x * BS + cx) * zoom
                tile_y = (y * BS + cy) * zoom

                if grid[y][x] == -2:
                    window.blit(w_up, (tile_x, tile_y))
                if grid[y][x] == -3:
                    window.blit(w_right, (tile_x, tile_y))

                if grid[y][x] == -4:
                    window.blit(w_down, (tile_x, tile_y))
                if grid[y][x] == -5:
                    window.blit(w_left, (tile_x, tile_y))
                if grid[y][x] == -6:
                    window.blit(squareImg, (tile_x, tile_y))
                if grid[y][x]==-7:
                    window.blit(deathWallImg,(tile_x+BS/4,tile_y))
                if grid[y][x]==-8:
                    window.blit(h_deathWallImg,(tile_x,tile_y+BS/4))
                if grid[y][x]==-9:
                    window.blit(trapwallImg,(tile_x,tile_y))
                
                if grid[y][x]>=10000:
                    grid[y][x]-=1
                
                if grid[y][x]>=10030 and grid[y][x]<10175: # Spike
                    img = None
                    try:
                        if grid[y][x+1]==-9:
                            img = spikes[3]
                    except Exception as e:
                        pass
                    
                    try:
                        if grid[y][x-1]==-9:
                            img = spikes[1]
                    except Exception as e:
                        pass
                    
                    try:
                        if grid[y+1][x]==-9:
                            img = spikes[2]
                    except Exception as e:
                        pass
                    
                    try:
                        if grid[y-1 ][x]==-9:
                            img = spikes[0]
                    except Exception as e:
                        pass
                    window.blit(img,(tile_x,tile_y))
                
                if (grid[y][x]>=10175 and grid[y][x]<10200) or (grid[y][x]>=10000 and grid[y][x]<10030):#Prespike
                    img = None
                    try:
                        if grid[y][x+1]==-9:
                            img = prespikes[2]
                    except Exception as e:
                        pass
                    
                    try:
                        if grid[y][x-1]==-9:
                            img = prespikes[0]
                    except Exception as e:
                        pass
                    
                    try:
                        if grid[y+1][x]==-9:
                            img = prespikes[1]
                    except Exception as e:
                        pass
                    
                    try:
                        if grid[y-1 ][x]==-9:
                            img = prespikes[3]
                    except Exception as e:
                        pass
                    window.blit(img,(tile_x,tile_y))
                
                if grid[y][x]==9999:
                    grid[y][x]=-1
                if grid[y][x] == 1:
                    pygame.draw.circle(window, coin, (tile_x + BS * zoom / 2, tile_y + BS * zoom / 2), BS * zoom / 10)
                if grid[y][x] == 2:
                    window.blit(starImg,(tile_x,tile_y))
                    #pygame.draw.circle(window, pygame.Color("Cyan"), (tile_x + BS * zoom / 2, tile_y + BS * zoom / 2), BS * zoom / 5)
                #if grid[y][x]==3:
                #    pygame.draw.rect(window,pygame.Color("Yellow"),pygame.Rect(tile_x,tile_y,BS*zoom,BS*zoom))
                if grid[y][x]==4:
                    window.blit(exitImg,(tile_x,tile_y))
                    # pygame.draw.rect(window,pygame.Color("green"),pygame.Rect(tile_x,tile_y,BS*zoom,BS*zoom))
        p.move(keys, grid)
        p.draw()
        pm.update()
        
        trueWindow.blit(window,(xShake,yShake))
        
        pygame.display.update()
        
        if grid[p.y][p.x]>10030 and grid[p.y][p.x]<10175 and waitCusDead==-1:
            waitCusDead=30
            pm.add(ParticleEmitter((p.x+p.dx/2)*BS,(p.y+p.dy/2)*BS,coin,33,0.5))
            pm.emitters[-1].type="goldfall"
            
        if p.y<0 or p.x<0:
            screen=0
            
        if waitCusDead==0:
            screen = 0
        elif waitCusDead>0:
            waitCusDead-=1
        else:
            pass
        
        if grid[p.y][p.x]==4:
            if p.done:
                print(f"Coins: {coins}")
                print(f"Stars: {stars}")
                
                level_stats[selectedLevel][2][0] = max(level_stats[selectedLevel][2][0],tStars)
                level_stats[selectedLevel][1][0] = max(level_stats[selectedLevel][1][0],tCoins)
                stars = 0
                for i in range(1,6):
                    stars += level_stats[i][2][0]
                
                screen=0
                level=max(level,selectedLevel+1)
            p.done=True
    clock.tick(60)
