from src.Popup.ShapeSelectPopup import ShapeSelectPopup
from src.Popup.SizeSelectPopup import SizeSelectPopup
from src.Popup.ColorSelectPopup import ColorSelectPopup
from src.RootCanvas import RootCanvas
from src.ToolbarButton import Toolbar

from kivy.uix.screenmanager import Screen


class RootScreen(Screen):
    """
    RootScreen() extends Screen https://kivy.org/docs/api-kivy.modules.screen.html
    RootScreen holds everything. It holds the popup objects. It holds the canvas and toolbar objects.
    It gets the drawing object from rootCanvas, and it links all the toolbar buttons from the toolbar object.
    """
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

        # link and bind all toolbar buttons
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

    def clearScreen(self, button):
        print("clearScreen()")
        self.rootCanvas.clearWidgets(True)

    def undoCallback(self, button):
        print("undoCallback()")
        # TODO: Implement undo logic
        # get last drawn shape
        self.rootCanvas.undo()

    def selectSquare(self, btn):
        print("selectSquare()")

        self.rootCanvas.currentDrawingWidget.drawSquare()
        self.shapeSelectPopup.dismiss()

    def selectCircle(self, btn):
        print("selectCircle()")

        self.rootCanvas.currentDrawingWidget.drawCircle()
        self.shapeSelectPopup.dismiss()

    def selectLine(self, btn):
        print("selectLine()")

        self.rootCanvas.currentDrawingWidget.drawLine()
        self.shapeSelectPopup.dismiss()

    def setColor(self, redVal, greenVal, blueVal):
        self.rootCanvas.currentDrawingWidget.setColor(redVal, greenVal, blueVal)

    def setSize(self, thickness, radius):
        self.rootCanvas.currentDrawingWidget.setSize(thickness, radius)
