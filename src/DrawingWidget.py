from kivy.graphics import *
from kivy.uix.widget import Widget

import math
import numpy as np


class Shape:
    def __init__(self, shapeDict):
        """
        Constructor for a Shape object
        :param shapeDict: A dictionary with keys = ['Shape', 'Thickness', 'Radius', 'Center', 'Endpoint1', 'Endpoint2',
        'OriginalTouch'].
        'Endpoint1' and 'Endpoint2' will only apply to 'Line' shapes. 'Center', 'Endpoint1' and 'Endpoint2' will all be
        dictionaries with keys = ['x', 'y']
        """
        self.type = shapeDict['Shape']
        self.thickness = shapeDict['Thickness']
        self.radius = shapeDict['Radius']
        self.center = shapeDict['Center']
        self.endpoint1 = shapeDict['Endpoint1']
        self.endpoint2 = shapeDict['Endpoint2']
        self.originalTouch = shapeDict['OriginalTouch']


class DrawingWidget(Widget):
    """
    The DrawingWidget class is the only drawing widget for the paint app. What the drawing widget does is use a string to
    keep track of what type of shape to draw.
    """
    CIRCLE_SHAPE = 'circle'
    SQUARE_SHAPE = 'square'
    LINE_SHAPE = 'line'

    curShape = ""
    curTouch = None
    prevTouch = None
    resetTouch = False
    radius = 125
    thickness = 3
    shapeStack = []
    rootCircle = {}

    def __init__(self, shapeStack, color, **kwargs):
        super(DrawingWidget, self).__init__(*kwargs)
        # initialize drawing widget to draw circles.
        self.curShape = "circle"
        self.color = color  # color is a tuple that represents R,G,B, set the default color to Blue
        self.shapeStack = shapeStack

    def normalizeVector(self, myVector):
        """
        Returns a unit vector based on the vector passed in
        :param myVector: Numpy array representing the vector to normalize
        :return: Numpy array representing the normalized vector
        """
        return myVector / np.linalg.norm(myVector)

    def drawVector(self, vectorOne, vectorTwo, color):
        """
        Draws a line between the 2 given points
        :param vectorOne: numpy array, represents the start of the line
        :param vectorTwo: numpy array, represents the end of the line
        :param color: tuple, represents R, G, B color value
        :return: None
        """
        # Draw Vector
        with self.canvas:
            Color(*color)
            Line(points=(vectorOne[0], vectorOne[1], vectorTwo[0], vectorTwo[1]),
                 width=self.thickness)

    def on_touch_down(self, touch):
        # keep track of current and previous touches
        self.prevTouch = self.curTouch
        self.curTouch = touch

        if self.resetTouch:  # if reset flag raised, then set the previous touch to none
            self.prevTouch = None
            self.resetTouch = False

        if self.curShape == self.CIRCLE_SHAPE:
            self.drawCircle()

        elif self.curShape == self.SQUARE_SHAPE:
            self.drawSquare()

        elif self.curShape == self.LINE_SHAPE:
            self.drawLine()

    def findIntersections(self, centerTwo, circle):
        """
        findIntersections() takes a point and a circle, and returns 2 points that are the intersections of the circles
        created by the 2 given points.
        :param centerTwo: numpy array. Represents the center of the 2nd circle.
        :param circle: dict with keys = ['radius', 'x', 'y']
        :return: list of dicts with keys = ['x', 'y']
        """
        """
        The starting point for aVector will be the center of the circle (circle[x and y]).
        The magnitude of aVector will be half the radius.
        The direction of aVector will be from centerOne to centerTwo.

        The starting point for bVector will be the ending point for aVector.
        The magnitude of bVector can be calculated
        The direction of bVector will be perpendicular to the direction of aVector

        The starting 
        """
        # colorRed = (1, 0, 0)
        # colorBlue = (0, 0, 1)
        # colorGreen = (0, 1, 0)
        # colorPurple = (1, 0, 0.75)

        r = circle['radius']
        centerOne = np.array([
            circle['x'],
            circle['y']
        ])
        magnitudeA = r / 2
        magnitudeB = magnitudeA * math.sqrt(3)
        # magnitudeB = (math.sqrt(3) / 2) * r  # sin(60 degrees) * hypotenuse

        aVector_direction = centerOne - centerTwo
        aVector_unit = self.normalizeVector(aVector_direction)

        aVector_final = centerOne - (aVector_unit * magnitudeA)

        rootVector = centerOne - aVector_final

        # https://gamedev.stackexchange.com/questions/70075/how-can-i-find-the-perpendicular-to-a-2d-vector
        bVector_initial = np.array([
            -rootVector[1],
            rootVector[0]
        ])

        cVector_initial = np.array([
            rootVector[1],
            -rootVector[0]
        ])

        sanityCheck = np.dot(rootVector, bVector_initial)
        print("aVector dot bVector_initial should be 0: " + str(sanityCheck))

        bVector_unit = self.normalizeVector(bVector_initial)
        cVector_unit = self.normalizeVector(cVector_initial)

        sanityCheck = np.dot(rootVector, bVector_unit)
        print("aVector dot bVector_unit should be 0: " + str(sanityCheck))

        bVector_final = aVector_final + (magnitudeB * bVector_unit)
        cVector_final = aVector_final + (magnitudeB * cVector_unit)

        # finalVector = aVector_final + bVector_final

        # sanityCheck = np.dot(aVector_final, bVector_final)
        # print("aVector dot bVector_final should be 0: " + str(sanityCheck))

        # Draw Vector
        # self.drawVector(centerOne, aVector_final, colorPurple)
        # self.drawVector(bVector_initial, aVector_final, colorGreen)
        # self.drawVector(bVector_unit, aVector_final, colorRed)
        # self.drawVector(bVector_final, aVector_final, colorBlue)

        # pass

        return [bVector_final, cVector_final]

    def adjustPoint(self, givenPoint, circle):
        """
        adjustPoint() takes a point and a circle, and returns a new point that is on the circle.
        givenPoint: givenPoint is a dict with keys = ['x', 'y']
        circle: circle is a dict with keys = ['radius', 'x', 'y']
        :return:
        """
        center = np.array([circle['x'],
                           circle['y']])

        givenVector = np.array([givenPoint['x'],
                                givenPoint['y']])

        startingVector = givenVector - center
        normalizedVector = startingVector / np.linalg.norm(startingVector)

        finalVector = center + (circle['radius'] * normalizedVector)
        return finalVector

    def getColor(self):
        return self.color

    def getShapeStack(self):
        return self.shapeStack

    def setShape(self, shapeString):
        if shapeString == self.CIRCLE_SHAPE:
            self.curShape = self.CIRCLE_SHAPE
        elif shapeString == self.SQUARE_SHAPE:
            self.curShape = self.SQUARE_SHAPE
        elif shapeString == self.LINE_SHAPE:
            self.curShape = self.LINE_SHAPE
        else:  # error incorrect string argument
            print('Error: Incorrect string argument')

    # each draw function changes this widget's curShape string
    def drawCircle(self):
        useAdjustment = False
        thirdCircleFlag = False
        fourthCircleFlag = False

        if len(self.shapeStack) > 0:
            if len(self.shapeStack) > 1:
                if len(self.shapeStack) > 2:
                    fourthCircleFlag = True

                # myAdjustedPoint = self.shapeStack[1]['adjustedPoint']
                myAdjustedPoint = np.array([
                    self.shapeStack[1].center['x'],
                    self.shapeStack[1].center['y']
                ])
                intersections = self.findIntersections(myAdjustedPoint, self.rootCircle)
                thirdCenter = intersections[0]

                thirdCircleFlag = True

                if fourthCircleFlag:
                    fourthCenter = intersections[1]
                    thirdCircleFlag = False

            if fourthCircleFlag:
                useAdjustment = False
            else:
                useAdjustment = True

            point = {
                'x': self.curTouch.x,
                'y': self.curTouch.y
            }

            self.rootCircle = {
                'radius': self.shapeStack[0].radius,  # todo: remove hardcoded shape reference
                'x': self.shapeStack[0].center['x'],
                'y': self.shapeStack[0].center['y']
            }

            adjustedPoint = self.adjustPoint(point, self.rootCircle)

        with self.canvas:
            Color(*self.color)

            if not thirdCircleFlag and useAdjustment:
                Line(circle=(adjustedPoint[0], adjustedPoint[1], self.radius), width=self.thickness)
                # Line(points=(self.rootCircle['x'], self.rootCircle['y'], adjustedPoint[0], adjustedPoint[1]),
                #      width=self.thickness)

                center = {
                    'x': adjustedPoint[0],
                    'y': adjustedPoint[1]
                }

                shapeDict = {
                    'Shape': "circle",
                    'Thickness': self.thickness,
                    'Radius': self.radius,
                    'OriginalTouch': self.curTouch,
                    'Endpoint1': None,
                    'Center': center,
                    'Endpoint2': None
                }

                tmpShape = Shape(shapeDict)

            elif thirdCircleFlag:
                Line(circle=(thirdCenter[0], thirdCenter[1], self.radius), width=self.thickness)

                center = {
                    'x': thirdCenter[0],
                    'y': thirdCenter[1]
                }

                shapeDict = {
                    'Shape': "circle",
                    'Thickness': self.thickness,
                    'Radius': self.radius,
                    'OriginalTouch': self.curTouch,
                    'Endpoint1': None,
                    'Endpoint2': None,
                    'Center': center
                }

                tmpShape = Shape(shapeDict)

            elif fourthCircleFlag:
                Line(circle=(fourthCenter[0], fourthCenter[1], self.radius), width=self.thickness)

                center = {
                    'x': fourthCenter[0],
                    'y': fourthCenter[1]
                }

                shapeDict = {
                    'Shape': "circle",
                    'Thickness': self.thickness,
                    'Radius': self.radius,
                    'OriginalTouch': self.curTouch,
                    'Endpoint1': None,
                    'Endpoint2': None,
                    'Center': center
                }

                tmpShape = Shape(shapeDict)

            else:
                Line(circle=(self.curTouch.x, self.curTouch.y, self.radius), width=self.thickness)

                center = {
                    'x': self.curTouch.x,
                    'y': self.curTouch.y
                }

                shapeDict = {
                    'Shape': "circle",
                    'Thickness': self.thickness,
                    'Radius': self.radius,
                    'OriginalTouch': self.curTouch,
                    'Endpoint1': None,
                    'Endpoint2': None,
                    'Center': center
                }

                tmpShape = Shape(shapeDict)

            # todo: make this dictionary save the adjusted point somehow
            # todo: Make ShapeDict a class called Shape
            self.shapeStack.append(tmpShape)

    def drawSquare(self):
        with self.canvas:
            Color(*self.color)
            size = self.radius
            Line(points=(self.curTouch.x - size, self.curTouch.y + size,  # top left
                         self.curTouch.x - size, self.curTouch.y - size,  # bot left
                         self.curTouch.x + size, self.curTouch.y - size,  # bot right
                         self.curTouch.x + size, self.curTouch.y + size,),  # top right
                 width=self.thickness,
                 close=True)

            shapeDict = {
                'Shape': "square",
                'Thickness': self.thickness,
                'Radius': self.radius,
                'OriginalTouch': self.curTouch,
                'Endpoint1': None,
                'Endpoint2': None,
                'Center': {
                    'x': self.curTouch.x,
                    'y': self.curTouch.y
                }
            }

            tmpShape = Shape(shapeDict)
            self.shapeStack.append(tmpShape)

    def drawLine(self):
        if self.prevTouch is None:  # if this is the first tap, draw a dot
            with self.canvas:
                Color(0, 0, 0)
                Line(circle=(self.curTouch.x, self.curTouch.y, 1))
        else:  # else draw a line from the prev to the cur
            with self.canvas:
                Color(*self.color)
                Line(points=(self.prevTouch.x, self.prevTouch.y, self.curTouch.x, self.curTouch.y),
                     width=self.thickness)
                self.resetTouch = True

                shapeDict = {
                    'Shape': "line",
                    'Thickness': self.thickness,
                    'Radius': self.radius,
                    'OriginalTouch': self.curTouch,
                    'Endpoint1': {
                        'x': self.prevTouch.x,
                        'y': self.prevTouch.y
                    },
                    'Endpoint2': {
                        'x': self.curTouch.x,
                        'y': self.curTouch.y
                    },
                    'Center': None
                }

                tmpShape = Shape(shapeDict)
                self.shapeStack.append(tmpShape)

    # setColor takes 3 ints and updates this widget's color tuple
    def setColor(self, red, green, blue):
        self.color = (red, green, blue)

    # setColor takes 2 ints, thickness and radius
    def setSize(self, thickness, radius):
        self.radius = radius
        self.thickness = thickness

    def getPrevTouch(self):
        return self.prevTouch

    # undoCallback returns the last shape drawn
    def undoCallback(self):
        return self.shapeStack.pop()

    def redrawShape(self, lastShape):
        if lastShape.type == 'circle':
            with self.canvas:
                Color(*self.color)
                Line(circle=(lastShape.center['x'], lastShape.center['y'], lastShape.radius),
                     width=lastShape.thickness)
        elif lastShape.type == 'square':
            with self.canvas:
                Color(*self.color)
                size = lastShape.radius
                curTouch = lastShape.originalTouch
                # Rectangle(pos=(touch.x, touch.y), size=(75, 75))
                Line(points=(curTouch.x - size, curTouch.y + size,  # top left
                             curTouch.x - size, curTouch.y - size,  # bot left
                             curTouch.x + size, curTouch.y - size,  # bot right
                             curTouch.x + size, curTouch.y + size,),  # top right
                     width=lastShape.thickness,
                     close=True)
        elif lastShape.type == 'line':
            with self.canvas:
                Color(*self.color)
                prevTouch = lastShape.endpoint1
                curTouch = lastShape.endpoint2
                Line(points=(prevTouch['x'], prevTouch['y'], curTouch['x'], curTouch['y']), width=lastShape.thickness)

    def undoDraw(self):
        if len(self.shapeStack) == 0:  # if there are no shapes, do nothing
            pass
        else:
            self.shapeStack.pop()
            for shape in self.shapeStack:
                self.redrawShape(shape)
