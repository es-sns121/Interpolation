import pandas as pd

class Import:
    
    def __init__(self, filename):
        self.filename = filename
        self.X = None
        self.Y = None
        self.data = None
        
    def read(self):
        dataframe = pd.read_excel(self.filename, index=None, header=None)
        data = dataframe.values
 
        self.X    = data[0][1:]     # Get the X axis of the chart.
        self.Y    = data[:, 0][1:]  # Get the Y axis of the chart.
        self.data = data[1:,1:]     # Get the rest of the chart.
