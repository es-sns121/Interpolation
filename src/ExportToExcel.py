# 
# Author(s): Evan Smith, smithej@ornl.gov
#

import pandas as pd

class Exporter:
    def __init__(self, filename='exported_data.xlsx'):
        self.filename = filename

    def export(self, headers, columns):
        '''
        Export a headers array and columns array to an excel file.
        
        The headers will constitute the first row of the file.
        The columns will constitute the contents of every column below the first row.
        
        Parameters
        ----------
            headers : Array-like object containing the header names for each column.
            columns : Array-like object containing the column data.
        
        Returns
        -------
            Nothing. File is exported to current directory.
        '''
        # Create a dictionary keyed on column name, and valued on column data.
        
        data = {}
        if len(headers) != len(columns):
            print 'Number of headers does not match the number of columns. Cannot export to file.'
            return
        
        for i in range(len(headers)):
            data[headers[i]] = columns[i]
        
        # Create a DataFrame from the passed arrays.
        dataFrame = pd.DataFrame(data)
        
        dataFrame.to_excel(self.filename, 'Data', index=False)
        
