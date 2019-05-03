__version__ = "1.0.0"

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.graphics import *
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.slider import Slider

import math
import numpy as np

Builder.load_file('PaintApp.kv')

'''
ShapeSelectPopup() extends Kivy's popup class https://kivy.org/docs/api-kivy.uix.popup.html
This class contains 3 buttons, when the user taps a button, the popup should close, and the app should
draw whatever shape the user selected.
'''
class ShapeSelectPopup(Popup):
    def __init__(self, parentscreen, **kwargs):
        super(ShapeSelectPopup, self).__init__(**kwargs)
        # local variable for storing the parent screen of this popup
        self.parentScreen = parentscreen

        # link the layout object
        myLayout = self.ids.shapeLayout

        # create button objects
        squareBtn = Button(text='Square')
        circleBtn = Button(text='Circle')
        lineBtn = Button(text='Line')

        # bind to callbacks
        squareBtn.bind(on_release=self.parentScreen.selectSquare)
        circleBtn.bind(on_release=self.parentScreen.selectCircle)
        lineBtn.bind(on_release=self.parentScreen.selectLine)

        # add buttons to layout
        myLayout.add_widget(squareBtn)
        myLayout.add_widget(circleBtn)
        myLayout.add_widget(lineBtn)

'''
ColorSelectPopup() extends Kivy's Popup class https://kivy.org/docs/api-kivy.uix.popup.html
This class consists of 3 sliders. When the user clicks apply, the value of the sliders should be packaged
up into a tuple and then sent off to the current drawing widget to draw different colors. The current drawing
widget is reached through the self.parentScreen variable.
'''
class ColorSelectPopup(Popup):
    def __init__(self, parentScreen, **kwargs):
        super(ColorSelectPopup, self).__init__(**kwargs)
        # local variable for storing the parent screen of this popup
        self.parentScreen = parentScreen

        #link the layout object
        myLayout = self.ids.colorLayout

        # create sliders and labels
        self.redLabel = Label(text="Red")
        self.redSlider = Slider(min=0,max=100,value=0)
        self.greenLabel = Label(text="Green")
        self.greenSlider = Slider(min=0, max=100, value=0)
        self.blueLabel = Label(text="Blue")
        self.blueSlider = Slider(min=0,max=100,value=0)

        # create Buttons, bind callbacks, and add them to a sub-layout
        self.btnLayout = BoxLayout(orientation='horizontal',spacing=self.height * 0.05)
        self.applyButton = Button(text='Apply')
        self.cancelButton = Button(text='Cancel')
        self.applyButton.bind(on_release=self.applyCallback)
        self.cancelButton.bind(on_release=self.dismiss)
        self.btnLayout.add_widget(self.applyButton)
        self.btnLayout.add_widget(self.cancelButton)

        # add everything to layout
        myLayout.add_widget(self.redLabel)
        myLayout.add_widget(self.redSlider)
        myLayout.add_widget(self.greenLabel)
        myLayout.add_widget(self.greenSlider)
        myLayout.add_widget(self.blueLabel)
        myLayout.add_widget(self.blueSlider)
        myLayout.add_widget(self.btnLayout)

    def applyCallback(self, button):
        print("applyCallback")
        self.parentScreen.setColor(self.redSlider.value_normalized,
                                   self.greenSlider.value_normalized,
                                   self.blueSlider.value_normalized)
        self.dismiss()

class SizeSelectPopup(Popup):
    def __init__(self, parentScreen, **kwargs):
        super(SizeSelectPopup, self).__init__(**kwargs)
        self.parentScreen = parentScreen

        myLayout = self.ids.sizeLayout

        # create sliders and labels
        self.thicknessLabel = Label(text="Thickness")
        self.thicknessSlider = Slider(min=1,max=10,value=1)
        self.radiusLabel = Label(text="Radius")
        self.radiusSlider = Slider(min=10, max=150, value=10)

        # create Buttons, bind callbacks, and add them to a sub-layout
        self.btnLayout = BoxLayout(orientation='horizontal',spacing=self.height * 0.05)
        self.applyButton = Button(text='Apply')
        self.cancelButton = Button(text='Cancel')
        self.applyButton.bind(on_release=self.applyCallback)
        self.cancelButton.bind(on_release=self.dismiss)
        self.btnLayout.add_widget(self.applyButton)
        self.btnLayout.add_widget(self.cancelButton)

        # add everything to layout
        myLayout.add_widget(self.thicknessLabel)
        myLayout.add_widget(self.thicknessSlider)
        myLayout.add_widget(self.radiusLabel)
        myLayout.add_widget(self.radiusSlider)
        myLayout.add_widget(self.btnLayout)

    def applyCallback(self, button):
        print("SizeSelectPopup.applyCallback()")
        self.parentScreen.setSize(self.thicknessSlider.value, self.radiusSlider.value)
        self.dismiss()

class ToolbarButton(Button):
    def colorSelectCallback(self):
        print("colorSelectCallback()")
        colorPopup = ColorSelectPopup()
        colorPopup.open()
    def shapeSelectCallback(self):
        print("shapeSelectCallback()")
        shapePopup = ShapeSelectPopup()
        shapePopup.open()
    def sizeSelectCallback(self):
        print("sizeSelectCallback()")
        sizePopup = SizeSelectPopup()
        sizePopup.open()
    def clearScreenCallback(self):
        print("clearScreenCallback()")
    def undoToolCallback(self):
        print("undoSelectCallback()")

'''
The DrawingWidget class is the only drawing widget for the paint app. What the drawing widget does is use a string to
keep track of what type of shape to draw.
'''
class DrawingWidget(Widget):
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
        #initialize drawing widget to draw circles.
        self.curShape = "circle"
        self.color = color #color is a tuple that represents R,G,B, set the default color to Blue
        self.shapeStack = shapeStack

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
        #keep track of current and previous touches
        self.prevTouch = self.curTouch
        self.curTouch = touch

        if self.resetTouch: #if reset flag raised, then set the previous touch to none
            self.prevTouch = None
            self.resetTouch = False

        if self.curShape == "circle":
            useAdjustment = False
            if len(self.shapeStack) > 0:
                if len(self.shapeStack) > 1:
                    point = {
                        'x': self.curTouch.x,
                        'y': self.curTouch.y
                    }

                    self.findIntersections(point, self.rootCircle)
                    pass
                useAdjustment = True
                point = {
                    'x': self.curTouch.x,
                    'y': self.curTouch.y
                }
                self.rootCircle = {
                    'radius': self.shapeStack[0]['Radius'],  # todo: remove hardcoded shape reference
                    'x': self.shapeStack[0]['Touch1'].x,
                    'y': self.shapeStack[0]['Touch1'].y
                }
                adjustedPoint = self.adjustPoint(point, self.rootCircle)
                thirdCenter = self.findIntersections(adjustedPoint, self.rootCircle)
                # print('Our adjusted point is: ' + str(adjustedPoint))
            with self.canvas:
                Color(*self.color)

                if useAdjustment:
                    Line(circle=(adjustedPoint[0], adjustedPoint[1], self.radius), width=self.thickness)
                    # Color(*(0, 1, 0))
                    # Line(points=(self.rootCircle['x'], self.rootCircle['y'], adjustedPoint[0], adjustedPoint[1]),
                    #      width=self.thickness)
                    # Line(circle=(thirdCenter[0], thirdCenter[1], self.radius), width=self.thickness)
                else:
                    Line(circle=(touch.x, touch.y, self.radius), width=self.thickness)

                # todo: make this dictionary save the adjusted point somehow
                # todo: Make ShapeDict a class called Shape
                shapeDict = {'Shape': "circle", 'Thickness': self.thickness, 'Radius': self.radius, "Touch1": self.curTouch, "Touch2": None}
                self.shapeStack.append(shapeDict)
        elif self.curShape == "square":
            #self.color = (0,1,0)
            with self.canvas:
                Color(*self.color)
                size = self.radius
                # Rectangle(pos=(touch.x, touch.y), size=(75, 75))
                Line(points=(self.curTouch.x - size, self.curTouch.y + size, # top left
                             self.curTouch.x - size, self.curTouch.y - size, # bot left
                             self.curTouch.x + size, self.curTouch.y - size, # bot right
                             self.curTouch.x + size, self.curTouch.y + size,), # top right
                     width=self.thickness,
                     close=True)
                shapeDict = {'Shape': "square", 'Thickness': self.thickness, 'Radius': self.radius, "Touch1": self.curTouch, "Touch2": None}
                self.shapeStack.append(shapeDict)
        elif self.curShape == "line":
            if self.prevTouch is None: # if this is the first tap, draw a dot
                with self.canvas:
                    Color(0,0,0)
                    Line(circle=(self.curTouch.x, self.curTouch.y, 1))
            else: # else draw a line from the prev to the cur
                with self.canvas:
                    Color(*self.color)
                    Line(points=(self.prevTouch.x, self.prevTouch.y, self.curTouch.x, self.curTouch.y),width=self.thickness)
                    self.resetTouch = True
                    shapeDict = {'Shape': "line", 'Thickness': self.thickness, 'Radius': self.radius, "Touch1": self.prevTouch, "Touch2": self.curTouch}
                    self.shapeStack.append(shapeDict)

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
        colorRed = (1, 0, 0)
        colorBlue = (0, 0, 1)
        colorGreen = (0, 1, 0)
        colorPurple = (1, 0, 0.75)

        r = circle['radius']
        centerOne = np.array([
            circle['x'],
            circle['y']
        ])
        magnitudeA = r / 2
        magnitudeB = magnitudeA * math.sqrt(3)
        # magnitudeB = (math.sqrt(3) / 2) * r  # sin(60 degrees) * hypotenuse

        aVector_direction = centerOne - centerTwo
        aVector_unit = aVector_direction / np.linalg.norm(aVector_direction)
        aVector_final = centerOne - (aVector_unit * magnitudeA)



        # https://gamedev.stackexchange.com/questions/70075/how-can-i-find-the-perpendicular-to-a-2d-vector
        bVector_initial = np.array([
            -aVector_final[1],
            aVector_final[0]
        ])

        sanityCheck = np.dot(aVector_final, bVector_initial)
        print("aVector dot bVector_initial should be 0: " + str(sanityCheck))

        bVector_unit = bVector_initial / np.linalg.norm(bVector_initial)

        sanityCheck = np.dot(aVector_final, bVector_unit)
        print("aVector dot bVector_unit should be 0: " + str(sanityCheck))

        bVector_final = aVector_final + (magnitudeB * bVector_unit)
        # finalVector = aVector_final + bVector_final

        sanityCheck = np.dot(aVector_final, bVector_final)
        print("aVector dot bVector_final should be 0: " + str(sanityCheck))

        # Draw Vector
        self.drawVector(centerOne, aVector_final, colorPurple)
        self.drawVector(bVector_initial, aVector_final, colorGreen)
        self.drawVector(bVector_unit, aVector_final, colorRed)
        self.drawVector(bVector_final, aVector_final, colorBlue)


        return bVector_final

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

    # each draw function changes this widget's curShape string
    def drawCircle(self):
        self.curShape = "circle"

    def drawSquare(self):
        self.curShape = "square"

    def drawLine(self):
        self.curShape = "line"

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

    def drawShape(self, lastShape):
            if lastShape['Shape'] == 'circle':
                with self.canvas:
                    Color(*self.color)
                    Line(circle=(lastShape['Touch1'].x, lastShape['Touch1'].y, lastShape['Radius']), width=lastShape['Thickness'])
            elif lastShape['Shape'] == 'square':
                with self.canvas:
                    Color(*self.color)
                    size = lastShape['Radius']
                    curTouch = lastShape['Touch1']
                    # Rectangle(pos=(touch.x, touch.y), size=(75, 75))
                    Line(points=(curTouch.x - size, curTouch.y + size, # top left
                                 curTouch.x - size, curTouch.y - size, # bot left
                                 curTouch.x + size, curTouch.y - size, # bot right
                                 curTouch.x + size, curTouch.y + size,), # top right
                         width=lastShape['Thickness'],
                         close=True)
            elif lastShape['Shape'] == 'line':
                with self.canvas:
                    Color(*self.color)
                    prevTouch = lastShape['Touch1']
                    curTouch = lastShape['Touch2']
                    Line(points=(prevTouch.x, prevTouch.y, curTouch.x, curTouch.y),width=lastShape['Thickness'])

    def undoDraw(self):
        if len(self.shapeStack) == 0: #if there are no shapes, do nothing
            pass
        else:
            self.shapeStack.pop()
            for shape in self.shapeStack:
                self.drawShape(shape)

        # lastShape = None
        # if len(self.shapeStack) > 0:
        #     lastShape = self.shapeStack.pop()
        # if lastShape is not None:
        #     if lastShape['Shape'] == 'circle':
        #         with self.canvas:
        #             Color(0,0,0)
        #             Line(circle=(lastShape['Touch1'].x, lastShape['Touch1'].y, lastShape['Radius']), width=lastShape['Thickness'])
        #     elif lastShape['Shape'] == 'square':
        #         with self.canvas:
        #             Color(0,0,0)
        #             size = lastShape['Radius']
        #             curTouch = lastShape['Touch1']
        #             # Rectangle(pos=(touch.x, touch.y), size=(75, 75))
        #             Line(points=(curTouch.x - size, curTouch.y + size, # top left
        #                          curTouch.x - size, curTouch.y - size, # bot left
        #                          curTouch.x + size, curTouch.y - size, # bot right
        #                          curTouch.x + size, curTouch.y + size,), # top right
        #                  width=lastShape['Thickness'],
        #                  close=True)
        #     elif lastShape['Shape'] == 'line':
        #         with self.canvas:
        #             Color(0,0,0)
        #             prevTouch = lastShape['Touch1']
        #             curTouch = lastShape['Touch2']
        #             Line(points=(prevTouch.x, prevTouch.y, curTouch.x, curTouch.y),width=lastShape['Thickness'])


# # Circle draw function - Eric Avery
# class CircleDraw(Widget):
#     def on_touch_down(self, touch):
#         color = (0,0,1)
#         with self.canvas:
#             Color(*color)
#             d = 30.
#             Line(circle=(touch.x, touch.y, d), width=2)
#             #Line(circle=(touch.x, touch.y, d), width=2)
#     def circleColor(self):
#         return Color(0,0,1)
#
# #Square draw function - Eric Avery
# class SquareDraw(Widget):
#     def on_touch_down(self, touch):
#         color = (0,1,0)
#         with self.canvas:
#             Color(*color)
#             Rectangle(pos=(touch.x, touch.y), size=(75, 75))
#
# #Line draw function - Eric Avery
# class LineDraw(Widget):
#     def on_touch_down(self, touch):
#         color = (1,0,0)
#         with self.canvas:
#             Color(*color)
#             touch.ud['line'] = Line(points=(touch.x, touch.y))
#     def on_touch_move(self, touch):
#         touch.ud['line'].points += [touch.x, touch.y]



class Toolbar(Widget):
    pass

'''
RootCanvas contains the drawing widget. Implementation of drawing different shapes is left up to the developer,
but I think it would be easiest to create new drawing widgets with new settings and then remove the old ones.
'''
class RootCanvas(Widget):
    def __init__(self, **kwargs):
        super(RootCanvas, self).__init__(**kwargs)
        #self.currentDrawingWidget = CircleDraw()
        self.canvasShapeStack = []
        defaultColor = (0,0,1)
        self.currentDrawingWidget = DrawingWidget(self.canvasShapeStack, defaultColor)
        self.ids.canvasLayout.add_widget(self.currentDrawingWidget)

    # return the current drawing widget. - Eric Avery
    def getCurDrawingWidget(self):
        return self.currentDrawingWidget

    # # change the drawing widget methodology - Eric Avery
    # def setCurDrawingWidget(self, mystring):
    #     if mystring == "square":
    #         self.ids.canvasLayout.remove_widget(self.currentDrawingWidget)
    #         self.currentDrawingWidget = SquareDraw()
    #         self.ids.canvasLayout.add_widget(self.currentDrawingWidget)
    #     elif mystring == "circle":
    #         self.ids.canvasLayout.remove_widget(self.currentDrawingWidget)
    #         self.currentDrawingWidget = CircleDraw()
    #         self.ids.canvasLayout.add_widget(self.currentDrawingWidget)
    #     elif mystring == "line":
    #         self.ids.canvasLayout.remove_widget(self.currentDrawingWidget)
    #         self.currentDrawingWidget = LineDraw()
    #         self.ids.canvasLayout.add_widget(self.currentDrawingWidget)
    #     return self.currentDrawingWidget

    #clear screen methodology - Eric Avery
    def clearWidgets(self, freshWidgetBoolean):
        if freshWidgetBoolean:
            self.canvasShapeStack = []
            currentColor = self.currentDrawingWidget.getColor()
            self.ids.canvasLayout.remove_widget(self.currentDrawingWidget)
            self.currentDrawingWidget = DrawingWidget(self.canvasShapeStack, currentColor)
            self.ids.canvasLayout.add_widget(self.currentDrawingWidget)
        else:
            self.canvasShapeStack = self.currentDrawingWidget.getShapeStack()
            currentColor = self.currentDrawingWidget.getColor()
            self.ids.canvasLayout.remove_widget(self.currentDrawingWidget)
            self.currentDrawingWidget = DrawingWidget(self.canvasShapeStack, currentColor)
            self.ids.canvasLayout.add_widget(self.currentDrawingWidget)

    def undo(self):
        self.clearWidgets(False)
        self.currentDrawingWidget.undoDraw()


'''
RootScreen() extends Screen https://kivy.org/docs/api-kivy.modules.screen.html
RootScreen holds everything. It holds the popup objects. It holds the canvas and toolbar objects.
It gets the drawing object from rootCanvas, and it links all the toolbar buttons from the toolbar object.
'''
class RootScreen(Screen):
    def __init__(self, **kwargs):
        super(RootScreen, self).__init__(**kwargs)
        # get layout by id
        rootLayout = self.ids.rootLayout

        # create popups
        self.colorSelectPopup = ColorSelectPopup(self)
        self.shapeSelectPopup = ShapeSelectPopup(self)
        self.sizeSelectPopup = SizeSelectPopup(self)

        # create root canvas and toolbar objects
        self.rootCanvas = RootCanvas()
        toolbar = Toolbar(size_hint_y=0.1)

        # get drawing widget
        self.curDrawingWidget = self.rootCanvas.getCurDrawingWidget()
        # self.color = CircleDraw.circleColor(self)


        #link and bind all toolbar buttons
        colorBtn = toolbar.ids.colorBtn
        colorBtn.bind(on_release=self.openColorPopup)
        shapeBtn = toolbar.ids.shapeBtn
        shapeBtn.bind(on_release=self.openShapePopup)
        sizeBtn = toolbar.ids.sizeBtn
        sizeBtn.bind(on_release=self.openSizePopup)
        clearBtn = toolbar.ids.clearBtn
        clearBtn.bind(on_release=self.clearScreen)
        undoBtn = toolbar.ids.undoBtn
        undoBtn.bind(on_release=self.undoCallback)

        # add root canvas and toolbar objects to layout
        rootLayout.add_widget(self.rootCanvas)
        rootLayout.add_widget(toolbar)

    def openSizePopup(self, button):
        print("openSizePopup()")
        self.sizeSelectPopup.open()

    def openColorPopup(self, button):
        print("openColorPopup()")
        self.colorSelectPopup.open()

    def openShapePopup(self, button):
        print("openColorPopup()")
        self.shapeSelectPopup.open()

    #COMPLETED. Resets drawing widget to circle by default - Eric Avery
    def clearScreen(self, button):
        print("clearScreen()")
        self.rootCanvas.clearWidgets(True)

    def undoCallback(self, button):
        print("undoCallback()")
        # TODO: Implement undo logic
        # get last drawn shape
        self.rootCanvas.undo()

    #all three shape selectors work - Eric Avery
    def selectSquare(self, btn):
        print("selectSquare()")
        #self.curDrawingWidget = self.rootCanvas.setCurDrawingWidget("square")
        self.rootCanvas.currentDrawingWidget.drawSquare()
        self.shapeSelectPopup.dismiss()

    def selectCircle(self, btn):
        print("selectCircle()")
        #self.curDrawingWidget = self.rootCanvas.setCurDrawingWidget("circle")
        self.rootCanvas.currentDrawingWidget.drawCircle()
        self.shapeSelectPopup.dismiss()

    def selectLine(self, btn):
        print("selectLine()")
        #self.curDrawingWidget = self.rootCanvas.setCurDrawingWidget("line")
        self.rootCanvas.currentDrawingWidget.drawLine()
        self.shapeSelectPopup.dismiss()

    def setColor(self, redVal, greenVal, blueVal):
        self.rootCanvas.currentDrawingWidget.setColor(redVal, greenVal, blueVal)

    def setSize(self, thickness, radius):
        self.rootCanvas.currentDrawingWidget.setSize(thickness, radius)



#     # Changes shape color to red - Eric Avery
#     def selectRed(self, btn):
#         print("selectRed()")
#         self.color = CircleDraw.canvas.Color(1, 0, 0)
#         #self.rootCanvas = (1, 0, 0)
#         self.dismiss()
#
#         # Changes shape color to blue - Eric Avery
#
#     def selectBlue(self, btn):
#         print("selectBlue()")
#         self.parentScreen.color = (0, 1, 0)
#         self.dismiss()
#
#         # Changes shape color to green - Eric Avery
#
#     def selectGreen(self, btn):
#         print("selectGreen()")
#         self.parentScreen.color = (0, 0, 1)
#         self.dismiss()

'''
RootManager() extends ScreenManager https://kivy.org/docs/api-kivy.uix.screenmanager.html
This class doesn't do anything other than hold our screen. It may be useful to remove this class completely.
'''
class RootManager(ScreenManager):
    def __init__(self, **kwargs):
        super(RootManager, self).__init__(**kwargs)
        rootScreen = RootScreen()
        self.add_widget(rootScreen)


'''
PaintApp extends App https://kivy.org/docs/api-kivy.app.html
This is the root of the app. The build() function is called when the app starts, and all it does is
return the rootmanager, which contains the rootscreen, which holds everything.
'''
class PaintApp(App):
    def build(self):
        rootManager = RootManager()
        return rootManager

# main calls the run function of PaintApp()
if __name__ == '__main__':
    PaintApp().run()
