# pool simulator


import random
from tkinter import *

WIDTH = 1200
HEIGHT = 700
POOL_BORDER_WIDTH = WIDTH/20
POOL_BORDER_HEIGHT = HEIGHT/20
NUM_SWIMMERS = 20

MIN_SPEED = 1
MAX_SPEED = 5

# Team blopit is FIRE & INCLUSIVE TO ALL GENDERS, RACES, SEXUALITIES, SCPECIES and ABILITIES <3

def getNewSpeed():
    return random.randint(MIN_SPEED, MAX_SPEED)

####################################
# CLASSES
####################################


class MovingDot(object):
    dotCount = 0
    dirs = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    dirNums = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]
    maxSpeed = 5
    minSpeed = 1

    def __init__(self, x, y):
        MovingDot.dotCount += 1
        #PLACEMENT
        self.x = x
        self.y = y
        self.r = 15

        #MOTION
        self.speed =  getNewSpeed()
        self.dir = random.randint(0,7) # random direction 
        self.moveX = MovingDot.dirNums[self.dir][0] * self.speed
        self.moveY = MovingDot.dirNums[self.dir][1] * self.speed

        #APPEARANCE
        self.bodyFill = "yellow"
        self.featureFill = "#4f5104"
        # goes from 0 to 7, 2 & 3 are Stable, 2-7 are Variable
        # 0 Non-Drowner floating
        # 1 Non-Drowner Submerged
        # 2 Drowner Frowner
        # 3 Drowner Screamer
        # 4 Drowner Line Mouth
        # 5 Inverted Drowner Frowner
        # 6 Inverted Drowner Screamer
        # 7 Inverted Drowner Line Mouth
        self.expression = 0

        #STATE
        self.isDrowning = False
        

    def containsPoint(self, x, y):
        d = ((self.x - x)**2 + (self.y - y)**2)**0.5
        return (d <= self.r)

    def draw(self, canvas): 
        leftX = self.x - self.r
        rightX = self.x + self.r
        topY = self.y - self.r
        bottomY = self.y + self.r

        bodyWidth = self.r * 2
        eyeWidthOffset = bodyWidth/5 # eyes take up a fifth of the face, and are a fifth from the edges

        #make above the eyes
        submergeY = topY + self.r/3 # y coordinte of water line when submerged
        floatY = bottomY - self.r/3 #y coordinte of water line when floating

        #create body
        canvas.create_oval(leftX,topY,
                            rightX, bottomY,
                            fill=self.bodyFill)
        #create left eye 
        canvas.create_oval(leftX + eyeWidthOffset, topY + bodyWidth/4,
                            leftX + 2 * eyeWidthOffset, topY + bodyWidth/2,
                            fill=self.featureFill)
        #create right eye
        canvas.create_oval(rightX - eyeWidthOffset, topY + bodyWidth/4,
                            rightX - 2 * eyeWidthOffset, topY + bodyWidth/2,
                            fill=self.featureFill)
        # create mouth :*
        canvas.create_arc(leftX + eyeWidthOffset, self.y + self.r/4, 
                            rightX - eyeWidthOffset, self.y + 4 * self.r/6, 
                            start=180, extent=180, width=.5,
                            outline="black", fill=self.featureFill)


    def onTimerFired(self, data):

        self.checkWallCollisions()
        self.checkSwimmerCollisions(data)

        self.move()


    def move(self):
        #check for direction and modify x and y coords accordingly
        self.x += self.moveX
        self.y += self.moveY
        

    def updateDir(self, newDir):
        self.dir = newDir
        self.moveX = MovingDot.dirNums[self.dir][0] * self.speed
        self.moveY = MovingDot.dirNums[self.dir][1] * self.speed


    def checkWallCollisions(self):
        collidedRight = self.x + self.r >= WIDTH - POOL_BORDER_WIDTH
        collidedLeft = self.x - self.r <= POOL_BORDER_WIDTH
        collidedTop = self.y - self.r <= POOL_BORDER_HEIGHT
        collidedBottom = self.y + self.r >= HEIGHT - POOL_BORDER_HEIGHT

        if(not (collidedLeft or collidedRight) and collidedTop): # COLLIDED with top
            newDir = random.randint(3, 5)
            self.updateDir(newDir)

        elif(collidedRight and collidedTop): # COLLIDED with top right
            newDir = random.randint(4, 6)
            self.updateDir(newDir)

        elif(collidedRight and not (collidedTop or collidedBottom)): # COLLIDED with right 
            newDir = random.randint(5, 7)
            self.updateDir(newDir)

        elif(collidedRight and collidedBottom): # COLLIDED with bottom right 
            newDir= random.choice([6, 7, 0])
            self.updateDir(newDir)

        elif(not (collidedRight or collidedLeft) and collidedBottom): # COLLIDED with bottom 
            newDir = random.choice([7, 0, 1])
            self.updateDir(newDir)

        elif(collidedLeft and collidedBottom): # COLLIDED with bottom left
            newDir = random.randint(0, 2)
            self.updateDir(newDir) 

        elif(collidedLeft and not (collidedTop or collidedBottom)): # COLLIDED with left
            newDir = random.randint(1, 3)
            self.updateDir(newDir)

        elif(collidedLeft and collidedBottom): # COLLIDED with top left
            newDir = random.randint(2, 4)
            self.updateDir(newDir)


    def checkSwimmerCollisions(self, data): # TODO: MAKE SURE SWIMMER NOT COLLIDING WITH WALL TOO
        for other in data.dots:
            if(other is self): # always colliding with self
                break

            xDist = abs(self.x - other.x)
            yDist = abs(self.y - other.y)
            collided = (xDist**2 + yDist**2)**0.5 < (self.r * 2) #Pythagoras, checks that radii are touching, add 2 for legroom

            if (collided): #collided N
                oppositeDirSelf = (self.dir + 4) % 8 
                self.updateDir(oppositeDirSelf)
                self.speed = getNewSpeed()

                oppositeDirOther = (other.dir + 4) % 8
                other.updateDir(oppositeDirOther)   
                other.speed = getNewSpeed()


        



####################################
# MAIN FUNCTIONS
####################################
def init(data):
    data.dots = [ ]
    i = 0
    #cR is the circle radius
    cR = 25
    numPatrons = NUM_SWIMMERS
    while (i < numPatrons):
        xCord = random.randint(50+cR,data.width-50-cR)
        yCord = random.randint(50+cR,data.height-50-cR)
        data.dots.append(MovingDot(xCord, yCord))
        i = i + 1
def mousePressed(event, data):
    for dot in reversed(data.dots):
        if (dot.containsPoint(event.x, event.y)):
            #if (dot.isDrowning):
                #correct
            #else
                #incorrect!
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
# RUN FUNCTION
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
    data.timerDelay = 33 # milliseconds
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