import pygame
import math

class Key(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, id):
        super(Key, self).__init__()
        self.clicked = False
        self.id = id
        self.poi = [(0,0,0)] # (xpos, ypos, radius)
        self.x = xpos
        self.y = ypos
        self.r = 255
        self.g = 0
        self.b = 255

pygame.init()
#size = (pygame.display.Info().current_w,pygame.display.Info().current_h)
size = (1920,1080)
step = 40
#size = (2560,1440)
screen = pygame.display.set_mode(size, pygame.RESIZABLE)
irisCoords = [screen.get_width()/2, screen.get_height()/2, 120, 80]
pygame.display.set_caption("MoonYard Top-Down")
moon = pygame.Color(32,32,32)
red = pygame.Color(220,80,50)
blue = pygame.Color(50,220,220)
green = pygame.Color(50,180,100)
darkblue = pygame.Color(50,140,240)
purple = pygame.Color(140,50,180)
pink = pygame.Color(200,30,180)
iris = pygame.Color(255,int(255*.843),0)
screen.fill(moon)
pygame.display.flip()
done = False
clock = pygame.time.Clock()
offset = [0,0,0] # x,y,deg
screenPos = [0,0] #x,y 
rovPos = [0,0] #rov center
#screenCen = [768, 420]
screenCen = [960, 540]
loc = []
cur = [0,0,0,None]
radius = 20
angle = 1
MoonYard_Scale = 20 # This number controls how much the map shifts
my_size = 2.54
poi_selected = False


def getPos():
    pos = pygame.mouse.get_pos()
    return pos

def addPoi():
    pos = getPos()
    pygame.draw.circle(screen,blue,pos,radius)
    loc.append([pos[0],pos[1],int(radius*(my_size/1.25)),blue, len(loc) + 1])
    

def addCur(x,y,r):
    if(not cur == None):
        pygame.draw.circle(screen,green,(x,y),r+10)

def redrawPoi():
    for p in loc:
        if(p[0] >= -p[2] and p[1] >= -p[2]):    
            pygame.draw.circle(screen,p[3],(p[0],p[1]),p[2])
            font = pygame.font.Font(None,30)
            num = font.render(str(p[4]), True, (0,0,0))
            screen.blit(num, (p[0]-5, p[1]-10))
            #if(p[0] == cur[0] and p[1] == cur[1]):
            #    angle = math.tan((abs(p[1] - rovPos[1]))/(abs(p[0] - rovPos[0])) * math.pi /180)*180/math.pi
            #    font = pygame.font.Font(None,20)
            #    text = font.render(f'{angle} deg',False,(0,0,0))
            #    screen.blit(text, (p[0] - 25, p[1] + 10))
        #text = font.render(f'Dist: {int((math.sqrt(((p[0]-(1920/2))**2)+((p[1]-(1080/2))**2))/my_size))-p[2]} cm  Size: {int(p[2]/(2))} cm',False,(0,0,0))
        #screen.blit(text, (p[0]-p[2]//2,p[1]-p[2]//2))
        
def redrawCur():
    if(not cur == None and poi_selected == True):
        for p in loc:
            if(p[0] == cur[0] and p[1] == cur[1]):
                pygame.draw.line(screen,p[3],(irisCoords[0],irisCoords[1]),(p[0],p[1]),3)

def redrawIris():
    surf =  pygame.Surface((120, 80))
    surf.fill(iris)
    #set a color key for blitting
    surf.set_colorkey((255, 0, 0))

    blittedRect = pygame.Rect(irisCoords[0] - irisCoords[2]//2, irisCoords[1] - irisCoords[3]//2, irisCoords[2], irisCoords[3])
    oldCenter = blittedRect.center
    rotatedSurf =  pygame.transform.rotate(surf, offset[2])
    rotRect = rotatedSurf.get_rect()
    rotRect.center = oldCenter
    offset[0] = (oldCenter[0] - screenCen[0] - screenPos[0])
    offset[1] = (oldCenter[1] - screenCen[1] - screenPos[1])

    pygame.draw.circle(screen, iris, rotRect.center, 72, 2)
    screen.blit(rotatedSurf, rotRect)
    pygame.display.flip()

def redrawGrid():
    rovPos[0] = offset[0] + screenCen[0] + screenPos[0]
    rovPos[1] = offset[1] + screenCen[1] + screenPos[1]

    if(offset[2] < 45 or offset[2] > 315):
        for i in range(-50, 50, 1):    
            p5 = (rovPos[0] + int(math.cos(-offset[2] * math.pi/180) * 3000)- 0, rovPos[1] + int(math.sin(-offset[2] * math.pi/180) * 3000) - int(step/math.cos(offset[2] * math.pi / 180))*i)
            p6 = (rovPos[0] - int(math.cos(-offset[2] * math.pi/180) * 3000)- 0, rovPos[1] - int(math.sin(-offset[2] * math.pi/180) * 3000) - int(step/math.cos(offset[2] * math.pi / 180))*i)
            p3 = (rovPos[0] - int(math.cos(-(90-offset[2]) * math.pi/180) * 3000) - int(step/math.cos(offset[2] * math.pi / 180))*i- 0, rovPos[1] + int(math.sin(-(90-offset[2]) * math.pi/180) * 3000))
            p4 = (rovPos[0] + int(math.cos(-(90-offset[2]) * math.pi/180) * 3000) - int(step/math.cos(offset[2] * math.pi / 180))*i- 0, rovPos[1] - int(math.sin(-(90-offset[2]) * math.pi/180) * 3000))
            if(i % 3 == 0):
                pygame.draw.line(screen, (150, 150, 150), p5, p6, 3)
                pygame.draw.line(screen, (150, 150, 150), p3, p4, 3)
            else:
                pygame.draw.line(screen, (100, 100, 100), p5, p6, 2)
                pygame.draw.line(screen, (100, 100, 100), p3, p4, 2)
            
    elif(offset[2] < 135):
        for i in range(-50, 50, 1):    
            p5 = (rovPos[0] + int(math.cos(-offset[2] * math.pi/180) * 3000) - int(step/math.sin(offset[2] * math.pi / 180))*i- 0, rovPos[1] + int(math.sin(-offset[2] * math.pi/180) * 3000))
            p6 = (rovPos[0] - int(math.cos(-offset[2] * math.pi/180) * 3000) - int(step/math.sin(offset[2] * math.pi / 180))*i- 0, rovPos[1] - int(math.sin(-offset[2] * math.pi/180) * 3000))
            p3 = (rovPos[0] - int(math.cos(-(90-offset[2]) * math.pi/180) * 3000)- 0, rovPos[1] + int(math.sin(-(90-offset[2]) * math.pi/180) * 3000) - int(step/math.sin(offset[2] * math.pi / 180))*i)
            p4 = (rovPos[0] + int(math.cos(-(90-offset[2]) * math.pi/180) * 3000)- 0, rovPos[1] - int(math.sin(-(90-offset[2]) * math.pi/180) * 3000) - int(step/math.sin(offset[2] * math.pi / 180))*i)
            if(i % 3 == 0):
                pygame.draw.line(screen, (150, 150, 150), p5, p6, 3)
                pygame.draw.line(screen, (150, 150, 150), p3, p4, 3)
            else:
                pygame.draw.line(screen, (100, 100, 100), p5, p6, 2)
                pygame.draw.line(screen, (100, 100, 100), p3, p4, 2)

    elif(offset[2] < 225):
        for i in range(-50, 50, 1):    
            p5 = (rovPos[0] + int(math.cos(-offset[2] * math.pi/180) * 3000)- 0, rovPos[1] + int(math.sin(-offset[2] * math.pi/180) * 3000) - int(step/math.cos((180 - offset[2]) * math.pi / 180))*i)
            p6 = (rovPos[0] - int(math.cos(-offset[2] * math.pi/180) * 3000)- 0, rovPos[1] - int(math.sin(-offset[2] * math.pi/180) * 3000) - int(step/math.cos((180 - offset[2]) * math.pi / 180))*i)
            p3 = (rovPos[0] - int(math.cos(-(90-offset[2]) * math.pi/180) * 3000) - int(step/math.cos((180 - offset[2]) * math.pi / 180))*i- 0, rovPos[1] + int(math.sin(-(90-offset[2]) * math.pi/180) * 3000))
            p4 = (rovPos[0] + int(math.cos(-(90-offset[2]) * math.pi/180) * 3000) - int(step/math.cos((180 - offset[2]) * math.pi / 180))*i- 0, rovPos[1] - int(math.sin(-(90-offset[2]) * math.pi/180) * 3000))
            if(i % 3 == 0):
                pygame.draw.line(screen, (150, 150, 150), p5, p6, 3)
                pygame.draw.line(screen, (150, 150, 150), p3, p4, 3)
            else:
                pygame.draw.line(screen, (100, 100, 100), p5, p6, 2)
                pygame.draw.line(screen, (100, 100, 100), p3, p4, 2)
    else:
        for i in range(-50, 50, 1):    
            p5 = (rovPos[0] + int(math.cos(-offset[2] * math.pi/180) * 3000) - int(step/math.sin((180-offset[2]) * math.pi / 180))*i- 0, rovPos[1] + int(math.sin(-offset[2] * math.pi/180) * 3000))
            p6 = (rovPos[0] - int(math.cos(-offset[2] * math.pi/180) * 3000) - int(step/math.sin((180-offset[2]) * math.pi / 180))*i- 0, rovPos[1] - int(math.sin(-offset[2] * math.pi/180) * 3000))
            p3 = (rovPos[0] - int(math.cos(-(90-offset[2]) * math.pi/180) * 3000)- 0, rovPos[1] + int(math.sin(-(90-offset[2]) * math.pi/180) * 3000) - int(step/math.sin((180-offset[2]) * math.pi / 180))*i)
            p4 = (rovPos[0] + int(math.cos(-(90-offset[2]) * math.pi/180) * 3000)- 0, rovPos[1] - int(math.sin(-(90-offset[2]) * math.pi/180) * 3000) - int(step/math.sin((180-offset[2]) * math.pi / 180))*i)
            if(i % 3 == 0):
                pygame.draw.line(screen, (150, 150, 150), p5, p6, 3)
                pygame.draw.line(screen, (150, 150, 150), p3, p4, 3)
            else:
                pygame.draw.line(screen, (100, 100, 100), p5, p6, 2)
                pygame.draw.line(screen, (100, 100, 100), p3, p4, 2)
        
        


def redrawAtlas():
    font = pygame.font.Font(None,40)
    text = font.render(f'X: {offset[0]//4} Y: {offset[1]//4} A: {offset[2]}',False,(150,150,150))
    screen.blit(text, (0,0))

def redrawDist():
    for p in loc:
        pygame.draw.line(screen,p[3],(irisCoords[0],irisCoords[1]),(p[0],p[1]),3)

def resizeScreen():
    #screen = pygame.display.set_mode((screen.get_width(), screen.get_height()), pygame.RESIZABLE)
    pass

def redrawAll():
    offset[2] = offset[2] % 360
    resizeScreen()
    screen.fill(moon)
    redrawGrid()
    #redrawDist()
    redrawCur()
    redrawPoi()
    redrawAtlas()
    redrawIris()
    pygame.display.update()

while not done:
    redrawAll()
    #except Exception as e: print(e)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            x = pos[0]
            y = pos[1]
            #print(x,y,event.button)
            if(event.button == 1):
                poi_selected = False
                dc = False
                for i in range(len(loc)):
                    #if((x>loc[i][0]+(2*loc[i][2]) or x<loc[i][0]-(2*loc[i][2])) or (y>loc[i][1]+(2*loc[i][2]) or y<loc[i][1]-(2*loc[i][2]))):
                    if((x>loc[i][0]+(1*loc[i][2]) or x<loc[i][0]-(1*loc[i][2])) or (y>loc[i][1]+(1*loc[i][2]) or y<loc[i][1]-(1*loc[i][2]))):
                        pass
                    else:
                        print("New POI is too close to an existing POI")
                        dc = True
                if(not dc):
                    poi_selected = True
                    addPoi()
                    cur = [x,y,radius,green]
                    addCur(cur[0],cur[1],cur[2])
                    pygame.display.update()
            elif(event.button == 3):
                poi_selected = False
                for i in range(len(loc)):
                    if((x<loc[i][0]+(loc[i][2]) and x>loc[i][0]-(loc[i][2])) and (y<loc[i][1]+(loc[i][2]) and y>loc[i][1]-(loc[i][2]))):
                        cur = [loc[i][0],loc[i][1],loc[i][2],green]
                        poi_selected = True
                    else:
                        pass
                if(poi_selected):
                    addCur(cur[0],cur[1],cur[2])
                    pygame.display.update()
                else:
                    cur = None
            if(event.button == 4 and poi_selected):
                i=0
                for p in loc:
                    if(p[0] == cur[0] and p[1] == cur[1]):
                        loc[i][2] += 5
                        cur[2] += 5
                    i+=1
                pygame.display.update()  
            if(event.button == 5 and poi_selected):
                i=0
                for p in loc:
                    if(p[0] == cur[0] and p[1] == cur[1] and loc[i][2] > 5):
                        loc[i][2] -= 5
                        cur[2] -= 5
                    i+=1
                pygame.display.update()
        if(event.type == pygame.KEYDOWN):
            if(event.key == pygame.K_LEFT and poi_selected):
                for p in loc:
                    if(p[0] == cur[0] and p[1] == cur[1]):
                        p[0] -= int(math.cos(offset[2] * math.pi / 180) * MoonYard_Scale)
                        p[1] += int(math.sin(offset[2] * math.pi / 180) * MoonYard_Scale)
                        if(cur != None):
                            cur[0] -= int(math.cos(offset[2] * math.pi / 180) * MoonYard_Scale)
                            cur[1] += int(math.sin(offset[2] * math.pi / 180) * MoonYard_Scale)
            elif(event.key == pygame.K_LEFT):
                offset[2] += angle
            if(event.key == pygame.K_RIGHT and poi_selected):
                for p in loc:
                    if(p[0] == cur[0] and p[1] == cur[1]):
                        p[0] += int(math.cos(offset[2] * math.pi / 180) * MoonYard_Scale)
                        p[1] -= int(math.sin(offset[2] * math.pi / 180) * MoonYard_Scale)
                        if(cur != None):
                            cur[0] += int(math.cos(offset[2] * math.pi / 180) * MoonYard_Scale)
                            cur[1] -= int(math.sin(offset[2] * math.pi / 180) * MoonYard_Scale)
            elif(event.key == pygame.K_RIGHT):
                offset[2] -= angle
            if(event.key == pygame.K_UP and poi_selected):
                for p in loc:
                    if(p[0] == cur[0] and p[1] == cur[1]):
                        p[0] -= int(math.sin(offset[2] * math.pi / 180) * MoonYard_Scale)
                        p[1] -= int(math.cos(offset[2] * math.pi / 180) * MoonYard_Scale)
                        if(cur != None):
                            cur[0] -= int(math.sin(offset[2] * math.pi / 180) * MoonYard_Scale)
                            cur[1] -= int(math.cos(offset[2] * math.pi / 180) * MoonYard_Scale)
            elif(event.key == pygame.K_UP):
                irisCoords[0] += int(math.cos(offset[2] * math.pi / 180) * MoonYard_Scale)
                irisCoords[1] -= int(math.sin(offset[2] * math.pi / 180) * MoonYard_Scale)
            if(event.key == pygame.K_DOWN and poi_selected):
                for p in loc:
                    if(p[0] == cur[0] and p[1] == cur[1]):
                        p[0] += math.sin(offset[2] * math.pi / 180) * MoonYard_Scale
                        p[1] += math.cos(offset[2] * math.pi / 180) * MoonYard_Scale
                        if(cur != None):
                            cur[0] += int(math.sin(offset[2] * math.pi / 180) * MoonYard_Scale)
                            cur[1] += int(math.cos(offset[2] * math.pi / 180) * MoonYard_Scale)
            elif(event.key == pygame.K_DOWN):
                irisCoords[0] -= int(math.cos(offset[2] * math.pi / 180) * MoonYard_Scale)
                irisCoords[1] += int(math.sin(offset[2] * math.pi / 180) * MoonYard_Scale)
            if(event.key == pygame.K_a):
                for p in loc:
                    p[0] -= MoonYard_Scale
                irisCoords[0] -= MoonYard_Scale
                screenPos[0] -= MoonYard_Scale
            if(event.key == pygame.K_d):
                for p in loc:
                    p[0] += MoonYard_Scale
                irisCoords[0] += MoonYard_Scale
                screenPos[0] += MoonYard_Scale
            if(event.key == pygame.K_s):
                for p in loc:
                    p[1] += MoonYard_Scale
                irisCoords[1] += MoonYard_Scale
                screenPos[1] += MoonYard_Scale
            if(event.key == pygame.K_w):
                for p in loc:
                    p[1] -= MoonYard_Scale
                irisCoords[1] -= MoonYard_Scale
                screenPos[1] -= MoonYard_Scale              

            if(event.key == pygame.K_r and poi_selected == True):
                for p in loc:
                    if(p[0] == cur[0] and p[1] == cur[1]):
                        if(p[3] != red): p[3] = red
                        else: p[3] = blue
            if(event.key == pygame.K_g and poi_selected == True):
                for p in loc:
                    if(p[0] == cur[0] and p[1] == cur[1]):
                        if(p[3] != green): p[3] = green
                        else: p[3] = blue
            if(event.key == pygame.K_b and poi_selected == True):
                for p in loc:
                    if(p[0] == cur[0] and p[1] == cur[1]):
                        p[3] = blue
            if(event.key == pygame.K_c and poi_selected == True):
                for p in loc:
                    if(p[0] == cur[0] and p[1] == cur[1]):
                        if(p[3] == blue):
                            p[3] = darkblue
                        elif(p[3] == darkblue):
                            p[3] = purple
                        elif(p[3] == purple):
                            p[3] = pink 
                        elif(p[3] == pink): 
                            p[3] = red
            if(event.key == pygame.K_x and poi_selected == True):
                for p in loc:
                    if(p[0] == cur[0] and p[1] == cur[1]):
                        if(p[3] == red):
                            p[3] = pink
                        elif(p[3] == pink):
                            p[3] = purple
                        elif(p[3] == purple):
                            p[3] = darkblue
                        elif(p[3] == darkblue): 
                            p[3] = blue
            if(event.key == pygame.K_DELETE and poi_selected == True):
                for p in loc:
                    if(p[0] == cur[0] and p[1] == cur[1]):
                        temp = p
                        loc.remove(p)
                        for p in loc:
                            if(p[4] > temp[4]):
                                p[4] -= 1
                        poi_selected = False
                        print("Removed POI")

            if(event.key == pygame.K_ESCAPE):
                pygame.quit()

pygame.quit()
