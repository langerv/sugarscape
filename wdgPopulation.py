'''
Created on 2010-05-03

@author: rv
'''

from tkinter import *

class WdgPopulation():
    '''
    classdocs
    '''

    def __init__(self, populationSeries, title = "Population time series", width = 600, height = 300):
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
        
        # Create population time series
        maxPopulation = max(populationSeries)
        incry = float(self.height - 100) / maxPopulation
        self.series = []
        curve = []
        x = x0
        for i in populationSeries:
            curve.append(x)
            curve.append(y0 - i * incry)
            x += 1
            if x >= self.width:
                self.series.append(curve)
                curve = []
                x = x0
        self.series.append(curve)
        
        # Add text coordinates
        self.canvas.create_text(x0 + 10, y0 - maxPopulation * incry, text = maxPopulation)
        self.canvas.create_text(x, y0 - 10 - populationSeries[-1] * incry, text = populationSeries[-1])

    # Display widget
    def execute(self):
        self.canvas.create_line(*self.X, arrow = LAST)
        self.canvas.create_line(*self.Y, arrow = LAST)
        for curve in self.series:
            self.canvas.create_line(*curve, fill = 'blue')
        self.root.mainloop()
