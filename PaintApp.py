from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.graphics import Color, Ellipse, Line
from kivy.uix.button import Button
from kivy.uix.popup import Popup

Builder.load_file('PaintApp.kv')


class ShapeSelectPopup(Popup):
    pass


class ColorSelectPopup(Popup):
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
    def bucketToolCallback(self):
        print("bucketSelectCallback()")
    def undoToolCallback(self):
        print("undoSelectCallback()")


class CircleDraw(Widget):
    def on_touch_down(self, touch):
        color = (1,0,0)
        with self.canvas:
            Color(*color)
            d = 30.
            #Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d,d))
            Line(circle=(touch.x, touch.y, d),width=2)


class Toolbar(Widget):
    pass


class RootCanvas(Widget):
    pass


class RootScreen(Screen):
    def __init__(self, **kwargs):
        super(RootScreen, self).__init__(**kwargs)


class RootManager(ScreenManager):
    def __init__(self, **kwargs):
        super(RootManager, self).__init__(**kwargs)
        rootScreen = RootScreen()
        self.add_widget(rootScreen)


class PaintApp(App):
    def build(self):
        rootManager = RootManager()
        return rootManager

if __name__ == '__main__':
    PaintApp().run()