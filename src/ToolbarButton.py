from src.Popup.ShapeSelectPopup import ShapeSelectPopup
from src.Popup import SizeSelectPopup
from src.Popup.ColorSelectPopup import ColorSelectPopup

from kivy.uix.button import Button
from kivy.uix.widget import Widget


class Toolbar(Widget):
    pass


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
