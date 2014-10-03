'''
Created on 2010-05-23

@author: rv
'''
from Tkinter import *

class WdgAgent():
    '''
    classdocs
    '''
    
    def __init__(self, metabolismMean, visionMean, title = "Agents' metabolism and vision means", width = 600, height = 300):
        '''
        Constructor
        '''
        self.root = Tk()
        self.root.title(title)
        self.canvas = Canvas(self.root, width = width, height = height)
        self.canvas.pack()
        self.width = width
        self.height = height

        # Create axis
        x0 = 20
        y0 = self.height - 20
        self.X = [0, y0, self.width, y0]
        self.Y = [x0, self.height, x0, 0]
        
        incry = float(self.height - 100) / 10
        
        # Create metabolism mean series
        seriesItr = self.createFormatSeries(x0, y0, self.width, self.height, 1, incry, metabolismMean)
        self.metabolismSeries = []
        while True:
            try:
                self.metabolismSeries.append(seriesItr.next())
            except StopIteration:
                break
        
        # Create vision mean series
        seriesItr = self.createFormatSeries(x0, y0, self.width, self.height, 1, incry, visionMean)
        self.visionSeries = []
        while True:
            try:
                self.visionSeries.append(seriesItr.next())
            except StopIteration:
                break
            
        # Add text coordinates for metabolism
        self.canvas.create_text(x0 + 10, y0 - metabolismMean[0] * incry, text = metabolismMean[0], fill = 'blue', anchor = SW)
        self.canvas.create_text(self.metabolismSeries[-1][-2], y0 - 10 - metabolismMean[-1] * incry, text = metabolismMean[-1], fill = 'blue', anchor = SW)

        # Add text coordinates for vision
        self.canvas.create_text(x0 + 10, y0 - visionMean[0] * incry, text = visionMean[0], fill = 'red', anchor = SW)
        self.canvas.create_text(self.visionSeries[-1][-2], y0 - 10 - visionMean[-1] * incry, text = visionMean[-1], fill = 'red', anchor = SW)

    # Generator that formats data in series 
    def createFormatSeries(self, xmin, ymin, xmax, ymax, dx, dy, data):
        curve = []
        x = xmin
        for datum in data:
            curve.append(x)
            curve.append(ymin - datum * dy)
            x += dx
            if x >= xmax:
                yield curve
                curve = []
                x = xmin
        yield curve

    # Display widget
    def execute(self):
        self.canvas.create_line(*self.X, arrow = LAST)
        self.canvas.create_line(*self.Y, arrow = LAST)
        for curve in self.metabolismSeries:
            self.canvas.create_line(*curve, fill = 'blue')
        for curve in self.visionSeries:
            self.canvas.create_line(*curve, fill = 'red')
        self.root.mainloop()
        