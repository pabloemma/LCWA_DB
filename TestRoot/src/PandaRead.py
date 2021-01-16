'''
Created on Jan 14, 2021

@author: klein

self.lcwa_data        The data buffer from the csv file, this is a pandas database structure
self.variable_list    A list fo all the variables, equiavlent to the column names
self.ReduceTable       The new table reduced to the list of columns in ReduceList 
'''

import pandas as PDS

import matplotlib.pyplot as plt

import matplotlib



class PandaRead(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
   
         '''
        self.vers = 0.0.1  #
        

    def ReadFile(self, filename):
        """ reads in the csv file from LaCanada
        """
        
        self.lcwa_data = PDS.read_csv(filename)
        print(" all the fields of the data file")
        
        # create a list of variables
        self.variable_list =  self.lcwa_data.head(0)

    
    def PlotVariable_Time(self , var1, val1 , var2,val2):
        """
        Plot a one dimensional figure of variable against time for give device
        """
        
        #try exec for building the cut:
        
        exec('self.temp_buf = self.lcwa_data.loc[(self.lcwa_data["%s"]== "%s") \
        & (self.lcwa_data["%s"] > %f)] ' \
         % (var1 , val1 , var2 , val2))
        
        self.temp_buf.plot(x='dtCreate',y='lanTxBytes')
        plt.show()
        
        
    def ReduceTable(self,ReduceList=None,ReduceFile=None): 
        """
        this routine reduces  the orginal table to a table consisting only on the columns listed
        in ReduceList. ReduceFile would be new file with reduced table
        """ 

        self.ReduceTable = newtab = self.lcwa_data.loc[:,ReduceList]
        #here we save the reduced table:
        if(ReduceFile != None):
            newtab.to_csv(ReduceFile)
        
        print(newtab.head(2))
        
    def CreateCut(self):
        """
        This routine creates the cut for pandas selection
        """
        example = (self.lcwa_data[variable1]== value) & (self.lcwa_data[variable2] > value2)
        return example
    
if __name__ == '__main__':
    
    filename = '/Users/klein/LCWA/data/new/devicedetail.csv'
    
    PR=PandaRead()
    PR.ReadFile(filename)
    
    # the list of columns we want to keep:
    ReduceList = ["apMac","cpuUsage","deviceIp","deviceName","dtCreate","lanRxBytes", \
              "lanRxErrors","lanRxPackets","lanTxBytes","lanTxErrors","lanTxPackets",\
              "loadavg","memBuffers","memFree","memTotal","remoteIP",\
              "remoteMac","wlanRxBytes","wlanRxErrors","wlanRxErrOther",\
              "wlanRxErrRetries","wlanRxPackets","wlanRxRate","wlanTxBytes",\
              "wlanTxErrors","wlanTxPackets","wlanTxRate"]
    
    
    
    variable1 = 'deviceName'
    value1='madre-de-dios'
    variable2 = 'lanTxBytes'
    value2 = 0.
    device = 'madre-de-dios'
    
    ReduceFile = '/Users/klein/LCWA/data/new/reduce_devicedetail.csv'
    PR.ReduceTable(ReduceList = ReduceList , ReduceFile = ReduceFile)
    PR.PlotVariable_Time(variable1, value1,variable2,value2)