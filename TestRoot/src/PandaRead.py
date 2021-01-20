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

import sys



class PandaRead(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
   
         '''
         
        self.prompt = 'Panda> '
        self.error_code = [None]* 200  # a list of 200 empty messages
        
        self.tests =''
        self.Progress()
        self.data_buf = {}  # a dictionary of the reduced dataframes. Those are collected and then can be plotted
 
    def Progress(self):
        
        
        self.vers = "0.00.03   "  #
        
        a=20*'*'
        print(a,'   PandaRead   ',a,'\n \n')
        print('*',' written by Andi Klein','\n')
        print('*', 'Currently at version  ',self.vers)
        print(a,10*'*',a,'\n\n\n')
        
        
        start = self.prompt +'version'+self.vers
        print(start,' added plotting and a MakTest facility')
        print('\n\n\n')
    
    def ClearTests(self):
        """ clears all the tests"""
        self.tests = ''
        
        
    def ReadFile(self, filename):
        """ reads in the csv file from LaCanada
        """
        
        self.lcwa_data = PDS.read_csv(filename)
        print(" all the fields of the data file")
        
        # create a list of variables
        self.variable_list =  self.lcwa_data.head(0)

    def MakeTest(self, testlist):
        """ creates queries for the table
        the format in the list is ['a','op','val1'],'op',['b','op',val2] ...
         escaping quotes 'madre-de-dios' becomes '\"madre-de-dios\"'
         always the odd index is the operator between the two neighbouring tests
        allowed operators are: and , not , the bitwise and the arithmetic
        """
        
        a=testlist
        temp1=''
        
        print(len(testlist))
        for k in range(0,len(testlist),2):
  
            temp = '('+(a[k][0]+a[k][1]+a[k][2])+')'
            
            if(len(testlist)-1> k):
                temp = temp+' '+a[k+1]+ ' '  # add operator
            
            temp1 = temp1+temp
            
        self.tests=temp1
        print(self.tests)
        
        
    def PT1(self,device , var1, var2):
        """plot variables with the full test suite
        """
        
        temp_data = self.ManipTable(device) # needed to get from cumulative to timeslices.
        
        temp_buf = temp_data.query(self.tests)
        self.data_buf[device] =temp_buf
        #print(self.data_buf)
        
        #self.data_buf[device].plot(x=var1,y=var2)
        
        #plt.show()

    def PlotGraph(self, var1, var2):
        
        """ currently plots all coolected plots on one plot
        The data to plot are in self.data_buf, which is a dictionary
        """
        for key in self.data_buf:
            self.data_buf[key].plot(x=var1,y=var2,label = key)
            plt.show()
        
        
    
    def PlotVariable_Time(self , var1, val1 , var2,val2):
        """
        Plot a one dimensional figure of variable against time for give device
        var: name of the value to be plotted
        val: the actual value to be plotted. 
        this is a fast plot and requires the first variable to be the device name
        and the second to be a variable consisting of numbers
        
        """
        
        #try exec for building the cut:
        
        temp_data = self.ManipTable(val1)
 
        
         
        #exec('self.temp_buf = temp_data.loc[(temp_data["%s"]== "%s") \
        #& (temp_data["%s"] > %f)] ' \
         #% (var1 , val1 , var2 , val2))
        
        #using query
        #query_text = '\"var1 == @val1 and var2 > @val2\"'

        
        OP= 'and'
        text = '('+var1+'==@val1) ' +OP+ '('+var2+'>@val2)'
        self.temp_buf = temp_data.query(text)
        self.temp_buf.plot(x='dtCreate',y=var2)
        
        plt.show()
        
    
     
     
     
    def LoopDevices(self, looplist = None):
        """loops through all the devices litesd in looplist"""
        if(looplist == None ):
            self.ErrorCode(101)
            return
        else:
            for k in looplist:
                print(self.prompt," currently working on ", k)
                self.ManipTable(k)
        
        return 1    
   
    
    def ManipTable(self,device):
        
        """ creates a subtable for only the entries with devicename
        """
        
        
        newtab2 = self.newtab1[self.newtab1['deviceName'] == device]
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
        #print(newtab['deviceName'])


        ReduceTableTemp = PDS.concat([s1,s2,s3,s4,s5,s6,s7,s8,s9,s10,s11,s12,s13,s14,s15],axis = 1)
        #rename columns
        #ReduceTableTemp.columns['dtCreate','lanTxBytesRate']
        collist =['dtCreate','lanTxBytesRate','lanRxBytesRate','wlanTxBytesRate','wlanRxBytesRate' , \
                  'lanTxErrorRate','lanRxErrorRate','wlanTxErrorRate','wlanRxErrorRate', \
                  'lanTxPacketsRate','lanRxPacketsRate','wlanTxPacketsRate','wlanRxPacketsRate', \
                  'cpuUsage','deviceName']
        tt = ReduceTableTemp.set_axis(collist,axis=1,inplace=False)
        #print(tt.head(5))
        

        return tt

    def ReduceTable(self,ReduceList=None,ReduceFile=None):
        """
        this routine reduces  the orginal table to a table consisting only on the columns listed
        in ReduceList. ReduceFile would be new file with reduced table
        """ 
        
        
        self.newtab1 = self.lcwa_data.loc[:,ReduceList]
        if(ReduceFile != None):
            self.newtab1.to_csv(ReduceFile)
            
            
     
    
    def ErrorCode(self,code):
        """
        Handles errors and warnings. error code below 100 are sysexit
        >100 are warning and returns to flow
        """
        self.error_code[101]= " you need to provide a list to Loop over for Loopdevice to work"
        
        if(code < 101):
            print(self.prompt,'Error  code :  ',self.error_code[code])
            sys.exit(0)
        elif(code >100 and code <201):
            print(self.prompt,'Warning  code :  ',self.error_code[code])
            return
        
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
    
    looplist =[ 'RidgeRoad5','madre-de-dios', 'camp-stoney', 'camp-stoney-2', 'hampton-road-986', 'la-posta', 'la-posta-0', 'la-posta-4', 'la-posta-5', 'old-santa-fe-trail', 'old-santa-fe-trail-1216', 'old-santa-fe-trail-14', 'stone-canyon-road-1120', 'wild-turkey-way']    

    
    variable1 = 'deviceName'
    value1='madre-de-dios'
    variable2 = 'cpuUsage'
    value2 = 70.
    device = 'madre-de-dios'
    
    
    #testlist format: 1st test [a,operator,b], if bi is a string you have to put it into 
    # escaping quotes 'madre-de-dios' becomes '\"madre-de-dios\"'
    # always the odd index is the operator between the two neighbouring tests
    # allowed operators are: and , not , the bitwise and the arithmetic
    testlist = [['deviceName','==','\"madre-de-dios\"'],'and',['cpuUsage','>','70.']]
    
    ReduceFile = '/Users/klein/LCWA/data/new/reduce_devicedetail.csv'
    PR.ReduceTable(ReduceList = ReduceList , ReduceFile = ReduceFile)
    #PR.ManipTable(device='madre-de-dios')
    PR.MakeTest(testlist)
    PR.PT1('madre-de-dios','dtCreate','cpuUsage')
    PR.PlotGraph('dtCreate','cpuUsage')
    PR.LoopDevices(looplist = looplist)
    PR.PlotVariable_Time(variable1, value1,variable2,value2)