'''
Created on Jan 14, 2021

@author: klein

self.lcwa_data        The data buffer from the csv file, this is a pandas database structure
self.variable_list    A list fo all the variables, equiavlent to the column names
self.ReduceTable       The new table reduced to the list of columns in ReduceList 
'''

import pandas as PDS

import matplotlib.pyplot as plt

import matplotlib.dates as md


import matplotlib

import sys

import time

import datetime

import datetime as dt

from random import seed

from random import randint

import numpy as np

from pdfrw import PdfReader, PdfWriter


import os
 

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
 
        self.timecut =[0,0]
        
        self.pdf_file_list =[]
        
        
        #create colorlist
        self.MakeColorList()
        self.SetupRnd()
        
        
    def Progress(self):
        
        
        self.vers = "1.01.01   "  #
        
        a=20*'*'
        print(a,'   PandaRead   ',a,'\n \n')
        print('*',' written by Andi Klein','\n')
        print('*', 'Currently at version  ',self.vers)
        print(a,10*'*',a,'\n\n\n')
        
        
        start = self.prompt +'version'+self.vers
        print(self.prompt, 'version 0.0.03',' added plotting and a MakeTest facility')
        print(self.prompt ,'version 1.00.01','multiple graphs with correct time axis')
        print(self.prompt ,'version 1.00.02','multicolor, different markers')
        print(self.prompt ,'version 1.01.01','loops thorugh list of devices and creates a status health for all')
        print('\n\n\n')
    
    def ClearTests(self):
        """ clears all the tests"""
        self.tests = ''
        
    def ClearPlots(self):
        self.data_buf = {}
    
    
    def GetTimeStamp(self,mytime):
        """calculates the unix time stamp"""
        #strip quotes
        mytime=mytime.strip('"')
        temp = time.mktime(datetime.datetime.strptime(mytime, "%Y-%m-%d %H:%M:%S").timetuple())
        return temp
    
    def LoopDevices(self, looplist = None, Plot=False,plotdir=None , plotting = False):
        """loops through all the devices listed in looplist"""
        
        #reset list of pdf file names, needed for adding pdf files together
        self.pdf_file_list=[]
        
        if(looplist == None ):
            self.ErrorCode(101)
            return
        else:
            for k in looplist:
                print(self.prompt," currently working on ", k)
                #self.ManipTable(k)
                self.PT1(k)
                print(type(k))
                if(Plot):
                    #self.PlotDeviceStatus(self, k , plotdir = plotdir)
                    self.PlotDeviceStatus(k ,symbol='d',color1='b', plotdir = plotdir , plotting = plotting)
        
        # done with looping merge all files inot one large one
        if(plotdir != None):
            masterfile = plotdir+'alldevices.pdf'
        

            writer = PdfWriter()
            for inpfn in self.pdf_file_list:
                writer.addpages(PdfReader(inpfn).pages)
                writer.write(masterfile)
            print(self.prompt,'figure saved in ',masterfile)
        
        
        
            
            
            
 
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
        s1 = (PDS.to_datetime(newtab['dtCreate'][0:n-1].reset_index(drop=True)).astype(np.int64)  + PDS.to_datetime(newtab['dtCreate'][1:n].reset_index(drop=True)).astype(np.int64))/2./1.e9
        dt = PDS.to_datetime(newtab['dtCreate'][1:n].reset_index(drop=True)).astype(np.int64)/1.e9  - PDS.to_datetime(newtab['dtCreate'][0:n-1].reset_index(drop=True)).astype(np.int64)/1.e9
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
        
    def MakeColorList(self):
        """ I found the matplotlib handling of colors not that great
        so, i put the colors into a list """
       
        colores =   {  'aliceblue':            '#F0F8FF',
    'antiquewhite':         '#FAEBD7',
    'aqua':                 '#00FFFF',
    'aquamarine':           '#7FFFD4',
    'azure':                '#F0FFFF',
    'beige':                '#F5F5DC',
    'bisque':               '#FFE4C4',
    'black':                '#000000',
    'blanchedalmond':       '#FFEBCD',
    'blue':                 '#0000FF',
    'blueviolet':           '#8A2BE2',
    'brown':                '#A52A2A',
    'burlywood':            '#DEB887',
    'cadetblue':            '#5F9EA0',
    'chartreuse':           '#7FFF00',
    'chocolate':            '#D2691E',
    'coral':                '#FF7F50',
    'cornflowerblue':       '#6495ED',
    'cornsilk':             '#FFF8DC',
    'crimson':              '#DC143C',
    'cyan':                 '#00FFFF',
    'darkblue':             '#00008B',
    'darkcyan':             '#008B8B',
    'darkgoldenrod':        '#B8860B',
    'darkgray':             '#A9A9A9',
    'darkgreen':            '#006400',
    'darkgrey':             '#A9A9A9',
    'darkkhaki':            '#BDB76B',
    'darkmagenta':          '#8B008B',
    'darkolivegreen':       '#556B2F',
    'darkorange':           '#FF8C00',
    'darkorchid':           '#9932CC',
    'darkred':              '#8B0000',
    'darksalmon':           '#E9967A',
    'darkseagreen':         '#8FBC8F',
    'darkslateblue':        '#483D8B',
    'darkslategray':        '#2F4F4F',
    'darkslategrey':        '#2F4F4F',
    'darkturquoise':        '#00CED1',
    'darkviolet':           '#9400D3',
    'deeppink':             '#FF1493',
    'deepskyblue':          '#00BFFF',
    'dimgray':              '#696969',
    'dimgrey':              '#696969',
    'dodgerblue':           '#1E90FF',
    'firebrick':            '#B22222',
    'floralwhite':          '#FFFAF0',
    'forestgreen':          '#228B22',
    'fuchsia':              '#FF00FF',
    'gainsboro':            '#DCDCDC',
    'ghostwhite':           '#F8F8FF',
    'gold':                 '#FFD700',
    'goldenrod':            '#DAA520',
    'gray':                 '#808080',
    'green':                '#008000',
    'greenyellow':          '#ADFF2F',
    'grey':                 '#808080',
    'honeydew':             '#F0FFF0',
    'hotpink':              '#FF69B4',
    'indianred':            '#CD5C5C',
    'indigo':               '#4B0082',
    'ivory':                '#FFFFF0',
    'khaki':                '#F0E68C',
    'lavender':             '#E6E6FA',
    'lavenderblush':        '#FFF0F5',
    'lawngreen':            '#7CFC00',
    'lemonchiffon':         '#FFFACD',
    'lightblue':            '#ADD8E6',
    'lightcoral':           '#F08080',
    'lightcyan':            '#E0FFFF',
    'lightgoldenrodyellow': '#FAFAD2',
    'lightgray':            '#D3D3D3',
    'lightgreen':           '#90EE90',
    'lightgrey':            '#D3D3D3',
    'lightpink':            '#FFB6C1',
    'lightsalmon':          '#FFA07A',
    'lightseagreen':        '#20B2AA',
    'lightskyblue':         '#87CEFA',
    'lightslategray':       '#778899',
    'lightslategrey':       '#778899',
    'lightsteelblue':       '#B0C4DE',
    'lightyellow':          '#FFFFE0',
    'lime':                 '#00FF00',
    'limegreen':            '#32CD32',
    'linen':                '#FAF0E6',
    'magenta':              '#FF00FF',
    'maroon':               '#800000',
    'mediumaquamarine':     '#66CDAA',
    'mediumblue':           '#0000CD',
    'mediumorchid':         '#BA55D3',
    'mediumpurple':         '#9370DB',
    'mediumseagreen':       '#3CB371',
    'mediumslateblue':      '#7B68EE',
    'mediumspringgreen':    '#00FA9A',
    'mediumturquoise':      '#48D1CC',
    'mediumvioletred':      '#C71585',
    'midnightblue':         '#191970',
    'mintcream':            '#F5FFFA',
    'mistyrose':            '#FFE4E1',
    'moccasin':             '#FFE4B5',
    'navajowhite':          '#FFDEAD',
    'navy':                 '#000080',
    'oldlace':              '#FDF5E6',
    'olive':                '#808000',
    'olivedrab':            '#6B8E23',
    'orange':               '#FFA500',
    'orangered':            '#FF4500',
    'orchid':               '#DA70D6',
    'palegoldenrod':        '#EEE8AA',
    'palegreen':            '#98FB98',
    'paleturquoise':        '#AFEEEE',
    'palevioletred':        '#DB7093',
    'papayawhip':           '#FFEFD5',
    'peachpuff':            '#FFDAB9',
    'peru':                 '#CD853F',
    'pink':                 '#FFC0CB',
    'plum':                 '#DDA0DD',
    'powderblue':           '#B0E0E6',
    'purple':               '#800080',
    'rebeccapurple':        '#663399',
    'red':                  '#FF0000',
    'rosybrown':            '#BC8F8F',
    'royalblue':            '#4169E1',
    'saddlebrown':          '#8B4513',
    'salmon':               '#FA8072',
    'sandybrown':           '#F4A460',
    'seagreen':             '#2E8B57',
    'seashell':             '#FFF5EE',
    'sienna':               '#A0522D',
    'silver':               '#C0C0C0',
    'skyblue':              '#87CEEB',
    'slateblue':            '#6A5ACD',
    'slategray':            '#708090',
    'slategrey':            '#708090',
    'snow':                 '#FFFAFA',
    'springgreen':          '#00FF7F',
    'steelblue':            '#4682B4',
    'tan':                  '#D2B48C',
    'teal':                 '#008080',
    'thistle':              '#D8BFD8',
    'tomato':               '#FF6347',
    'turquoise':            '#40E0D0',
    'violet':               '#EE82EE',
    'wheat':                '#F5DEB3',    'whitesmoke':           '#F5F5F5',
    'yellow':               '#FFFF00',
    'yellowgreen':          '#9ACD32'}
        self.colorlist_hex=[]
        self.colorlist_name=[]
        
        for key in colores:
            self.colorlist_hex.append(colores[key])
            self.colorlist_name.append(key)
        
        
        
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

        
        # now add the timecut if there is one
        if(self.timecut != [0,0]):
            temp = '(dtCreate >'+str(self.timecut[0])+') and (dtCreate <'+str(self.timecut[1])+')'
            temp1 = temp1+'and'+temp
          
        self.tests=temp1
        print('\n ',self.prompt,'all the cuts in the current selection    ',self.tests)
        print('\n')
        
    def MakeTimeCut(self, time_low = None, time_high = None):
        """ converts the time format
        "%Y-%m-%d %h:%m:%s"
        into unix time stamp and creates a test
        if both time and time_high are given it uses this timewindow,
        otherwise it just uses time for operations """
        
        if (time_high != None):
            time_l =self.GetTimeStamp(time_low)
            time_h =self.GetTimeStamp(time_high)
            self.timecut = [time_l,time_h]
            
        else:
            time_l = self.GetTimeStamp(time_low)
            self.timecut = [time_l,0]
            
        
        
        
    def PT1(self,device):
        """plot variables with the full test suite
        """
        
        temp_data = self.ManipTable(device) # needed to get from cumulative to timeslices.
        
        temp_buf = temp_data.query(self.tests)
        self.data_buf[device] =temp_buf
        #print(self.data_buf)
        
        #self.data_buf[device].plot(x=var1,y=var2)
        
        #plt.show()

    def PlotDeviceStatus(self, device ,symbol=None,color1=None, plotdir = None , plotting = True):
        """
        Loops thorugh all the data of one device and plots it on one page
        if plotdir is not None we save the plot file
        if plotting is false, no screen output
        """
        if(symbol==None):
            symbol='-'  #solidline

        
        temp_data = self.ManipTable(device) # needed to get from cumulative to timeslices.
        
        temp_buf = temp_data.query(self.tests)
        # now loop through different variables
        temp_list = temp_buf.columns.tolist()
        print(type(temp_list))
        #temp_list =['lanRxBytesRate','wlanTxBytesRate']
        
        
        
        
        
        
        count=0
        fig = plt.figure(figsize = (10,12), dpi= 80)
        print(len(temp_list))
        gs = fig.add_gridspec(len(temp_list), hspace=0)
        axs = gs.subplots(sharex=True)
        fig.suptitle('Health of '+device)
        # main loop
        for val in temp_list:
            if(val != 'dtCreate'):
                x = temp_buf['dtCreate']
                dates=[dt.datetime.fromtimestamp(ts) for ts in x]
                y = temp_buf[val]
        
                if(color1 == None): # randomly pcik color from colorlis_hex, we have 144 one to pick from ( iremoved white ones)
                    pick =self.colorlist_hex[randint(0, 144)]

                    axs[count].plot(dates,y,symbol,label = val, color=pick)
                else: 
                    
                    axs[count].plot(dates,y,symbol,label = val , color=color1)
                axs[count].legend(loc='upper right')
                count +=1
            #print(axs)
  
        plt.legend()
        
        #save the plot
    
        if(plotdir != None):
            plotfile = plotdir+'status_'+device+'.pdf'
            print(self.prompt,'figure saved in ',plotfile)
            plt.savefig(plotfile,dpi=300)
            
            # add name to list of created files
            self.pdf_file_list.append(plotfile)
        if(plotting):
            plt.show()
                

     
        

    def PlotGraph(self, var1, var2,symbol=None,color1=None):
        
        """ currently plots all collected plots on one plot
        The data to plot are in self.data_buf, which is a dictionary
        I think in order to plot on different graphs
        I have to fill two series and then plot them
        """
        #setup figures
        
        if(symbol==None):
            symbol='-'  #solidline
        count=0
        fig = plt.figure(figsize = (10,12), dpi= 80)
        gs = fig.add_gridspec(len(self.data_buf), hspace=0)
        axs = gs.subplots(sharex=True, sharey=True)
        
        
        fig.suptitle(str(var1) +'  vs  '+str(var2))
        for key in self.data_buf:
            if(var1 == 'dtCreate'):
                #x = self.data_buf[key][var1].astype(int)
                x = self.data_buf[key][var1]
                dates=[dt.datetime.fromtimestamp(ts) for ts in x]
            else:    
                x = self.data_buf[key][var1]
            y = self.data_buf[key][var2]
            if(color1 == None): # randomly pcik color from colorlis_hex, we have 144 one to pick from ( iremoved white ones)
                pick =self.colorlist_hex[randint(0, 144)]
                if(var1 == 'dtCreate'):
                    axs[count].plot(dates,y,symbol,label = key, color=pick)
                else:
                    axs[count].plot(x,y,symbol,label = key, color=pick)
            else: 
                if(var1 == 'dtCreate'):
                    axs[count].plot(dates,y,symbol,label = key , color=color1)
                else:
                    axs[count].plot(x,y,symbol,label = key, color=color1)

                
                  
            
            
            
            if(var1 == 'dtCreate'):
                #axs[count].xaxis.set_major_locator(md.MinuteLocator(interval=360))
                axs[count].xaxis.set_major_formatter(md.DateFormatter('%m-%d %H:%M'))

            axs[count].legend(loc='upper right')
            count +=1
            #print(axs)

        if(var1 == 'dtCreate'):
            plt.xticks(rotation = 90)
            
        plt.legend()
        
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
        
    
    def ReadFile(self, filename):
        """ reads in the csv file from LaCanada
        """
        
        self.lcwa_data = PDS.read_csv(filename)
        print(" all the fields of the data file")
        
        # create a list of variables
        self.variable_list =  self.lcwa_data.head(0)
  
     
     

    def ReduceTable(self,ReduceList=None,ReduceFile=None):
        """
        this routine reduces  the orginal table to a table consisting only on the columns listed
        in ReduceList. ReduceFile would be new file with reduced table
        """ 
        
        
        self.newtab1 = self.lcwa_data.loc[:,ReduceList]
        if(ReduceFile != None):
            self.newtab1.to_csv(ReduceFile)
            
    def SetupRnd(self):
        """ sets up the random number generator for the color scheme"""
        
        # generate random integer values
       # seed random number generator
        seed(1)
        # generate some integers
    
    
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

    
    # where you put your copy of the raw data, will also be the place where you will have the reduced file
    master_dir = '/Users/klein/LCWA/data/new/'
    
    filename = master_dir+'devicedetail.csv'
    
    #instantiate the class
    PR=PandaRead()
    #read in the raw datafile
    PR.ReadFile(filename)
    
    # the list of columns we want to keep: If yo want more to keep add the names here. the
    #order does not matter
    ReduceList = ["apMac","cpuUsage","deviceIp","deviceName","dtCreate","lanRxBytes", \
              "lanRxErrors","lanRxPackets","lanTxBytes","lanTxErrors","lanTxPackets",\
              "loadavg","memBuffers","memFree","memTotal","remoteIP",\
              "remoteMac","wlanRxBytes","wlanRxErrors","wlanRxErrOther",\
              "wlanRxErrRetries","wlanRxPackets","wlanRxRate","wlanTxBytes",\
              "wlanTxErrors","wlanTxPackets","wlanTxRate"]
    
    # this is the list of the variables you can plot:
    #'dtCreate','lanTxBytesRate','lanRxBytesRate','wlanTxBytesRate','wlanRxBytesRate' , \
    #'lanTxErrorRate','lanRxErrorRate','wlanTxErrorRate','wlanRxErrorRate', \
    #'lanTxPacketsRate','lanRxPacketsRate','wlanTxPacketsRate','wlanRxPacketsRate', \
    #'cpuUsage','deviceName']
    
    looplist =[ 'RidgeRoad5','madre-de-dios', 'camp-stoney', 'camp-stoney-2', 'hampton-road-986', 'la-posta', 'la-posta-0', 'la-posta-4', 'la-posta-5', 'old-santa-fe-trail', 'old-santa-fe-trail-1216', 'old-santa-fe-trail-14', 'stone-canyon-road-1120', 'wild-turkey-way']    

    
    
    
    #testlist format: 1st test [a,operator,b], if bi is a string you have to put it into 
    # escaping quotes 'madre-de-dios' becomes '\"madre-de-dios\"'
    # always the odd index is the operator between the two neighbouring tests
    # allowed operators are: and , not , the bitwise and the arithmetic
    #
    #example fo a test list
    #testlist = [['deviceName','==','\"madre-de-dios\"'],'and',['cpuUsage','>','70.']]
    # the important thing to notice is that tests are always grouped in units of three and then a logical operatore connects those
    testlist = [['cpuUsage','>','70.']]
    
    
    # now we reduce the file to calculable units and convert to rates from cummulative
    # the reducefile is the new file created from the original one
    ReduceFile = master_dir+'reduce_devicedetail.csv'
    PR.ReduceTable(ReduceList = ReduceList , ReduceFile = ReduceFile)

    
    
    #here we set a time cut. if none is used all the times in the file will be used.
    # if you just give a low limit, all from low limit to end of file will be used.
    #the timecut will be applied to the cuts define in testlist
    PR.MakeTimeCut(time_low="2021-01-08 00:00:01", time_high="2021-01-09 00:00:01")
    
    
    PR.MakeTest(testlist)
    
    
    # for a single device status
    #PR.PlotDeviceStatus('madre-de-dios', symbol='d', color1 = 'g',plotdir = master_dir)
    
    #Here we loop over all devices defined in the looplist
    #they are all plotted
    #with plotting: true, there will be a screen plotr as well as saving the plots
    PR.LoopDevices(looplist = looplist,Plot=True,plotdir=master_dir,plotting = False)
    
    
    #here we define what to plot
    #if you want to have time on the x axis, the first value has to be dtCreate
    # the symbol defines the marker, at https://matplotlib.org/3.3.3/api/markers_api.html
    #you can find valid markers
    # here a few '-' : full line, 'o':circle,'d':diamond etc
    # you can also add a color by using color ='g' or 'k' (black),'b' etc
    # the possible colors are here https://matplotlib.org/3.2.1/tutorials/colors/colors.html
    # the following directives would all be okay
    #PR.PlotGraph('dtCreate','cpuUsage',symbol = 'd',color1='aqua')
    #PR.PlotGraph('dtCreate','cpuUsage',symbol = 'd',color1='g')
    #
    #important: if you do not select a color, every graph will have a different color, if you give the keyword color1=
    #the all the graphs will be in the same color
    
    
    PR.PlotGraph('dtCreate','cpuUsage',symbol = 'd')
    
    
    
    #usually you won't need the next routines, they are called from within the program
    #PR.PT1('madre-de-dios')
 
 
    #If you want just a quick answer for a specific device
    #uncomment the next few lines
    #variable1 = 'deviceName'
    #value1='madre-de-dios'
    #variable2 = 'cpuUsage'
    #value2 = 70.
    #device = 'madre-de-dios'

    #PR.ManipTable(device=device)

    #PR.PlotVariable_Time(variable1, value1,variable2,value2)
    
    
    
    