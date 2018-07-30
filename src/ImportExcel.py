# 
# Author(s): Evan Smith, smithej@ornl.gov
#

import pandas as pd
from scipy import interpolate

class Importer:
    
    def __init__(self):
        self.X_axis = None
        self.Y_axis = None
        self.data = None
        
    def readFile(self, filename):
        dataframe = pd.read_excel(filename, index=None, header=None)
        data = dataframe.values
 
        self.X_axis = data[0][1:]     # Get the X axis of the chart.
        self.Y_axis = data[:, 0][1:]  # Get the Y axis of the chart.
        self.data   = data[1:,1:]     # Get the rest of the chart.
        
    def get2dInterpolationFunction(self):
        return interpolate.interp2d(self.X_axis, self.Y_axis, self.data)
