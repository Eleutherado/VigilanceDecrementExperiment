# pool simulator
# Special thanks to Mark Stehlik and David Kosbie <3 
# for teaching Blopit how to steal their code and enhance it w engineering chops

import random
import time
import csv
from tkinter import *


#WIDTH = 1200
#HEIGHT = 700
WIDTH = 1900
HEIGHT = 990

POOL_BORDER_WIDTH = WIDTH/20
POOL_BORDER_HEIGHT = HEIGHT/20
NUM_SWIMMERS = 50

MIN_SPEED = 0
MAX_SPEED = 2

IS_VARIABLE_CONDITION = False


PARTICIPANT_ID = random.randint(0, 99999)
DATA_OUT_TO = ("VigilanceDecrement_Infr_Sta_%d.csv" % PARTICIPANT_ID)




# Team blopit is FIRE & INCLUSIVE TO ALL GENDERS, RACES, SEXUALITIES, SCPECIES and ABILITIES <3


def getNewSpeed():
    return random.randint(MIN_SPEED, MAX_SPEED)

def timeIntoSimulation(data):
    if(data.mode == data.modes[3]): # in experiment
        return time.time() - data.experimentStart
    elif(data.mode == data.modes[1]): # in simulation
        return time.time() - data.trainingStart

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
        self.willDrown = False
        self.isSubmerged = False
        self.isDrowning = False
        self.isColliding = False
        self.timeStartedDrowning = None
        self.timeStartedSubmerge = None
        self.timeToDrown = None
        

    def containsPoint(self, x, y):
        d = ((self.x - x)**2 + (self.y - y)**2)**0.5
        return (d <= self.r)

    def drown(self, data):
        #if stable--> chose either 2 or 3

        self.isDrowning = True
        data.isDuringDrowning = True
        data.timeToDrown = None

        if (IS_VARIABLE_CONDITION):
            self.expression = random.randint(2,7)
        else:
            self.expression = random.randint(2,3)
        self.timeStartedDrowning = timeIntoSimulation(data)

        # else choose from 2 - 7
        #### ENHANCEMENT: 5 seconds under water, no face change
        # flip isDrowning to True

    def startDrown(self, data):
        # expression turns to 1
        # after 5 seconds, call drown
        self.willDrown = True
        self.expression = 1
        self.timeToDrown = timeIntoSimulation(data)

    def unDrown(self, data):
        self.isDrowning = False
        data.isDuringDrowning = False

        self.expression = 0
        self.timeStartedDrowning = None

    def submerge(self, data):
        self.expression = 1
        self.isSubmerged = True
        self.timeStartedSubmerge = timeIntoSimulation(data)

    def unSubmerge(self):
        self.expression = 0
        self.isSubmerged = False
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

        if(self.willDrown and timeIntoSimulation(data) - self.timeToDrown >= data.submergeTime):
            self.drown(data)
            self.willDrown = False

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


    def checkSwimmerCollisions(self, data): 
        dotList = data.experimentDots if (data.mode == data.modes[3]) else data.trainingDots
        for other in dotList:
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
    data.modes = ['splashScreen', 'training', 'postTraining', 'experiment']
    data.timePeriods = ['Training', 'Initial', 'Condition', 'End']
    data.mode = data.modes[0]
    data.contrastColor = "#edc78e"
    data.waterColor = '#48a3f2'
    

    splashScreenInit(data)

    data.drawGreenTick = False 
    data.startResponseDraw = 0
    data.responseDisplayDelay = 0.5
    data.greenTickColor = '#067c2d'
    data.drawRedX = False
    data.isDuringDrowning = False
    data.submergeTime = 3

    # [(time, clickDelay, swimmer.expression)...]
    data.correctClickDelays = [] #in seconds - difference between drown start and save

    #(clickNum, time, timePeriod, isCorrect, onSwimmer, isDuringDrowning, onDiver, clickDelay, swimmer.expression, swimmer.x, swimmer.y)
    data.clickLog = [] # in seconds 


def initPopulate(data, dotList):
    i = 0
    #cR is the circle radius
    offset = 25
    numPatrons = NUM_SWIMMERS
    while (i < numPatrons):
        xCord = random.randint(POOL_BORDER_WIDTH +offset, data.width - POOL_BORDER_WIDTH - offset)
        yCord = random.randint(POOL_BORDER_HEIGHT + offset, data.height - 50 - offset)
        dotList.append(MovingDot(xCord, yCord))
        i = i + 1


######################################
# DELEGATOR HANDLERS
######################################

def mousePressed(event, data):
    if (data.mode == 'training'): trainingMousePressed(event, data)
    elif (data.mode == 'experiment'): experimentMousePressed(event, data)
    

def keyPressed(event, data): pass

def spacePressed(event, data):
    if(data.mode == 'splashScreen'): splashScreenSpacePressed(event, data)
    elif(data.mode == 'postTraining'): postTrainingSpacePressed(event, data)

def redrawAll(canvas, data):
    if (data.mode == 'splashScreen'): splashScreenRedrawAll(canvas, data)
    elif (data.mode == 'training'): trainingRedrawAll(canvas, data)
    elif (data.mode == 'postTraining'): postTrainingRedrawAll(canvas, data)
    elif (data.mode == 'experiment'): experimentRedrawAll(canvas, data)
    

def timerFired(data):
    if (data.mode == 'training'): trainingTimerFired(data)
    elif (data.mode == 'experiment'): experimentTimerFired(data)

def switchMode(newMode, data):
    # ['splashScreen', 'training', 'postTraining', 'experiment']
    if(newMode == data.modes[1]):
        trainingInit(data)
    elif(newMode == data.modes[3]):
        experimentInit(data)
    data.mode = newMode


######################################
# SPLASH SCREEN HANDLERS
######################################

def splashScreenInit(data):
    data.splashSpaceBarPressed = False

def splashScreenSpacePressed(event, data):
    if(data.splashSpaceBarPressed):
        switchMode(data.modes[1], data)
    else:
        data.splashSpaceBarPressed = True

def splashScreenRedrawAll(canvas, data):
    #canvas.create_text(data.width/2, data.height/2, text="Its Over", font=("Arial", 200), fill="red")
    offset = data.height/10
    if (not data.splashSpaceBarPressed):
        canvas.create_text(data.width/2, data.height/4, text="Welcome to Team Blopit's Experiment!", font=("Arial", 48), fill=data.contrastColor)
        canvas.create_text(data.width/2, data.height/4 + offset, text="We are grateful for your time", font=("Arial", 36), fill=data.contrastColor)
        canvas.create_text(data.width/2, data.height/4 + 4*offset, text="Please Read the Instructions sheet", font=("Arial", 48), fill=data.contrastColor)
        canvas.create_text(data.width/2, data.height/4 + 5*offset, text="Ask us if you have any questions", font=("Arial", 36), fill=data.contrastColor)
        canvas.create_text(data.width/2, data.height/4 + 5.5*offset, text="Press the SpaceBar to proceed to training", font=("Arial", 24), fill=data.contrastColor)
    else:
        canvas.create_text(data.width/2, data.height/2, text="Last chance! Make sure you understand the instructions", font=("Arial", 36), fill=data.contrastColor)
        canvas.create_text(data.width/2, data.height/4 + 5.5*offset, text="Press the SpaceBar to Actually proceed to training", font=("Arial", 36), fill=data.contrastColor)



######################################
# TRAINING HANDLERS
######################################


def trainingInit(data):
    # populate pool
    # start timers

    data.trainingStarted = True
    data.trainingOver = False
    data.trainingStart = time.time()
    data.trainingEnd = 45 # 45

    #[30, 60, 100, 250, 270] # in seconds
    # [5, 10, 15, 20] # for testing

    data.trainingDrownerTimes = [5, 15, 35] #for testing
    data.trainingDrownerTimes.sort()

    data.trainingDrownerNum = 0
    data.trainingClickNum = 0

    data.trainingDots = []
    initPopulate(data, data.trainingDots)

def trainingMousePressed(event, data):
    if(not data.trainingOver):
        swimmerClicked = False
        for dot in reversed(data.trainingDots):
            if (dot.containsPoint(event.x, event.y)):
                swimmerClicked = True
                if (dot.isDrowning):
                    #TODO 
                    #logClick(data, timeIntoSimulation(data), True, swimmerClicked, dot) # correct
                    data.drawGreenTick = True
                    data.startResponseDraw = time.time()
                    dot.unDrown(data)

                else:
                    #logClick(data, timeIntoSimulation(data), False, swimmerClicked, dot) # incorrect onswimmer
                    data.drawRedX = True
                    data.startResponseDraw = time.time()
        if(not swimmerClicked):
            #logClick(data, timeIntoSimulation(data), False, swimmerClicked, None) # offswimmer
            data.drawRedX = True
            data.startResponseDraw = time.time()

def trainingRedrawAll(canvas, data):
    for dot in data.trainingDots:
        dot.draw(canvas)
    if(data.drawGreenTick):
        drawGreenTick(canvas, data)

    if(data.drawRedX):
        drawRedX(canvas, data)

    if(data.trainingOver):
        canvas.create_text(data.width/2, data.height/2, text="Its Over", font=("Arial", 200), fill="red")

def trainingTimerFired(data):
    if(not data.trainingOver): 
        for dot in data.trainingDots:
            dot.onTimerFired(data)
            if(dot.isSubmerged and timeIntoSimulation(data) - dot.timeStartedSubmerge >= data.submergeTime):
                dot.unSubmerge()


        checkToDrown(data)
        checkToSubmerge(data)

        if(data.trainingEnd <= timeIntoSimulation(data)):
            data.trainingOver = True
            # TODO CHANGE DATA OUTPUT AND LOGGING TO TRAINING ONLY
            # printFinalData(data)
            # writeToCSV(data.clickLog)
    else:
        switchMode(data.modes[2], data)



######################################
# POSTTRAINING HANDLERS
######################################


def postTrainingSpacePressed(event, data):
    switchMode(data.modes[3], data)

def postTrainingRedrawAll(canvas, data):
    offset = data.height/10
    canvas.create_text(data.width/2, data.height/2, text="Your training session is done!", font=("Arial", 48), fill=data.contrastColor)
    canvas.create_text(data.width/2, data.height/4 + 4*offset, text="Raise your hand if you have any questions", font=("Arial", 36), fill=data.contrastColor)
    canvas.create_text(data.width/2, data.height/4 + 5.5*offset, text="Press the SpaceBar to Begin Experiment", font=("Arial", 36), fill=data.contrastColor)


######################################
# EXPERIMENT HANDLERS
######################################

def experimentInit(data):
    # start timers
    #data.initialMeasureEnd = 120 # should be 120 - 2 Minutes
    #data.endMeasureStart = 1020 # should be 1020 - 17 Minutes 
    #data.experimentStart = time.time()
    #data.experimentEnd = 1200 # should be 1200, 20 minutes. 2 init measure, 15 condition, 3 end measure.

    data.initialMeasureEnd = 10 # should be 120 - 2 Minutes
    data.endMeasureStart = 20 # should be 1020 - 17 Minutes 
    data.experimentStart = time.time()
    data.experimentEnd = 30 # should be 1200, 20 minutes. 2 init measure, 15 condition, 3 end measure.

    setUpExperimentTimers(data)

    data.experimentStarted = True
    data.isOver = True

    data.experimentDrownerNum = 0
    data.experimentClickNum = 0

    data.experimentDots = []
    initPopulate(data, data.experimentDots)


def setUpExperimentTimers(data):
    # THESE TIMES ARE RELATIVE TO THE BEGINNING OF EACH PERIOD 
    # i.e. num of seconds into (CONDITION or INITIAL or END) 
    # NOT IN ABSOLUTE SECONDS INTO EXPERIMENT, please edit them as such, don't do absolute secs. 

    #SET THAT TIME
    # Change condition to 40 times
    conditionDrownerTimes = [51, 199, 323, 527, 795]
    initialMeasureDrownerTimes = [3, 60, 95] 
    endMeasureDrownerTimes = [15, 60, 140]

    initialMeasureDrownerTimes.sort()
    conditionDrownerTimes.sort()
    endMeasureDrownerTimes.sort()
    assert(conditionDrownerTimes[-1] < data.endMeasureStart - data.initialMeasureEnd)
    assert(initialMeasureDrownerTimes[-1] < data.initialMeasureEnd)

    data.experimentDrownerTimes = initialMeasureDrownerTimes + list(map(lambda x: x + data.initialMeasureEnd, conditionDrownerTimes)) + list(map(lambda x: x + data.endMeasureStart, endMeasureDrownerTimes))


def experimentMousePressed(event, data):
    if(not data.isOver):
        swimmerClicked = False
        for dot in reversed(data.experimentDots):
            if (dot.containsPoint(event.x, event.y)):
                swimmerClicked = True
                if (dot.isDrowning):
                    logClick(data, timeIntoSimulation(data), True, swimmerClicked, dot) # correct
                    data.drawGreenTick = True
                    data.startResponseDraw = time.time()
                    dot.unDrown(data)

                else:
                    logClick(data, timeIntoSimulation(data), False, swimmerClicked, dot) # incorrect onswimmer
                    data.drawRedX = True
                    data.startResponseDraw = time.time()
        if(not swimmerClicked):
            logClick(data, timeIntoSimulation(data), False, swimmerClicked, None) # offswimmer
            data.drawRedX = True

            data.startResponseDraw = time.time()

def experimentRedrawAll(canvas, data):
    for dot in data.experimentDots:
        dot.draw(canvas)
    if(data.drawGreenTick):
        drawGreenTick(canvas, data)

    if(data.drawRedX):
        drawRedX(canvas, data)

    if(data.isOver):
        canvas.create_text(data.width/2, data.height/2, text="Its Over", font=("Arial", 180), fill="red")
        canvas.create_text(data.width/2, 3 * data.height/4, text="Thank you!", font=("Arial", 120), fill=data.greenTickColor)
def experimentTimerFired(data):
    #occasionally have some dots submerge.
    if(not data.isOver): 
        for dot in data.experimentDots:
            dot.onTimerFired(data)
            if(dot.isSubmerged and timeIntoSimulation(data) - dot.timeStartedSubmerge >= data.submergeTime):
                dot.unSubmerge()

        checkToDrown(data)
        checkToSubmerge(data)

        if(data.experimentEnd <= timeIntoSimulation(data)):
            data.isOver = True
            printFinalData(data)
            writeToCSV(data.clickLog)

def keyPressed(event, data): pass


def drawGreenTick(canvas, data):
    timeResponseDisplay(data, "tick")
    canvas.create_text(data.width/2, data.height/2, text="safe!", font=("Arial", 120), fill=data.greenTickColor)

def drawRedX(canvas, data):
    timeResponseDisplay(data,"X")
    canvas.create_text(data.width/2, data.height/2, text="X", font=("Arial", 200), fill="red")

def timeResponseDisplay(data, response):
    if(response == 'tick'):
        if(time.time() - data.startResponseDraw >= data.responseDisplayDelay and data.drawGreenTick):
            data.drawGreenTick = False

    elif(response == 'X'):
        if(time.time() - data.startResponseDraw >= data.responseDisplayDelay and data.drawRedX):
            data.drawRedX = False



def logClick(data, time, isCorrect, onSwimmer, swimmer=None):
    #sanity Checks
    assert(onSwimmer == bool(swimmer))
    if(swimmer != None):
        assert(isinstance(swimmer,MovingDot)) 
    if(timeIntoSimulation(data) <= data.initialMeasureEnd):
        timePeriod = data.timePeriods[1]
    elif(timeIntoSimulation(data) >= data.endMeasureStart):
        timePeriod = data.timePeriods[3]
    else:
        timePeriod = data.timePeriods[2]

    clickDelay = None
    logExpression = None
    onDiver = (onSwimmer and not isCorrect and swimmer.expression == 1)
    xLoc = None
    yLoc = None
    swimmerStill = None

    if(swimmer != None):
        xLoc = swimmer.x 
        yLoc = swimmer.y
        logExpression = swimmer.expression
        swimmerStill = (swimmer.speed == 0)

        if (isCorrect): 
            clickDelay = time - swimmer.timeStartedDrowning 
            data.correctClickDelays.append((time, clickDelay, logExpression))

    #(clickNum, time, timePeriod, isCorrect, onSwimmer, isDuringDrowning, onDiver, clickDelay, swimmer.expression, swimmerStill, swimmer.x, swimmer.y)
    data.clickLog.append((data.experimentClickNum, time, timePeriod, isCorrect, onSwimmer, data.isDuringDrowning, onDiver, 
                                                    clickDelay, logExpression, swimmerStill, xLoc, yLoc))
    print("click: ", data.clickLog[data.experimentClickNum])
    data.experimentClickNum += 1
    print("Clicks so far = ", data.experimentClickNum)

def checkToSubmerge(data):
    dotList = data.experimentDots if (data.mode == data.modes[3]) else data.trainingDots
    roll = random.randint(1, 40) # this is called 3 times per second, so we expect a drowner every 120 seconds on avg
    if(roll == 5):
        canSubmerge = list(filter(lambda x: not (x.isDrowning or x.isColliding or x.willDrown), dotList))
        random.choice(canSubmerge).submerge(data)

def checkToDrown(data):
    isExperimentMode = data.mode == data.modes[3]
    dotList = data.experimentDots if isExperimentMode else data.trainingDots
    drownerNum = data.experimentDrownerNum if isExperimentMode else data.trainingDrownerNum
    drownerTimes = data.experimentDrownerTimes if isExperimentMode else data.trainingDrownerTimes

    haveDrownersLeft = drownerNum < len(drownerTimes)

    if(haveDrownersLeft and timeIntoSimulation(data) >= drownerTimes[drownerNum]):
        #filter dots in a collision -- no colliders or already drowners
        canDrown = list(filter(lambda x: not (x.isDrowning or x.isColliding), dotList))
        if(len(canDrown) > 0):
            print("drowned", drownerNum)
            random.choice(canDrown).startDrown(data)
            if(isExperimentMode):
                data.experimentDrownerNum += 1 # make sure it doesnt go beyond list len
            else:
                data.trainingDrownerNum += 1



def printFinalData(data):
    print("Total Click Nums= ", data.experimentClickNum)
    print("All Click info : \n", data.clickLog)
    print("All Correct clicks: \n", data.correctClickDelays)

def writeToCSV(myClickList):
    # TODO: name the file according to the 'PARTICIPANT ID'
    with open(DATA_OUT_TO, 'w', newline='') as csvfile:
        fieldnames = ['clickNum','time', 'timePeriod', 'isCorrect', 'onSwimmer', 'isDuringDrowning', 
                'onDiver', 'clickDelay', 'expression', 'swimmerStill', 'swimmerX', 'swimmerY']

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect="excel")

        writer.writeheader()
        for click in myClickList:
            writer.writerow({'clickNum': click[0],
                            'time': click[1], 
                            'timePeriod': click[2], 
                            'isCorrect': click[3], 
                            'onSwimmer': click[4], 
                            'isDuringDrowning': click[5], 
                            'onDiver': click[6], 
                            'clickDelay': click[7], 
                            'expression': click[8],
                            'swimmerStill': click[9], 
                            'swimmerX': click[10], 
                            'swimmerY': click[11]})

####################################
# RUN FUNCTION
####################################

def run(width, height):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        #Draw pool background
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill= data.contrastColor, width=0)
        #Draw Pool water
        canvas.create_rectangle(POOL_BORDER_WIDTH, POOL_BORDER_HEIGHT, data.width - POOL_BORDER_WIDTH, data.height - POOL_BORDER_HEIGHT,
                                fill= data.waterColor , width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def spacePressedWrapper(event, canvas, data):
        spacePressed(event, data)
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
    root.bind("<space>", lambda event:
                            spacePressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(WIDTH, HEIGHT)