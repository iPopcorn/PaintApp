from kivy.uix.popup import Popup
from kivy.uix.button import Button


class ShapeSelectPopup(Popup):
    """
    ShapeSelectPopup() extends Kivy's popup class https://kivy.org/docs/api-kivy.uix.popup.html
    This class contains 3 buttons, when the user taps a button, the popup should close, and the app should
    draw whatever shape the user selected.
    """
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
