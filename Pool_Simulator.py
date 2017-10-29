# pool simulator


import random
from tkinter import *

WIDTH = 1000
HEIGHT = 700
POOL_BORDER_WIDTH = WIDTH/20
POOL_BORDER_HEIGHT = HEIGHT/20

class Dot(object):
    dotCount = 0
    dirs = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    dirNums = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]

    def __init__(self, x, y):
        Dot.dotCount += 1
        self.x = x
        self.y = y
        self.r = 15
        self.fill = "yellow"
        self.isDrowning = False
        self.dir = random.randint(0,7) # Team blopit is FIRE & INCLUSIVE TO ALL GENDERS, RACES, SEXUALITIES, SCPECIES and ABILITIES <3
        # goes from 0 to 6
        # 0 Non-Drowner floating
        # 1 Non-Drowner Submerged
        # 2 Drowner Frowner
        # 3 Drowner Screamer
        # 4 Drowner Line Mouth
        # 5 Inverted  Drowner Frowner
        # 6 Inverted Drowner Screamer
        # 7 Inverted Drowner Line Mouth

        # 2 & 3 are Stable, 2-7 are Variable
        self.expression = 0

    def containsPoint(self, x, y):
        d = ((self.x - x)**2 + (self.y - y)**2)**0.5
        return (d <= self.r)

    def draw(self, canvas):
        leftX = self.x-self.r
        rightX = self.x+self.r
        topY = self.y-self.r
        bottomY = self.y+self.r
        bodyWidth = self.r * 2
        #make above the eyes
        submergeY = topY + self.r/3 # y coordinte of water line when submerged
        floatY = bottomY - self.r/3 #y coordinte of water line when floating

        #create body
        canvas.create_oval(leftX, topY,
                           rightX, bottomY,
                           fill=self.fill)
        #create left eye
        canvas.create_oval(leftX+6, topY+6,
                           leftX , bottomY-18,
                           fill=self.fill)
        #create right eye
        canvas.create_oval(leftX+12, topY+6,
                           rightX-10, bottomY-18,
                           fill=self.fill)
        # create mouth :*
        canvas.create_arc(leftX + 5, self.y + self.r/4, rightX - 5, self.y + 4 * self.r/6, start=180,
                    extent=180, outline="black", fill=None, width=.5)


    def onTimerFired(self, data):
        #check for pool border COLLISIONS
        # Need to check for corner collisions!!!
        collidedRight = self.x + self.r >= WIDTH - POOL_BORDER_WIDTH
        collidedLeft = self.x - self.r <= POOL_BORDER_WIDTH
        collidedTop = self.y - self.r <= POOL_BORDER_HEIGHT
        collidedBottom = self.y + self.r >= HEIGHT - POOL_BORDER_HEIGHT

        # DO ALL COLLISION CHECKS!!!!

        if(collidedRight and not (collidedTop or collidedBottom)): # COLLIDED with right Border
            self.dir = random.randint(5, 7)

#        elif(collidedRight and collidedBottom)


        #CHECK SWIMMER COLLISIONS


class MovingDot(Dot):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.speed = 2 # default initial speed

    def onTimerFired(self, data):
        #moves to the right
        #check for direction and modify x and y coords accordingly
        self.x += self.speed
        if (self.x > data.width):
            self.x = 0

class drowningDot(MovingDot):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.speed = 0
        self.flashCounter = 0
        self.showFlash = True

    def onTimerFired(self, data):
        super().onTimerFired(data)
        self.flashCounter += 1
        if (self.flashCounter == 5):
            self.flashCounter = 0
            self.showFlash = not self.showFlash

    def draw(self, canvas):
        canvas.create_rectangle(self.x-self.r, self.y-self.r,
                               self.x+self.r, self.y+self.r,
                               fill="lightGray")
        super().draw(canvas)

def init(data):
    data.dots = [ ]
    i = 0
    #cR is the circle radius
    cR = 25
    numPatrons = 20
    while (i < numPatrons):
        xCord = random.randint(50+cR,data.width-50-cR)
        yCord = random.randint(50+cR,data.height-50-cR)
        data.dots.append(MovingDot(xCord, yCord))
        i = i + 1

def mousePressed(event, data):
    for dot in reversed(data.dots):
        if (dot.containsPoint(event.x, event.y)):
            #saved or false alarm!!
            return


def redrawAll(canvas, data):
    for dot in data.dots:
        dot.draw(canvas)
    #canvas.create_text(data.width/2, 10, text="%d Dots" % Dot.dotCount)

def keyPressed(event, data):
    pass

def timerFired(data):
    for dot in data.dots:
        dot.onTimerFired(data)

####################################
# use the run function as-is
####################################

def run(width, height):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        #Draw pool background
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='NavajoWhite2', width=0)
        #Draw Pool water
        canvas.create_rectangle(POOL_BORDER_WIDTH, POOL_BORDER_HEIGHT, data.width - POOL_BORDER_WIDTH, data.height - POOL_BORDER_HEIGHT,
                                fill='DeepSkyBlue2', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(WIDTH, HEIGHT)