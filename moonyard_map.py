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

class Obstacle:
    def __init__(self, cx, cy, size, color, idnum, shape):
        self.cx = cx
        self.cy = cy
        self.size = size
        self.color = color
        self.idnum = idnum
        self.shape = shape
    
    def get_cx(self):
        return self.cx
    
    def change_cx(self, dif):
        self.cx += dif
    
    def get_cy(self):
        return self.cy
    
    def change_cy(self, dif):
        self.cy += dif

    def get_size(self):
        return self.size
    
    def change_size(self, dif):
        self.size += dif

    def get_color(self):
        return self.color
    
    def inc_color(self):
        if(self.color == green):
            self.color = yellow            
        elif(self.color == yellow):
            self.color = red
        elif(self.color == red):
            self.color = green

    def get_idnum(self):
        return self.idnum

    def get_shape(self):
        return self.shape

    def inc_shape(self):
        if(self.shape == "circle"):
            self.shape = "square"            
        elif(self.shape == "square"):
            self.shape = "triangle"
        elif(self.shape == "triangle"):
            self.shape = "circle"

    def draw(self, screen):
        if(self.cx >= -self.size and self.cy >= -self.size): 
            if(self.shape == "circle"):
                pygame.draw.circle(screen,self.color,(self.cx, self.cy), self.size)
                font = pygame.font.Font(None,30)
                num = font.render(str(self.idnum), True, (0,0,0))
                screen.blit(num, (self.cx-5, self.cy-10))
            if(self.shape == "square"):
                pygame.draw.rect(screen, self.color, pygame.Rect(self.cx - self.size, self.cy - self.size, 2*self.size, 2*self.size))
                font = pygame.font.Font(None,30)
                num = font.render(str(self.idnum), True, (0,0,0))
                screen.blit(num, (self.cx-5, self.cy-10))
            if(self.shape == "triangle"):
                pygame.draw.polygon(screen, self.color, ((self.cx , self.cy - self.size ), (self.cx - self.size, self.cy + self.size), (self.cx + self.size, self.cy + self.size)))
                font = pygame.font.Font(None,30)
                num = font.render(str(self.idnum), True, (0,0,0))
                screen.blit(num, (self.cx - 5, self.cy))
        

        
    
pygame.init()
#size = (pygame.display.Info().current_w,pygame.display.Info().current_h)
size = (1920,1080)
step = 40
#size = (2560,1440)
screen = pygame.display.set_mode(size, pygame.RESIZABLE)
irisCoords = [screen.get_width()/2, screen.get_height()/2, 120, 80]
pygame.display.set_caption("MoonYard Top-Down")
moon = pygame.Color(255,255,255)
red = pygame.Color(220,80,50)
blue = pygame.Color(50,220,220)
green = pygame.Color(50,180,100)
darkblue = pygame.Color(60,60,185)
purple = pygame.Color(140,50,180)
pink = pygame.Color(250,120,200)
yellow = pygame.Color(230, 200, 70)
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
path_mode = False
path_number = 0
path_point_selected = False
cur_path_point = (0, 0)
paths = []
path_colors = (red, blue, darkblue, purple, pink)
for i in range(5):
    paths.append([])


def getPos():
    pos = pygame.mouse.get_pos()
    return pos

#0 cx, 1 cy, 2 size, 3 color, 4 idnum, 5 shape

def addPoi():
    pos = getPos()
    num = -1;
    for i in range(1, len(loc), 1):
        next = True
        for p in loc:
            if(p.get_idnum() == i):
                next = False
                break
        if(next):
            num = i
            break
    if(num == -1):
        largest = 0
        for p in loc:
            if(p.get_idnum() > largest):
                largest = p.get_idnum()
        num = largest + 1

    loc.append(Obstacle(pos[0], pos[1], int(radius*(my_size/1.25)),green, num, "circle"))

def redrawPoi():
    for p in loc:
        if(p.get_cx() >= -p.get_size() and p.get_cy() >= -p.get_size()):    
            p.draw(screen)

def addCur(x,y,r):
    if(not cur == None):
        pygame.draw.circle(screen,green,(x,y),r+10)

def redrawCur():
    if(not cur == None and poi_selected == True):
        for p in loc:
            if(p.get_cx() == cur[0] and p.get_cy() == cur[1]):
                pygame.draw.line(screen,p.get_color(),(irisCoords[0],irisCoords[1]),(p.get_cx(),p.get_cy()),3)

def addPathPoint():
    pos = getPos()
    pygame.draw.circle(screen, path_colors[path_number], pos, 5)
    paths[path_number].append(pos)

def redrawPathPoints():
    i = 0
    for path in paths:
        prev = None
        for point in path:
            pygame.draw.circle(screen, path_colors[i], point, 5)
            if prev:
                pygame.draw.line(screen, path_colors[i], prev, point, 3)
            prev = point
        i += 1

def redrawCurPathPoint():
    i = cur_path_point[0]
    j = cur_path_point[1]
    if(path_point_selected):
        pygame.draw.circle(screen, (255, 255, 255), paths[i][j], 5, 2)

def redrawIris():
    surf =  pygame.Surface((120, 80))
    surf.fill(blue)
    pygame.draw.rect(surf, (50, 50, 50), pygame.Rect(100, 39, 15, 3))
    pygame.draw.rect(surf, (50, 50, 50), pygame.Rect(58, 38, 4, 4))
    pygame.draw.rect(surf, (255,0,0), pygame.Rect(15, 15, irisCoords[2] - 30, irisCoords[3] - 30))
    
    #set a color key for blitting
    surf.set_colorkey((255, 0, 0))

    blittedRect = pygame.Rect(irisCoords[0] - irisCoords[2]//2, irisCoords[1] - irisCoords[3]//2, irisCoords[2], irisCoords[3])
    oldCenter = blittedRect.center
    rotatedSurf =  pygame.transform.rotate(surf, offset[2])
    rotRect = rotatedSurf.get_rect()
    rotRect.center = oldCenter
    offset[0] = (oldCenter[0] - screenCen[0] - screenPos[0])
    offset[1] = (oldCenter[1] - screenCen[1] - screenPos[1])

    pygame.draw.circle(screen, blue, rotRect.center, 72, 2)
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
                pygame.draw.line(screen, (50, 50, 50), p5, p6, 3)
                pygame.draw.line(screen, (50, 50, 50), p3, p4, 3)
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
                pygame.draw.line(screen, (50, 50, 50), p5, p6, 3)
                pygame.draw.line(screen, (50, 50, 50), p3, p4, 3)
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
                pygame.draw.line(screen, (50, 50, 50), p5, p6, 3)
                pygame.draw.line(screen, (50, 50, 50), p3, p4, 3)
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
                pygame.draw.line(screen, (50, 50, 50), p5, p6, 3)
                pygame.draw.line(screen, (50, 50, 50), p3, p4, 3)
            else:
                pygame.draw.line(screen, (100, 100, 100), p5, p6, 2)
                pygame.draw.line(screen, (100, 100, 100), p3, p4, 2)
        
        


def redrawAtlas():
    pygame.draw.rect(screen, (255,255,255), pygame.Rect(0, 0, 300, 30))
    font = pygame.font.Font(None,40)
    text = font.render(f'X: {offset[0]//4} Y: {offset[1]//4} A: {offset[2]}',False,(0,0,0))
    screen.blit(text, (0,0))

def redrawDist():
    for p in loc:
        pygame.draw.line(screen,p.get_color(),(irisCoords[0],irisCoords[1]),(p.get_cx(),p.get_cy()),3)

def resizeScreen():
    #screen = pygame.display.set_mode((screen.get_width(), screen.get_height()), pygame.RESIZABLE)
    pass

def redrawAll():
    offset[2] = offset[2] % 360
    resizeScreen()
    screen.fill(moon)
    redrawGrid()
    redrawCur()
    redrawPoi()
    redrawPathPoints()
    redrawCurPathPoint()
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
            if(event.button == 1 and not path_mode):
                poi_selected = False
                dc = False
                for i in range(len(loc)):
                    if((x > (loc[i].get_cx() + loc[i].get_size()) or x < (loc[i].get_cx() - loc[i].get_size())) or (y > (loc[i].get_cy() + loc[i].get_size()) or y < (loc[i].get_cy() - loc[i].get_size()))):
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
            elif(event.button == 1):
                path_selected = True
                addPathPoint()
                cur_path_point = (path_number, len(paths[path_number]) - 1)
                path_point_selected = True
                pygame.display.update
            elif(event.button == 3 and not path_mode):
                poi_selected = False
                for i in range(len(loc)):
                    if((x < (loc[i].get_cx() + loc[i].get_size()) and x > (loc[i].get_cx() - loc[i].get_size())) and (y < (loc[i].get_cy() + loc[i].get_size()) and y > (loc[i].get_cy() - loc[i].get_size()))):
                        cur = [loc[i].get_cx(),loc[i].get_cy(),loc[i].get_size(),green]
                        poi_selected = True
                    else:
                        pass
                if(poi_selected):
                    addCur(cur[0],cur[1],cur[2])
                    pygame.display.update()
                else:
                    cur = None
            elif(event.button == 3):
                path_point_selected = False
                for i in range (len(paths)):
                    for j in range (len(paths[i])):
                        if ((x < paths[i][j][0] + 5 and x < paths[i][j][0]) - 5 and (y < paths[i][j][1] + 5 and y > paths[i][j][1] - 5)):
                            cur_path_point = (i, j)
                            path_point_selected = True
            if(event.button == 4 and poi_selected):
                i=0
                for p in loc:
                    if(p.get_cx() == cur[0] and p.get_cy() == cur[1]):
                        loc[i].change_size(5)
                        cur[2] += 5
                    i+=1
                pygame.display.update()  
            if(event.button == 5 and poi_selected):
                i=0
                for p in loc:
                    if(p.get_cx() == cur[0] and p.get_cy() == cur[1] and loc[i].get_size() > 5):
                        loc[i].change_size(-5)
                        cur[2] -= 5
                    i+=1
                pygame.display.update()
        if(event.type == pygame.KEYDOWN):
            if(event.key == pygame.K_LEFT and poi_selected):
                for p in loc:
                    if(p.get_cx() == cur[0] and p.get_cy() == cur[1]):
                        p.change_cx(-int(math.cos(offset[2] * math.pi / 180) * MoonYard_Scale))
                        p.change_cy(int(math.sin(offset[2] * math.pi / 180) * MoonYard_Scale))
                        if(cur != None):
                            cur[0] -= int(math.cos(offset[2] * math.pi / 180) * MoonYard_Scale)
                            cur[1] += int(math.sin(offset[2] * math.pi / 180) * MoonYard_Scale)
            elif(event.key == pygame.K_LEFT and path_point_selected):
                i = cur_path_point[0]
                j = cur_path_point[1]
                old_x = paths[i][j][0]
                old_y = paths[i][j][1]
                new_x = old_x - int(math.cos(offset[2] * math.pi / 180) * MoonYard_Scale)
                new_y = old_y + int(math.sin(offset[2] * math.pi / 180) * MoonYard_Scale)
                paths[i][j] = (new_x, new_y)
            elif(event.key == pygame.K_LEFT):
                offset[2] += angle

            if(event.key == pygame.K_RIGHT and poi_selected):
                for p in loc:
                    if(p.get_cx() == cur[0] and p.get_cy() == cur[1]):
                        p.change_cx(int(math.cos(offset[2] * math.pi / 180) * MoonYard_Scale))
                        p.change_cy(-int(math.sin(offset[2] * math.pi / 180) * MoonYard_Scale))
                        if(cur != None):
                            cur[0] += int(math.cos(offset[2] * math.pi / 180) * MoonYard_Scale)
                            cur[1] -= int(math.sin(offset[2] * math.pi / 180) * MoonYard_Scale)
            elif(event.key == pygame.K_RIGHT and path_point_selected):
                i = cur_path_point[0]
                j = cur_path_point[1]
                old_x = paths[i][j][0]
                old_y = paths[i][j][1]
                new_x = old_x + int(math.cos(offset[2] * math.pi / 180) * MoonYard_Scale)
                new_y = old_y - int(math.sin(offset[2] * math.pi / 180) * MoonYard_Scale)
                paths[i][j] = (new_x, new_y)
            elif(event.key == pygame.K_RIGHT):
                offset[2] -= angle

            if(event.key == pygame.K_UP and poi_selected):
                for p in loc:
                    if(p.get_cx() == cur[0] and p.get_cy() == cur[1]):
                        p.change_cx(-int(math.sin(offset[2] * math.pi / 180) * MoonYard_Scale))
                        p.change_cy(-int(math.cos(offset[2] * math.pi / 180) * MoonYard_Scale))
                        if(cur != None):
                            cur[0] -= int(math.sin(offset[2] * math.pi / 180) * MoonYard_Scale)
                            cur[1] -= int(math.cos(offset[2] * math.pi / 180) * MoonYard_Scale)
            elif(event.key == pygame.K_UP and path_point_selected):
                i = cur_path_point[0]
                j = cur_path_point[1]
                old_x = paths[i][j][0]
                old_y = paths[i][j][1]
                new_x = old_x - int(math.sin(offset[2] * math.pi / 180) * MoonYard_Scale)
                new_y = old_y - int(math.cos(offset[2] * math.pi / 180) * MoonYard_Scale)
                paths[i][j] = (new_x, new_y)
            elif(event.key == pygame.K_UP):
                irisCoords[0] += int(math.cos(offset[2] * math.pi / 180) * MoonYard_Scale)
                irisCoords[1] -= int(math.sin(offset[2] * math.pi / 180) * MoonYard_Scale)

            if(event.key == pygame.K_DOWN and poi_selected):
                for p in loc:
                    if(p.get_cx() == cur[0] and p.get_cy() == cur[1]):
                        p.change_cx(int(math.sin(offset[2] * math.pi / 180) * MoonYard_Scale))
                        p.change_cy(int(math.cos(offset[2] * math.pi / 180) * MoonYard_Scale))
                        if(cur != None):
                            cur[0] += int(math.sin(offset[2] * math.pi / 180) * MoonYard_Scale)
                            cur[1] += int(math.cos(offset[2] * math.pi / 180) * MoonYard_Scale)
            elif(event.key == pygame.K_DOWN and path_point_selected):
                i = cur_path_point[0]
                j = cur_path_point[1]
                old_x = paths[i][j][0]
                old_y = paths[i][j][1]
                new_x = old_x + int(math.sin(offset[2] * math.pi / 180) * MoonYard_Scale)
                new_y = old_y + int(math.cos(offset[2] * math.pi / 180) * MoonYard_Scale)
                paths[i][j] = (new_x, new_y)
            elif(event.key == pygame.K_DOWN):
                irisCoords[0] -= int(math.cos(offset[2] * math.pi / 180) * MoonYard_Scale)
                irisCoords[1] += int(math.sin(offset[2] * math.pi / 180) * MoonYard_Scale)

            if(event.key == pygame.K_a):
                for p in loc:
                    p.change_cx(-MoonYard_Scale)
                    cur[0] -= MoonYard_Scale
                for i in range(len(paths)):
                    for j in range(len(paths[i])):
                        paths[i][j] = (paths[i][j][0] - MoonYard_Scale, paths[i][j][1])
                irisCoords[0] -= MoonYard_Scale
                screenPos[0] -= MoonYard_Scale
            if(event.key == pygame.K_d):
                for p in loc:
                    p.change_cx(MoonYard_Scale)
                    cur[0] += MoonYard_Scale
                for i in range(len(paths)):
                    for j in range(len(paths[i])):
                        paths[i][j] = (paths[i][j][0] + MoonYard_Scale, paths[i][j][1])
                irisCoords[0] += MoonYard_Scale
                screenPos[0] += MoonYard_Scale
            if(event.key == pygame.K_s):
                for p in loc:
                    p.change_cy(MoonYard_Scale)
                    cur[1] += MoonYard_Scale
                for i in range(len(paths)):
                    for j in range(len(paths[i])):
                        paths[i][j] = (paths[i][j][0], paths[i][j][1] + MoonYard_Scale)
                irisCoords[1] += MoonYard_Scale
                screenPos[1] += MoonYard_Scale
            if(event.key == pygame.K_w):
                for p in loc:
                    p.change_cy(-MoonYard_Scale)
                    cur[1] -= MoonYard_Scale
                for i in range(len(paths)):
                    for j in range(len(paths[i])):
                        paths[i][j] = (paths[i][j][0], paths[i][j][1] - MoonYard_Scale)
                irisCoords[1] -= MoonYard_Scale
                screenPos[1] -= MoonYard_Scale  

            if(event.key == pygame.K_k and poi_selected == True):
                for p in loc:
                    if(p.get_cx() == cur[0] and p.get_cy() == cur[1]):
                        p.inc_shape()         

            # if(event.key == pygame.K_r and poi_selected == True):
            #     for p in loc:
            #         if(p[0] == cur[0] and p[1] == cur[1]):
            #             p[3] = red
            # if(event.key == pygame.K_g and poi_selected == True):
            #     for p in loc:
            #         if(p[0] == cur[0] and p[1] == cur[1]):
            #             p[3] = green
            # if(event.key == pygame.K_y and poi_selected == True):
            #     for p in loc:
            #         if(p[0] == cur[0] and p[1] == cur[1]):
            #             p[3] = yellow
            if(event.key == pygame.K_c and poi_selected == True):
                for p in loc:
                    if(p.get_cx() == cur[0] and p.get_cy() == cur[1]):
                        p.inc_color()
            # if(event.key == pygame.K_x and poi_selected == True):
            #     for p in loc:
            #         if(p[0] == cur[0] and p[1] == cur[1]):
            #             if(p[3] == red):
            #                 p[3] = pink
            #             elif(p[3] == pink):
            #                 p[3] = purple
            #             elif(p[3] == purple):
            #                 p[3] = darkblue
            #             elif(p[3] == darkblue): 
            #                 p[3] = blue
            if(event.key == pygame.K_DELETE and poi_selected == True):
                for p in loc:
                    if(p.get_cx() == cur[0] and p.get_cy() == cur[1]):
                        temp = p
                        loc.remove(p)
                        poi_selected = False
                        print("Removed POI")
            elif(event.key == pygame.K_DELETE and path_point_selected):
                i = cur_path_point[0]
                j = cur_path_point[1]
                del(paths[i][j])
                path_point_selected = False

            if(event.key == pygame.K_p):
                if path_mode:
                    path_mode = False
                    path_point_selected = False
                else:
                    path_mode = True
                    poi_selected = False
                    cur = None

            if(event.key == pygame.K_1 and path_mode):
                path_number = 0
            if(event.key == pygame.K_2 and path_mode):
                path_number = 1
            if(event.key == pygame.K_3 and path_mode):
                path_number = 2
            if(event.key == pygame.K_4 and path_mode):
                path_number = 3
            if(event.key == pygame.K_5 and path_mode):
                path_number = 4

            if(event.key == pygame.K_ESCAPE):
                pygame.quit()

            clock.tick(30)

pygame.quit()