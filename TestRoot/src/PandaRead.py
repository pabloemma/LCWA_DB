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
        self.vers = "0.0.1"  #
        

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
        
    def RT1(self,ReduceList=None,ReduceFile=None):
        
        
        newtab1 = self.lcwa_data.loc[:,ReduceList]
        if(ReduceFile != None):
            newtab1.to_csv(ReduceFile)
            
        #Now we reduce table to just one device_name  
        
        newtab2 = newtab1[newtab1['deviceName'] == 'madre-de-dios']
        newtab = newtab2.reset_index(drop=True)
        
        
        
        #newtab.to_csv('/Users/klein/LCWA/data/new/test1.csv')
        #print(newtab.head(5))
        #newtab.to_csv(ReduceFile)
        n = len(newtab.index)
        #first rearrange time
        s1 = (PDS.to_datetime(newtab['dtCreate'][0:n-1].reset_index(drop=True)).astype(int)  + PDS.to_datetime(newtab['dtCreate'][1:n].reset_index(drop=True)).astype(int))/2./1.e9
        dt = PDS.to_datetime(newtab['dtCreate'][1:n].reset_index(drop=True)).astype(int)/1.e9  - PDS.to_datetime(newtab['dtCreate'][0:n-1].reset_index(drop=True)).astype(int)/1.e9
        s2 = (newtab['lanTxBytes'][1:n].reset_index(drop=True)  - newtab['lanTxBytes'][0:n-1].reset_index(drop=True))/dt
        s3 = (newtab['lanRxBytes'][1:n].reset_index(drop=True)  - newtab['lanRxBytes'][0:n-1].reset_index(drop=True))/dt
        s4 = (newtab['wlanTxBytes'][1:n].reset_index(drop=True)  - newtab['wlanTxBytes'][0:n-1].reset_index(drop=True))/dt
        s5 = (newtab['wlanRxBytes'][1:n].reset_index(drop=True)  - newtab['wlanRxBytes'][0:n-1].reset_index(drop=True))/dt
           
        s6 = (newtab['lanTxErrors'][1:n].reset_index(drop=True)  - newtab['lanTxErrors'][0:n-1].reset_index(drop=True))/dt
        s7 = (newtab['lanRxErrors'][1:n].reset_index(drop=True)  - newtab['lanRxErrors'][0:n-1].reset_index(drop=True))/dt
        s8 = (newtab['wlanTxErrors'][1:n].reset_index(drop=True)  - newtab['wlanTxErrors'][0:n-1].reset_index(drop=True))/dt
        s9 = (newtab['wlanRxErrors'][1:n].reset_index(drop=True)  - newtab['wlanRxErrors'][0:n-1].reset_index(drop=True))/dt
        
        s10 = (newtab['lanTxPackets'][1:n].reset_index(drop=True)  - newtab['lanTxPackets'][0:n-1].reset_index(drop=True))/dt
        s11 = (newtab['lanRxPackets'][1:n].reset_index(drop=True)  - newtab['lanRxPackets'][0:n-1].reset_index(drop=True))/dt
        s12 = (newtab['wlanTxPackets'][1:n].reset_index(drop=True)  - newtab['wlanTxPackets'][0:n-1].reset_index(drop=True))/dt
        s13 = (newtab['wlanRxPackets'][1:n].reset_index(drop=True)  - newtab['wlanRxPackets'][0:n-1].reset_index(drop=True))/dt
        
        s14 = (newtab['cpuUsage'][0:n-1].reset_index(drop=True)  + newtab['cpuUsage'][1:n].reset_index(drop=True))/2.
        s15 = newtab.loc[:,'deviceName']
        #s15 = newtab['deviceName'][0:n-1]
        print(newtab['deviceName'])


        ReduceTableTemp = PDS.concat([s1,s2,s3,s4,s5,s6,s7,s8,s9,s10,s11,s12,s13,s14,s15],axis = 1)
        #rename columns
        #ReduceTableTemp.columns['dtCreate','lanTxBytesRate']
        collist =['dtCreate','lanTxBytesRate','lanRxBytesRate','wlanTxBytesRate','wlanRxBytesRate' , \
                  'lanTxErrorRate','lanRxErrorRate','wlanTxErrorRate','wlanRxErrorRate', \
                  'lanTxPacketsRate','lanRxPacketsRate','wlanTxPacketsRate','wlanRxPacketsRate', \
                  'cpuUsage','deviceName']
        tt = ReduceTableTemp.set_axis(collist,axis=1,inplace=False)
        print(tt.head(5))
        tt.to_csv('/Users/klein/LCWA/data/new/test.csv')

               
    def ReduceTable(self,ReduceList=None,ReduceFile=None): 
        """
        this routine reduces  the orginal table to a table consisting only on the columns listed
        in ReduceList. ReduceFile would be new file with reduced table
        """ 
        
        
        
        
        newtab = self.lcwa_data.loc[:,ReduceList]

        
        #now that we have reduced the size we need to massage it to get rid of the values being
        #incremental
        
        #this is solution from Kun
        # assume original dataframe is named data, with two columns 'time', and 'value'
        #n = len(data.index)
        #s1 = (data['time'][0:n-1].reset_index(drop=True)  + data['time'][1:n].reset_index(drop=True))/2.
        #dt = data['time'][1:n].reset_index(drop=True) - data['time'][0:n-1].reset_index(drop=True)
        #s2 = (data['value'][0:n-1].reset_index(drop=True) + data['value'][1:n].reset_index(drop=True))/dt
        #s2.rename('rate')
        #newdata = pd.concat([s1, s2], axis=1)
        
        n = len(newtab.index)
        #first rearrange time
        s1 = (PDS.to_datetime(newtab['dtCreate'][0:n-1].reset_index(drop=True)).astype(int)  + PDS.to_datetime(newtab['dtCreate'][1:n].reset_index(drop=True)).astype(int))/2./1.e9
        dt = PDS.to_datetime(newtab['dtCreate'][1:n].reset_index(drop=True)).astype(int)/1.e9  - PDS.to_datetime(newtab['dtCreate'][0:n-1].reset_index(drop=True)).astype(int)/1.e9
        s2 = (newtab['lanTxBytes'][0:n-1].reset_index(drop=True)  + newtab['lanTxBytes'][1:n].reset_index(drop=True))/dt
        s3 = (newtab['lanRxBytes'][0:n-1].reset_index(drop=True)  + newtab['lanRxBytes'][1:n].reset_index(drop=True))/dt
        s4 = (newtab['wlanTxBytes'][0:n-1].reset_index(drop=True)  + newtab['wlanTxBytes'][1:n].reset_index(drop=True))/dt
        s5 = (newtab['wlanRxBytes'][0:n-1].reset_index(drop=True)  + newtab['wlanRxBytes'][1:n].reset_index(drop=True))/dt
           
        s6 = (newtab['lanTxErrors'][0:n-1].reset_index(drop=True)  + newtab['lanTxErrors'][1:n].reset_index(drop=True))/dt
        s7 = (newtab['lanRxErrors'][0:n-1].reset_index(drop=True)  + newtab['lanRxErrors'][1:n].reset_index(drop=True))/dt
        s8 = (newtab['wlanTxErrors'][0:n-1].reset_index(drop=True)  + newtab['wlanTxErrors'][1:n].reset_index(drop=True))/dt
        s9 = (newtab['wlanRxErrors'][0:n-1].reset_index(drop=True)  + newtab['wlanRxErrors'][1:n].reset_index(drop=True))/dt
        
        s10 = (newtab['lanTxPackets'][0:n-1].reset_index(drop=True)  + newtab['lanTxPackets'][1:n].reset_index(drop=True))/dt
        s11 = (newtab['lanRxPackets'][0:n-1].reset_index(drop=True)  + newtab['lanRxPackets'][1:n].reset_index(drop=True))/dt
        s12 = (newtab['wlanTxPackets'][0:n-1].reset_index(drop=True)  + newtab['wlanTxPackets'][1:n].reset_index(drop=True))/dt
        s13 = (newtab['wlanRxPackets'][0:n-1].reset_index(drop=True)  + newtab['wlanRxPackets'][1:n].reset_index(drop=True))/dt
        
        s14 = (newtab['cpuUsage'][0:n-1].reset_index(drop=True)  + newtab['cpuUsage'][1:n].reset_index(drop=True))/dt
        s15 = newtab.loc[:,'deviceName']

        s2.rename('lanTxBytesRate')
        s3.rename('lanRxBytesRate')
        s4.rename('wlanTxBytesRate')
        s5.rename('wlanRxBytesRate')
        
        s6.rename('lanTxErrorRate')
        s7.rename('lanRxErrorRate')
        s8.rename('wlanTxErrorRate')
        s9.rename('wlanRxErrorRate')
       
        s10.rename('lanTxPacketsRate')
        s11.rename('lanRxPacketsRate')
        s12.rename('wlanTxPacketsRate')
        s13.rename('wlanRxPacketsRate')
        
        s14.rename('cpuUsage')
        s15.rename('deviceName')



        self.ReduceTable = PDS.concat([s1,s2,s3,s4,s5,s6,s7,s8,s9,s10,s11,s12,s13,s14,s15],axis = 1)
        
        #here we save the reduced table:
        
        print(self.ReduceTable.head(2))
    
    
        
    
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
    #PR.ReduceTable(ReduceList = ReduceList , ReduceFile = ReduceFile)
    PR.RT1(ReduceList = ReduceList , ReduceFile = ReduceFile)
    PR.PlotVariable_Time(variable1, value1,variable2,value2)