from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.boxlayout import BoxLayout


class ColorSelectPopup(Popup):
    """
    ColorSelectPopup() extends Kivy's Popup class https://kivy.org/docs/api-kivy.uix.popup.html
    This class consists of 3 sliders. When the user clicks apply, the value of the sliders should be packaged
    up into a tuple and then sent off to the current drawing widget to draw different colors. The current drawing
    widget is reached through the self.parentScreen variable.
    """
    def __init__(self, parentScreen, **kwargs):
        super(ColorSelectPopup, self).__init__(**kwargs)
        # local variable for storing the parent screen of this popup
        self.parentScreen = parentScreen

        # link the layout object
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
