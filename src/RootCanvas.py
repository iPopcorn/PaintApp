from src.DrawingWidget import DrawingWidget

from kivy.uix.widget import Widget


class RootCanvas(Widget):
    """
    RootCanvas contains the drawing widget. Implementation of drawing different shapes is left up to the developer,
    but I think it would be easiest to create new drawing widgets with new settings and then remove the old ones.
    """
    def __init__(self, **kwargs):
        super(RootCanvas, self).__init__(**kwargs)
        self.canvasShapeStack = []
        defaultColor = (0,0,1)
        self.currentDrawingWidget = DrawingWidget(self.canvasShapeStack, defaultColor)
        self.ids.canvasLayout.add_widget(self.currentDrawingWidget)

    # return the current drawing widget. - Eric Avery
    def getCurDrawingWidget(self):
        return self.currentDrawingWidget

    #clear screen methodology - Eric Avery
    def clearWidgets(self, freshWidgetBoolean):
        if freshWidgetBoolean:
            self.canvasShapeStack = []
            currentColor = self.currentDrawingWidget.getColor()
            self.ids.canvasLayout.remove_widget(self.currentDrawingWidget)
            self.currentDrawingWidget = DrawingWidget(self.canvasShapeStack, currentColor)
            self.ids.canvasLayout.add_widget(self.currentDrawingWidget)
        else:
            self.canvasShapeStack = self.currentDrawingWidget.getShapeStack()
            currentColor = self.currentDrawingWidget.getColor()
            self.ids.canvasLayout.remove_widget(self.currentDrawingWidget)
            self.currentDrawingWidget = DrawingWidget(self.canvasShapeStack, currentColor)
            self.ids.canvasLayout.add_widget(self.currentDrawingWidget)

    def undo(self):
        self.clearWidgets(False)
        self.currentDrawingWidget.undoDraw()