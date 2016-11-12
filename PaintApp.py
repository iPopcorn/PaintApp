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
        squareBtn.bind(on_release=self.parentScreen.changeShape("square"))
        circleBtn.bind(on_release=self.selectCircle)
        lineBtn.bind(on_release=self.selectLine)

        # add buttons to layout
        myLayout.add_widget(squareBtn)
        myLayout.add_widget(circleBtn)
        myLayout.add_widget(lineBtn)

    def selectSquare(self, btn):
        print("selectSquare()")
        self.parentScreen.changeShape("square");
        self.dismiss()
    def selectCircle(self, btn):
        print("selectCircle()")
        self.parentScreen.changeShape("circle");
        self.dismiss()
    def selectLine(self, btn):
        print("selectLine()")
        self.parentScreen.changeShape("line");
        self.dismiss()

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
        redLabel = Label(text="Red")
        redSlider = Slider(min=0,max=100,value=0)
        greenLabel = Label(text="Blue")
        greenSlider = Slider(min=0, max=100, value=0)
        blueLabel = Label(text="Blue")
        blueSlider = Slider(min=0,max=100,value=0)

        # create Buttons, bind callbacks, and add them to a sub-layout
        btnLayout = BoxLayout(orientation='horizontal',spacing=self.height * 0.05)
        applyButton = Button(text='Apply')
        cancelButton = Button(text='Cancel')
        applyButton.bind(on_release=self.applyCallback)
        cancelButton.bind(on_release=self.dismiss)
        btnLayout.add_widget(applyButton)
        btnLayout.add_widget(cancelButton)

        # add everything to layout
        myLayout.add_widget(redLabel)
        myLayout.add_widget(redSlider)
        myLayout.add_widget(greenLabel)
        myLayout.add_widget(greenSlider)
        myLayout.add_widget(blueLabel)
        myLayout.add_widget(blueSlider)
        myLayout.add_widget(btnLayout)

    def applyCallback(self):
        print("applyCallback")
        self.dismiss()

# Changes shape color to red - Eric Avery
    def selectRed(self, btn):
        print("selectRed()")
        self.parentScreen.color = (1, 0, 0)
        self.dismiss()

# Changes shape color to blue - Eric Avery
    def selectBlue(self, btn):
        print("selectBlue()")
        self.parentScreen.color = (0, 1, 0)
        self.dismiss()

# Changes shape color to green - Eric Avery
    def selectGreen(self, btn):
        print("selectGreen()")
        self.parentScreen.color = (0, 0, 1)
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
    def clearScreenCallback(self):
        print("clearScreenCallback()")

    def undoToolCallback(self):
        print("undoSelectCallback()")

'''
This widget draws circles. Implementation for drawing is left up to the developer to figure out a way
that makes sense.
'''

# Circle draw function - Eric Avery
class CircleDraw(Widget):
    def on_touch_down(self, touch):
        color = (0,0,1)
        with self.canvas:
            Color(*color)
            d = 30.
            Line(circle=(touch.x, touch.y, d), width=2)

#Square draw function - Eric Avery
class SquareDraw(Widget):
    def on_touch_down(self, touch):
        color = (0,1,0)
        with self.canvas:
            Color(*color)
            Rectangle(pos=(touch.x, touch.y), size=(75, 75))

#Line draw function - Eric Avery
class LineDraw(Widget):
    def on_touch_down(self, touch):
        color = (1,0,0)
        with self.canvas:
            Color(*color)
            touch.ud['line'] = Line(points=(touch.x, touch.y))
    def on_touch_move(self, touch):
        touch.ud['line'].points += [touch.x, touch.y]



class Toolbar(Widget):
    pass

'''
RootCanvas contains the drawing widget. Implementation of drawing different shapes is left up to the developer,
but I think it would be easiest to create new drawing widgets with new settings and then remove the old ones.
'''
class RootCanvas(Widget):
    def __init__(self, **kwargs):
        super(RootCanvas, self).__init__(**kwargs);
        self.currentDrawingWidget = CircleDraw();
        self.ids.canvasLayout.add_widget(self.currentDrawingWidget);

    # return the current drawing widget.
    def getCurDrawingWidget(self):
        return self.currentDrawingWidget;

    def setCurDrawingWidget(self, myString):
        if myString == "square":
            self.currentDrawingWidget = SquareDraw();
        elif myString == "circle":
            self.currentDrawingWidget = CircleDraw();
        elif myString == "line":
            self.currentDrawingWidget = LineDraw();


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

        # create root canvas and toolbar objects
        self.rootCanvas = RootCanvas()
        toolbar = Toolbar(size_hint_y=0.1)

        # get drawing widget
        self.curDrawingWidget = self.rootCanvas.getCurDrawingWidget()

        #link and bind all toolbar buttons
        colorBtn = toolbar.ids.colorBtn
        colorBtn.bind(on_release=self.openColorPopup)
        shapeBtn = toolbar.ids.shapeBtn
        shapeBtn.bind(on_release=self.openShapePopup)
        clearBtn = toolbar.ids.clearBtn
        clearBtn.bind(on_release=self.clearScreen)
        undoBtn = toolbar.ids.undoBtn
        undoBtn.bind(on_release=self.undoCallback)

        # add root canvas and toolbar objects to layout
        rootLayout.add_widget(self.rootCanvas)
        rootLayout.add_widget(toolbar)

    def openColorPopup(self, button):
        print("openColorPopup()")
        self.colorSelectPopup.open()

    def openShapePopup(self, button):
        print("openColorPopup()")
        self.shapeSelectPopup.open()

    def clearScreen(self, button):
        print("clearScreen()")
        self.rootCanvas.canvas.clear()
        #reset canvas to have currentDrawingWidget

    def undoCallback(self, button):
        print("undoCallback()")
        # TODO: Implement undo logic

    def changeShape(self, myString):
        print("changeShape()")
        if myString == "square":
            self.rootCanvas.setCurDrawingWidget(myString);
            self.rootCanvas.curDrawingWidget = self.rootCanvas.getCurDrawingWidget()
        elif myString == "circle":
            self.rootCanvas.setCurDrawingWidget(myString);
        elif myString == "line":
            self.rootCanvas.setCurDrawingWidget(myString);
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