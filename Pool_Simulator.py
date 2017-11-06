# pool simulator
# Special thanks to Mark Stehlik and David Kosbie <3 
# for teaching Blopit how to steal their code and enhance it w engineering chops

import random
import time
import csv
from tkinter import *


WIDTH = 1200
HEIGHT = 700
POOL_BORDER_WIDTH = WIDTH/20
POOL_BORDER_HEIGHT = HEIGHT/20
NUM_SWIMMERS = 40

MIN_SPEED = 1
MAX_SPEED = 3

IS_VARIABLE_CONDITION = True


SIMULATION_START = time.time()  # --> number of miliseconds that the simulation has been running.
SIMULATION_END = 25 # should be 1260, 21 minutes. 3 init measure, 15 condition, 3 end measure.


INITIAL_MEASURE_END = 180 # should be 180 - 3 Minutes
END_MEASURE_START = 1080 # should be 1080 - 18 Minutes 

PARTICIPANT_ID = 0
DATA_OUT_TO = ("VigilanceDecrement_%d.csv" % PARTICIPANT_ID)


#[30, 60, 100, 250, 270] # in seconds

DROWNER_TIMES = [5, 10, 20] # in seconds
DROWNER_TIMES.sort()

NUM_DROWNERS = len(DROWNER_TIMES)


# Team blopit is FIRE & INCLUSIVE TO ALL GENDERS, RACES, SEXUALITIES, SCPECIES and ABILITIES <3


def getNewSpeed():
    return random.randint(MIN_SPEED, MAX_SPEED)

def timeIntoExperiment():
    return time.time() - SIMULATION_START

####################################
# MOVING DOT CLASS
####################################


class MovingDot(object):
    dotCount = 0
    dirs = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    dirNums = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]
    submergedColor = '#4b90cc'

    def __init__(self, x, y):
        MovingDot.dotCount += 1
        #PLACEMENT
        self.x = x
        self.y = y
        self.r = 10

        #MOTION
        self.speed = getNewSpeed()
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
        self.isColliding = False
        self.timeStartedDrowning = None
        self.timeStartedSubmerge = None
        

    def containsPoint(self, x, y):
        d = ((self.x - x)**2 + (self.y - y)**2)**0.5
        return (d <= self.r)

    def drown(self, data):
        #if stable--> chose either 2 or 3
        self.isDrowning = True
        data.isDuringDrowning = True

        if (IS_VARIABLE_CONDITION):
            self.expression = random.randint(2,7)
        else:
            self.expression = random.randint(2,3)
        self.timeStartedDrowning = timeIntoExperiment()

        # else choose from 2 - 7
        #### ENHANCEMENT: 5 seconds under water, no face change
        # flip isDrowning to True

    def unDrown(self, data):
        self.isDrowning = False
        data.isDuringDrowning = False

        self.expression = 0
        self.timeStartedDrowning = None

    def submerge(self):
        self.expression = 1
        self.timeStartedSubmerge = timeIntoExperiment()

    def unSubmerge(self):
        self.expression = 0
        self.timeStartedSubmerge = None


    def draw(self, canvas): 
        leftX = self.x - self.r
        rightX = self.x + self.r
        topY = self.y - self.r
        bottomY = self.y + self.r

        bodyWidth = self.r * 2

        eyeWidthOffset = bodyWidth/5 # eyes take up a fifth of the face, and are a fifth from the edges
        isInverted = False
        
        # 0 Non-Drowner floating
        # 1 Non-Drowner Submerged
        # 2 Drowner Frowner
        # 3 Drowner Screamer
        # 4 Drowner Line Mouth 
        # 5 Inverted Drowner Frowner
        # 6 Inverted Drowner Screamer
        # 7 Inverted Drowner Line Mouth

        # Check expression, draw face based on that

        #create body
        canvas.create_oval(leftX,topY,
                            rightX, bottomY,
                            fill=self.bodyFill)

        #### is submerged? --> Draw WaterLine Above

        if (1 <= self.expression):
            self.drawWaterline(canvas,leftX, rightX, topY, bottomY, True)
        else:
            self.drawWaterline(canvas, leftX, rightX, topY, bottomY, False)



        #### is inverted? --> Draw eyes below and mouth Above
        if (5 <= self.expression):
            isInverted = True
        self.drawEyes(canvas, leftX, rightX, topY, bottomY, isInverted)
         

        if (self.expression == 2):
            #frown
            self.drawMouth(canvas, leftX, rightX, topY, bottomY, isInverted, 'arcUp')

        elif (self.expression == 3 or self.expression == 6):
            #scream
            self.drawMouth(canvas, leftX, rightX, topY, bottomY, isInverted, 'ellipse')
    

        elif (self.expression == 4 or self.expression == 7):
            #line mouth
            self.drawMouth(canvas, leftX, rightX, topY, bottomY, isInverted, 'line')
        else:
            #smile
            self.drawMouth(canvas, leftX, rightX, topY, bottomY, isInverted, 'arcDown')


        
    def drawWaterline(self, canvas, leftX, rightX, topY, bottomY, isSubmerged):
        # if submerged then draw waterline near top, else, near bottom
        if(isSubmerged):
            waterlineY = topY + self.r # y coordinte of water line when submerged  
        else: waterlineY = bottomY - self.r/4 # y coordinte of water line when floating



        canvas.create_rectangle(leftX, waterlineY, 
                                rightX, bottomY, 
                            outline=MovingDot.submergedColor, fill=MovingDot.submergedColor)
        #redraw face outline
        canvas.create_oval(leftX,topY,
                            rightX, bottomY,
                            fill="")



    def drawEyes(self, canvas, leftX, rightX, topY, bottomY, isInverted):
        # if inverted then draw eyes near bottom, else, near top

        bodyWidth = self.r * 2
        eyeWidthOffset = bodyWidth/5 # eyes take up a fifth of the face, and are a fifth from the edges
        eyeHeight = bodyWidth/4

        if(isInverted):
            eyeY = bottomY - bodyWidth/2
        else:
            eyeY = topY + bodyWidth/4

        #create left eye 
        canvas.create_oval(leftX + eyeWidthOffset, eyeY,
                            leftX + 2 * eyeWidthOffset, eyeY + eyeHeight,
                            fill=self.featureFill)
        #create right eye
        canvas.create_oval(rightX - eyeWidthOffset, eyeY,
                            rightX - 2 * eyeWidthOffset, eyeY + eyeHeight,
                            fill=self.featureFill)

    def drawMouth(self, canvas, leftX, rightX, topY, bottomY, isInverted, mouthType):
        # if inverted then draw mouth near top, else, near bottom

        # Draw shape based on mouth type
        # frown drawInvArc (2, 5) -- scream drawEllipse(3, 6) -- line mouth drawLine (4, 7)

        bodyWidth = self.r * 2
        mouthHeight = bodyWidth/4 
        eyeWidthOffset = bodyWidth/5 # TODO clean up repeated code: eyeWidthOffset and bodyWidth

        if(isInverted):
            mouthTopY = self.y - self.r/5 - mouthHeight
        else:
            mouthTopY = self.y + self.r/5

        # create mouth :*
        if(mouthType == 'arcDown'):
            canvas.create_arc(leftX + eyeWidthOffset, mouthTopY, 
                            rightX - eyeWidthOffset, mouthTopY + mouthHeight, 
                            start=180, extent=180, width=.5,
                            fill=self.featureFill)

        elif(mouthType == 'arcUp'):
            canvas.create_arc(leftX + eyeWidthOffset, mouthTopY, 
                            rightX - eyeWidthOffset, mouthTopY + mouthHeight, 
                            start=0, extent=180, width=.5,
                            fill=self.featureFill)

        elif(mouthType == 'ellipse'):
            canvas.create_oval(leftX + eyeWidthOffset, mouthTopY, 
                            rightX - eyeWidthOffset, mouthTopY + mouthHeight, 
                            fill=self.featureFill)

            
        elif(mouthType == 'line'):
            canvas.create_line(leftX + eyeWidthOffset, mouthTopY + mouthHeight/2, 
                                rightX - eyeWidthOffset, mouthTopY + mouthHeight/2,
                                width=mouthHeight, fill=self.featureFill)
 

    def onTimerFired(self, data):

        self.checkWallCollisions()
        self.checkSwimmerCollisions(data)

        if (not self.isDrowning):
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

        if (not (collidedLeft or collidedRight) and collidedTop): # COLLIDED with top
            newDir = random.randint(3, 5)
            self.updateDir(newDir)

        elif (collidedRight and collidedTop): # COLLIDED with top right
            newDir = random.randint(4, 6)
            self.updateDir(newDir)

        elif (collidedRight and not (collidedTop or collidedBottom)): # COLLIDED with right 
            newDir = random.randint(5, 7)
            self.updateDir(newDir)

        elif (collidedRight and collidedBottom): # COLLIDED with bottom right 
            newDir= random.choice([6, 7, 0])
            self.updateDir(newDir)

        elif (not (collidedRight or collidedLeft) and collidedBottom): # COLLIDED with bottom 
            newDir = random.choice([7, 0, 1])
            self.updateDir(newDir)

        elif (collidedLeft and collidedBottom): # COLLIDED with bottom left
            newDir = random.randint(0, 2)
            self.updateDir(newDir) 

        elif (collidedLeft and not (collidedTop or collidedBottom)): # COLLIDED with left
            newDir = random.randint(1, 3)
            self.updateDir(newDir)

        elif (collidedLeft and collidedBottom): # COLLIDED with top left
            newDir = random.randint(2, 4)
            self.updateDir(newDir)


    def checkSwimmerCollisions(self, data): # TODO: MAKE SURE SWIMMER NOT COLLIDING WITH WALL TOO
        for other in data.dots:
            if (other is self): # always colliding with self
                break

            xDist = abs(self.x - other.x)
            yDist = abs(self.y - other.y)
            collided = (xDist**2 + yDist**2)**0.5 < (self.r * 2) #Pythagoras, checks that radii are touching, add 2 for legroom

            if (collided): #collided N
                self.isColliding = True
                oppositeDirSelf = (self.dir + 4) % 8 
                self.updateDir(oppositeDirSelf)
                self.speed = getNewSpeed()

                oppositeDirOther = (other.dir + 4) % 8
                other.updateDir(oppositeDirOther)   
                other.speed = getNewSpeed()
                other.isColliding = True
            else:
                self.isColliding = False



        



########################################################################
#                           MAIN FUNCTIONS                             #
########################################################################

            #########################################

def init(data):
    data.drawGreenTick = False 
    data.drownerNum = 0
    data.startResponseDraw = 0
    data.responseDisplayDelay = 0.5
    data.greenTickColor = '#067c2d'
    data.drawRedX = False
    data.isDuringDrowning = False
    data.clickNum = 0
    data.isOver = False
    data.submergeTime = 4

    # [(time, clickDelay, swimmer.expression)...]
    data.correctClickDelays = [] #in seconds - difference between drown start and save

    # [(time, timePeriod, isCorrect, onSwimmer, isDuringDrowning, onDiver, clickDelay, swimmer.expression)...]
    # timePeriod = 'Initial', 'Condition', 'End'

    data.clickLog = [] # in seconds 

    data.dots = [ ]
    i = 0
    #cR is the circle radius
    offset = 25
    numPatrons = NUM_SWIMMERS
    while (i < numPatrons):
        xCord = random.randint(50+offset,data.width-50-offset)
        yCord = random.randint(50+offset,data.height-50-offset)
        data.dots.append(MovingDot(xCord, yCord))
        i = i + 1

def timeResponseDisplay(data, response):
    if(response == 'tick'):
        if(time.time() - data.startResponseDraw >= data.responseDisplayDelay and data.drawGreenTick):
            data.drawGreenTick = False

    elif(response == 'X'):
        if(time.time() - data.startResponseDraw >= data.responseDisplayDelay and data.drawRedX):
            data.drawRedX = False


def mousePressed(event, data):
    if(not data.isOver):
        swimmerClicked = False
        for dot in reversed(data.dots):
            if (dot.containsPoint(event.x, event.y)):
                swimmerClicked = True
                if (dot.isDrowning):
                    logClick(data, timeIntoExperiment(), True, swimmerClicked, dot) # correct
                    data.drawGreenTick = True
                    data.startResponseDraw = time.time()
                    dot.unDrown(data)

                else:
                    logClick(data, timeIntoExperiment(), False, swimmerClicked, dot) # incorrect onswimmer
                    data.drawRedX = True
                    data.startResponseDraw = time.time()
        if(not swimmerClicked):
            logClick(data, timeIntoExperiment(), False, swimmerClicked, None) # incorrect offswimmer
            data.drawRedX = True
            data.startResponseDraw = time.time()

    #log out-of-swimmer click
    #log whether current drowning or not.
    return

def logClick(data, time, isCorrect, onSwimmer, swimmer=None):
    #sanity Checks
    assert(onSwimmer == bool(swimmer))
    if(swimmer != None):
        assert(isinstance(swimmer,MovingDot)) 
    if(timeIntoExperiment() <= INITIAL_MEASURE_END):
        timePeriod = 'Initial'
    elif(timeIntoExperiment() >= END_MEASURE_START):
        timePeriod = 'End'
    else:
        timePeriod = 'Condition'

    clickDelay = None
    logExpression = None
    onDiver = (onSwimmer and not isCorrect and swimmer.expression == 1)
    xLoc = None
    yLoc = None

    if(swimmer != None):
        xLoc = swimmer.x 
        yLoc = swimmer.y
        logExpression = swimmer.expression

        if (isCorrect): 
            clickDelay = time - swimmer.timeStartedDrowning 
            data.correctClickDelays.append((time, clickDelay, logExpression))

    #(time, timePeriod, isCorrect, onSwimmer, isDuringDrowning, onDiver, clickDelay, swimmer.expression, swimmer.x, swimmer.y)
    data.clickLog.append((time, timePeriod, isCorrect, onSwimmer, data.isDuringDrowning, onDiver, 
                                                    clickDelay, logExpression, xLoc, yLoc))
    print("click: ", data.clickLog[data.clickNum])
    data.clickNum += 1
    print("Clicks so far = ", data.clickNum)

def redrawAll(canvas, data):
    for dot in data.dots:
        dot.draw(canvas)
    if(data.drawGreenTick):
        drawGreenTick(canvas, data)

    if(data.drawRedX):
        drawRedX(canvas, data)

    if(data.isOver):

        canvas.create_text(data.width/2, data.height/2, text="Its Over", font=("Arial", 200), fill="red")


def drawGreenTick(canvas, data):
    timeResponseDisplay(data, "tick")
    canvas.create_text(data.width/2, data.height/2, text="safe!", font=("Arial", 120), fill=data.greenTickColor)


def drawRedX(canvas, data):
    timeResponseDisplay(data,"X")
    canvas.create_text(data.width/2, data.height/2, text="X", font=("Arial", 200), fill="red")


def keyPressed(event, data):
    pass

def timerFired(data):
    #occasionally have some dots submerge.
    if(not data.isOver): 
        for dot in data.dots:
            dot.onTimerFired(data)
            if(dot.expression == 1 and timeIntoExperiment() - dot.timeStartedSubmerge >= data.submergeTime):
                dot.unSubmerge()


        checkToDrown(data)
        checkToSubmerge(data)

        if(SIMULATION_END <= timeIntoExperiment()):
            data.isOver = True
            printFinalData(data)
            writeToCSV(data.clickLog)

def checkToSubmerge(data):
    roll = random.randint(1, 300) # this is called 3 times per second, so we expect a drowner every 100 seconds on avg
    if(roll == 5):
        canSubmerge = list(filter(lambda x: not (x.isDrowning or x.isColliding), data.dots))
        random.choice(canSubmerge).submerge()

def checkToDrown(data):
    haveDrownersLeft = data.drownerNum < len(DROWNER_TIMES)
    if(haveDrownersLeft and timeIntoExperiment() >= DROWNER_TIMES[data.drownerNum]):
        #filter dots in a collision -- no colliders or already drowners
        canDrown = list(filter(lambda x: not (x.isDrowning or x.isColliding), data.dots))
        if(len(canDrown) > 0):
            print("drowned", data.drownerNum)
            random.choice(canDrown).drown(data)
            data.drownerNum += 1 # make sure it doesnt go beyond list len


def printFinalData(data):
    print("Total Click Nums= ", data.clickNum)
    print("All Click info : \n", data.clickLog)
    print("All Correct clicks: \n", data.correctClickDelays)

def writeToCSV(myClickList):
    # TODO: name the file according to the 'PARTICIPANT ID'
    with open(DATA_OUT_TO, 'w', newline='') as csvfile:
        fieldnames = ['time', 'timePeriod', 'isCorrect', 'onSwimmer', 'isDuringDrowning', 
                'onDiver', 'clickDelay', 'expression', 'swimmerX', 'swimmerY']

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect="excel")

        writer.writeheader()
        for click in myClickList:
            writer.writerow({'time': click[0], 
                            'timePeriod': click[1], 
                            'isCorrect': click[2], 
                            'onSwimmer': click[3], 
                            'isDuringDrowning': click[4], 
                            'onDiver': click[5], 
                            'clickDelay': click[6], 
                            'expression': click[7], 
                            'swimmerX': click[8], 
                            'swimmerY': click[9]})




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
                                fill='#48a3f2', width=0)
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