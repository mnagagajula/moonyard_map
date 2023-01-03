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
#size = (2560,1440)
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
pygame.display.set_caption("MoonYard Top-Down")
moon = pygame.Color(255,255,255)
red = pygame.Color(200,50,50)
blue = pygame.Color(0,250,250)
green = pygame.Color(100,250,100)
darkblue = pygame.Color(100,150,250)
purple = pygame.Color(150,0,200)
pink = pygame.Color(200,0,200)
iris = pygame.Color(255,int(255*.843),0)
screen.fill(moon)
pygame.display.flip()
done = False
clock = pygame.time.Clock()
offset = [0,0,0] # x,y,deg
loc = []
cur = [0,0,0,None]
radius = 20
angle = 1
MoonYard_Scale = 5 # This number controls how much the map shifts
my_size = 2.54
poi_selected = False

def getPos():
    pos = pygame.mouse.get_pos()
    return pos

def addPoi():
    pos = getPos()
    pygame.draw.circle(screen,blue,pos,radius)
    loc.append([pos[0],pos[1],int(radius*(my_size/1.25)),blue])

def addCur(x,y,r):
    if(not cur == None):
        pygame.draw.circle(screen,green,(x,y),r+10)

def redrawPoi():
    for p in loc:
        pygame.draw.circle(screen,p[3],(p[0],p[1]),p[2])
        font = pygame.font.Font(None,30)
        text = font.render(f'Dist: {int((math.sqrt(((p[0]-(1920/2))**2)+((p[1]-(1080/2))**2))/my_size))-p[2]} cm  Size: {int(p[2]/(2))} cm',False,(0,0,0))
        screen.blit(text, (p[0]-p[2]//2,p[1]-p[2]//2))

def redrawCur():
    if(not cur == None and poi_selected == True):
        pygame.draw.circle(screen,green,(cur[0],cur[1]),cur[2]+10)

def redrawGrid():
    for i in range(int(-abs(offset[0])//(100/my_size)),int(size[0]//(100/my_size)) + int(abs(offset[0])//(100/my_size)) + 2):
        lC = abs(int(math.sin(50*i*math.pi/180)*111))
        pygame.draw.line(screen,(lC,lC,lC),((100/my_size*i)+offset[0],0),((100/my_size*i)+offset[0],size[1]),3)
    for i in range(int(-abs(offset[1])//(100/my_size)),int(size[1]//(100/my_size)) + int(abs(offset[1])//(100/my_size)) + 2):  
        lC = abs(int(math.sin(50*i*math.pi/180)*111))
        pygame.draw.line(screen,(lC,lC,lC),(0,(100/my_size*i)-offset[1]),(size[0],(100/my_size*i)-offset[1]),3)

def redrawAtlas():
    font = pygame.font.Font(None,40)
    text = font.render(f'X: {offset[0]} Y: {offset[1]} H: {offset[2]%360}',False,(0,0,0))
    screen.blit(text, (0,0))

def redrawDist():
    for p in loc:
        pygame.draw.line(screen,(0,0,0),(1920//2,1080//2),(p[0],p[1]),2)

def redrawIris():
    pygame.draw.rect(screen,iris,((size[0]//2 - 80, size[1]//2 - 40),(120,80)))
    #pygame.draw.rect(screen,iris,((size[1]//2 - 80, size[0]//2 - 40),(80, 120)))

def resizeScreen():
    #screen = pygame.display.set_mode((screen.get_width(), screen.get_height()), pygame.RESIZABLE)
    pass

def redrawAll():
    resizeScreen()
    screen.fill(moon)
    redrawGrid()
    redrawCur()
    redrawDist()
    redrawPoi()
    redrawIris()
    redrawAtlas()
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
                        p[0] -= MoonYard_Scale
                        if(cur != None):
                            cur[0] -= MoonYard_Scale
            elif(event.key == pygame.K_LEFT):
                poi_selected = False
                offset[0] += MoonYard_Scale
                for p in loc:
                    p[0] += MoonYard_Scale
                    if(cur != None):
                        cur[0] += MoonYard_Scale
            if(event.key == pygame.K_RIGHT and poi_selected):
                for p in loc:
                    if(p[0] == cur[0] and p[1] == cur[1]):
                        p[0] += MoonYard_Scale
                        if(cur != None):
                            cur[0] += MoonYard_Scale
            elif(event.key == pygame.K_RIGHT):
                poi_selected = False
                offset[0] -= MoonYard_Scale
                for p in loc:
                    p[0] -= MoonYard_Scale
                    if(cur != None):
                        cur[0] -= MoonYard_Scale
            if((event.key == pygame.K_UP or event.key == pygame.K_w) and poi_selected):
                for p in loc:
                    if(p[0] == cur[0] and p[1] == cur[1]):
                        p[1] -= MoonYard_Scale
                        if(cur != None):
                            cur[1] -= MoonYard_Scale
            elif(event.key == pygame.K_UP or event.key == pygame.K_w):
                poi_selected = False
                offset[1] -= MoonYard_Scale
                for p in loc:
                    p[1] += MoonYard_Scale
                    if(cur != None):
                        cur[1] += MoonYard_Scale
            if((event.key == pygame.K_DOWN or event.key == pygame.K_s) and poi_selected):
                for p in loc:
                    if(p[0] == cur[0] and p[1] == cur[1]):
                        p[1] += MoonYard_Scale
                        if(cur != None):
                            cur[1] += MoonYard_Scale
            elif(event.key == pygame.K_DOWN or event.key == pygame.K_s):
                poi_selected = False
                offset[1] += MoonYard_Scale
                for p in loc:
                    p[1] -= MoonYard_Scale
                    if(cur != None):
                        cur[1] -= MoonYard_Scale

            if(event.key == pygame.K_d):
                for p in loc:
                    x1 = ((p[0]-(1920/2))*math.cos(-angle*math.pi/180))-((p[1]-(1080/2))*math.sin(-angle*math.pi/180)) + (1920/2)
                    y1 = ((p[0]-(1920/2))*math.sin(-angle*math.pi/180))+((p[1]-(1080/2))*math.cos(-angle*math.pi/180)) + (1080/2)
                    p[0],p[1] = int(x1),int(y1)
                offset[2] += angle

            if(event.key == pygame.K_a):
                for p in loc:
                    x1 = ((p[0]-(1920/2))*math.cos(angle*math.pi/180))-((p[1]-(1080/2))*math.sin(angle*math.pi/180)) + (1920/2)
                    y1 = ((p[0]-(1920/2))*math.sin(angle*math.pi/180))+((p[1]-(1080/2))*math.cos(angle*math.pi/180)) + (1080/2)
                    p[0],p[1] = int(x1),int(y1)
                offset[2] -= angle

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
                        loc.remove(p)
                        poi_selected = False
                        print("Removed POI")

            if(event.key == pygame.K_ESCAPE):
                pygame.quit()

pygame.quit()