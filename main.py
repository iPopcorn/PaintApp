__version__ = "1.0.0"
from src.RootManager import RootManager
from kivy.app import App
from kivy.lang import Builder

Builder.load_file('PaintApp.kv')


class PaintApp(App):
    """
    PaintApp extends App https://kivy.org/docs/api-kivy.app.html
    This is the root of the app. The build() function is called when the app starts, and all it does is
    return the rootmanager, which contains the rootscreen, which holds everything.
    """
    def build(self):
        rootManager = RootManager()
        return rootManager


# main calls the run function of PaintApp()
if __name__ == '__main__':
    PaintApp().run()
