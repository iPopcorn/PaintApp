from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen, ScreenManager

Builder.load_file('PaintApp.kv')


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

class Toolbar2(Widget):
    pass


class PaintApp(App):
    def build(self):
        rootManager = RootManager()
        return rootManager

if __name__ == '__main__':
    PaintApp().run()