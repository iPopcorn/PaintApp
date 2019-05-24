from src.RootScreen import RootScreen

from kivy.uix.screenmanager import ScreenManager


class RootManager(ScreenManager):
    """
    RootManager() extends ScreenManager https://kivy.org/docs/api-kivy.uix.screenmanager.html
    This class doesn't do anything other than hold our screen. It may be useful to remove this class completely.
    """
    def __init__(self, **kwargs):
        super(RootManager, self).__init__(**kwargs)
        rootScreen = RootScreen()
        self.add_widget(rootScreen)
