from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button


class SizeSelectPopup(Popup):
    """
    Popup that allows user to select the size
    """
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
