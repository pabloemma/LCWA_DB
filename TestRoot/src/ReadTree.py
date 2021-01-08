'''
Created on Dec 2, 2020

@author: klein
'''

import ROOT as RO
from ROOT import  TFile, TCut, TCanvas, TH1F,TH2F,gApplication,gROOT
#import strucDef
from array import array




from os import path 
from os.path import expanduser

import time
import datetime
import sys
#add to python path
sys.path.insert(1,'/Users/klein/git/LCWA/src')
import MakePlots as MP

import json # needed for reading in cutfiles. They are written as a dictionary

class MyReadTree(object):
    '''
    classdocs
    '''


    def __init__(self, rootfile):
        '''
        Constructor
        '''
        gROOT.Reset()
        if path.exists(rootfile):
            self.myrootfile = TFile(rootfile,"r")
        else:
            self.ErrorHandle(0,info=rootfile)
         
        # Create default Canvas
        #self.MakeCanvas() 
        
        
        # get home directory

        self.myhome = expanduser("~") +'/' 
 
        self.histo1 = []  #list of one dimensional histos
        self.histo100 = [] #list of two dimensional histos
        self.graph1 = []  #list of one dimensional graphs for tx and rx
        self.graph200 = [] #list of two dimensional grapsh
        self.multig = [] #"multigraph list"
        self.multigL = []# "legend for multigraph"
        
        self.multiglrx = [] # list of multigrahs for the lan rx
        self.multigltx = []
        self.multigwrx = []
        self.multigwtx = []
        
        
        self.compare = False # if you call getspeedboxfile this will be set to true
        self.tfmt = "%m/%d %H:%M %F 1970-01-01 00:00:00" #format for time display
    
    def CloseApp(self):
        
        self.application.Terminate()
 
    def CreateHisto11(self,variable,name='histo1',title='histo1',nchan=50,lowx=0.,highx=1000.):
        h1 = TH1F(name,title,nchan,lowx,highx)
        for entry in self.mychain:
            if self.GetTimeStamp(entry.dtCreate)>self.timecut[0] and self.GetTimeStamp(entry.dtCreate)<self.timecut[1]:
                exec('h1.Fill(entry.%s)' % variable)
        #self.c1.cd()
        #h1.Draw()
        #self.c1.Modified()
        #self.c1.Update()
        
        #a = input("press any character to continue")
        self.histo1.append(h1)
         

    def CreateHisto22(self,variable1,variable2,name='histo100',title='histo100',nchan=50,lowx=0.,highx=1e12,nchan1=50,lowx1=0.,highx1=1e12):
        h100 = TH2F(name,title,nchan,lowx,highx,nchan1,lowx1,highx1)
        for entry in self.mychain:
#
#            print(entry.dtCreate)
            if self.GetTimeStamp(entry.dtCreate)>self.timecut[0] and self.GetTimeStamp(entry.dtCreate)<self.timecut[1]:
                exec('h100.Fill(entry.%s,entry.%s)' % (variable1 , variable2))
        #h100.Draw()
        #self.c1.Modified()
        #self.c1.Update()

            
        self.histo100.append(h100)
 
    
        
    def DrawVariable(self,variable,cut_expression = None , devicename = None):
        #1 dimensional drawing
        self.c3=TCanvas('c3','LCWA3 Canvas', 950, 10, 700, 500 ) 

        self.c3.cd()
        
        if(cut_expression != None):
            cutt = self.cutlist[cut_expression]
            if(devicename != None):
                cutt = cutt+" && deviceName == \""+ devicename + "\""
                print(cutt)
            self.mychain.Draw(variable,self.MakeCut(cutt))
        else:
            if(devicename != None):
                cutt = "deviceName == \"" + devicename + "\""
                print(cutt)
                self.mychain.Draw(variable,self.MakeCut(cutt))
            else:
                self.mychain.Draw(variable)
         
        self.c3.Modified()
        self.c3.Update()
        
      

    def DrawVariable2(self,variable1,cut_expression = None, devicename = None):
        #1 dimensional drawing
        self.c4=TCanvas('c4','LCWA4 Canvas', 950, 600, 700, 500 ) 

        self.c4.cd()
        
        if(cut_expression != None):
            cutt = self.cutlist[cut_expression]
            if(devicename != None):
                cutt = cutt+" && deviceName == \""+ devicename + "\""
                print(cutt)
            self.mychain.Draw(variable1,self.MakeCut(cutt))
        else:
            if(devicename != None):
                cutt = "deviceName == \"" + devicename + "\""
                print(cutt)
                self.mychain.Draw(variable1,self.MakeCut(cutt))
            else:
                self.mychain.Draw(variable1)
         
        self.c4.Modified()
        self.c4.Update()

    def DrawGraph(self):
        """ draws the one and two dimensional histos"""
        #self.c1.Draw()

        self.MakeCanvas()
        
        if self.compare:
            self.c1.cd()
            self.root_print = "/Users/klein/scratch/compares.pdf"
            self.c1.Print(self.root_print+"[")

            self.c1.Draw()
            self.multig[0].Draw("AP")
            self.multigL[0].Draw()
            self.speedup.Draw()
            self.c1.Modified()
            self.c1.Update()
            self.c1.Draw()
            self.c1.Print(self.root_print)
            self.c1.Print(self.root_print+"]")
            self.c1.Draw()
            #return
    
        #count = 0
        #self.c1.Divide(2,2,0,0)
        #self.c1.Draw()
        #for k in self.graph1:
         #   self.c1.cd(count+1)
          #  #self.c1.Draw()
           # k.Draw("AP")
            #count+=1
            #a = input("press any character to continue")
        #self.c1.Modified()
        #self.c1.Update()
        #self.c1.Draw()
        
        #open file
        self.root_print = "/Users/klein/scratch/aaatest.pdf"
        self.c2.Print(self.root_print+"[")
        self.c2.Draw()
        for k in range(0,len(self.multig)):
            self.c2.cd()
            self.multig[k].Draw("AP")
            self.multigL[k].Draw("")
            self.c2.Modified()
            self.c2.Update()
            self.c2.Draw()
            self.c2.Print(self.root_print)
            
            self.c2.Clear()
        #self.multispeed.Draw("AP")
        self.c2.Modified()
        self.c2.Update()
        self.c2.Print(self.root_print)
 
        self.c2.Print(self.root_print+"]")
        
        self.c3=TCanvas('c3','LCWA3 Canvas', 950, 10, 700, 500 ) 

        self.c3.Draw()
        self.c3.cd()
        #self.TG2D.Draw()
        self.c3.Modified()
        self.c3.Update()
        #for k in self.histo100:
        #    self.c2.cd()
        #    self.c2.Draw()
        #    k.Draw()
        #    self.c2.Modified()
        #    self.c2.Update()
            #a = input("press any character to continue")
        
        if(self.gr2 !=None):
            self.c4=TCanvas('c3','LCWA3 Canvas', 950, 500, 700, 500 ) 

            self.c4.Draw()
            self.c4.cd()
            self.gr2.Draw("AP")
            self.c4.Modified()
            self.c4.Update()
           
    def DrawGraph1(self): 
        
        
                #constant for axis division
        ndiv = 204
        
        #offset for label
        off =.02
        
        "splitline directive"
        spl = "#splitline{%m/%d}{%H:%M}"

        xmin = 0.
        
        self.c10 = RO.TCanvas("c10"," lots of devices",20,20,900,1000)
               
        self.root_print = "/Users/klein/scratch/multiplots.pdf"
        self.c10.Print(self.root_print+"[")
        self.c10.Divide(2,2)
        self.c10.Draw()
        self.c10.cd(1)
        self.multigraph_wtx.SetMinimum(xmin)
        self.multigraph_wtx.GetXaxis().SetTimeDisplay(1);
        self.multigraph_wtx.GetXaxis().SetNdivisions(ndiv)
        self.multigraph_wtx.GetXaxis().SetTimeFormat(self.tfmt); 
        self.multigraph_wtx.GetXaxis().SetLabelOffset(off); 
        self.multigraph_wtx.GetXaxis().SetTimeFormat(spl);    
           
        self.multigraph_wtx.Draw("AP")
        self.mgL_tx.Draw("")
        
        self.c10.cd(2)
        self.multigraph_wrx.GetXaxis().SetTimeDisplay(1);
        self.multigraph_wrx.GetXaxis().SetNdivisions(ndiv)
        self.multigraph_wrx.GetXaxis().SetTimeFormat(self.tfmt);        
        self.multigraph_wrx.SetMinimum(xmin)        
        self.multigraph_wrx.GetXaxis().SetLabelOffset(off); 
        self.multigraph_wrx.GetXaxis().SetTimeFormat(spl);    
        self.multigraph_wrx.Draw("AP")
        self.mgL_rx.Draw("")
        
        self.c10.cd(3)
        self.multigraph_lrx.GetXaxis().SetTimeDisplay(1);
        self.multigraph_lrx.GetXaxis().SetNdivisions(ndiv)
        self.multigraph_lrx.GetXaxis().SetTimeFormat(self.tfmt);        
        self.multigraph_lrx.SetMinimum(xmin)        
        self.multigraph_lrx.GetXaxis().SetLabelOffset(off); 
        self.multigraph_lrx.GetXaxis().SetTimeFormat(spl);    
        self.multigraph_lrx.Draw("AP")
        self.mgL_ltx.Draw("")
        
        self.c10.cd(4)
        self.multigraph_ltx.GetXaxis().SetTimeDisplay(1);
        self.multigraph_ltx.GetXaxis().SetNdivisions(ndiv)
        self.multigraph_ltx.GetXaxis().SetTimeFormat(self.tfmt);        
        self.multigraph_ltx.SetMinimum(xmin)        
        self.multigraph_ltx.GetXaxis().SetLabelOffset(off); 
        self.multigraph_ltx.GetXaxis().SetTimeFormat(spl);    
        self.multigraph_ltx.Draw("AP")
        self.mgL_lrx.Draw("")
        
        
        
             
            
            
        #self.multispeed.Draw("AP")
        self.c10.Modified()
        self.c10.Update()
        self.c10.Draw()
        self.c10.Print(self.root_print)
 
        self.c10.Print(self.root_print+"]")

    def GetBranchList(self):
        """ Get list of branches"""
        self.Blist = []

        self.branches_list = self.mychain.GetListOfBranches() #this is an iterator TobjArray

        
        for k in range(0,len(self.branches_list)):
            self.Blist.append(self.branches_list.At(k).GetName())
        
        print(self.Blist)
     
    
    def GetDeviceList(self):
        """ Takes the list of devices and creates a new one where 
        the devices are only listed once. This will then be used to loop through all of them
        and create the graphs"""
        self.item_list =[]
        
        for k in range(0,self.myentries):
            self.mychain.GetEntry(k) 
            self.item_list.append(self.mychain.deviceName) if self.mychain.deviceName not in self.item_list else None    
        return self.item_list
    
    def GetSpeedBoxFile(self,filename):
        """ this routine reads a csv file from the speedbox
        and will the be used for graphing in the tx/rx graph
        """
        #instatiate the PlotAll
        
        #conversion constant Megabits to Bytes
        convert= 1.250e5
        GMT = 7*3600.
        
        tfmt = self.tfmt
        
        self.compare = True
        self.SF = MP.MakePlots(filename)
        self.SFdata = self.SF.ReadCSVFile() #self.SFdata is a list of three numpy array [0: time, 1: down, 2: up]
        #print(self.SFdata)
        print(filename, "  sucessfully imported")
        #Create the TGraph for speedbox
        # get length of arrays first
        array_length = len(self.SFdata[0])
        self.speeddown = RO.TGraph(array_length,self.SFdata[0]-GMT,self.SFdata[1]*convert)
        self.speeddown.SetMarkerColor(9)
        self.speeddown.SetMarkerStyle(26)
        self.speeddown.GetXaxis().SetTimeDisplay(1);
        self.speeddown.GetXaxis().SetTimeFormat(tfmt);        

        self.speedup = RO.TGraph(array_length,self.SFdata[0]-GMT,self.SFdata[2]*convert)
        self.speedup.SetMarkerColor(8)
        self.speedup.SetMarkerStyle(27)
        self.speedup.GetXaxis().SetTimeDisplay(1);
        self.speedup.GetXaxis().SetTimeFormat(tfmt);        

        self.multispeed = RO.TMultiGraph()
        self.multispeed.Add(self.speeddown)
        self.multispeed.Add(self.speedup)
        self.multispeed.GetXaxis().SetTimeDisplay(1)
        self.multispeed.GetXaxis().SetTimeFormat(tfmt)
        self.multispeed.GetXaxis().SetNdivisions(508)

    
        
            
        

    def GetNameFromIP(self,IPaddress):
        """returns the Name for a given IP 
        by looping over the tree
        """
        for k in range(0,self.myentries):
            self.mychain.GetEntry(k)    
            if(self.mychain.deviceIp==IPaddress):
                print(" device name  ",self.mychain.deviceName)
                break

    def GetIPFromName(self,Name):
        """returns the Name for a given IP 
        by looping over the tree
        """
        for k in range(0,self.myentries):
            self.mychain.GetEntry(k)    
            if(self.mychain.deviceName==Name):
                print(" device IP  ",self.mychain.deviceIp)
                break
        
    def GetTimeStamp(self,mytime):
        """calculates the unix time stamp"""
        #strip quotes
        mytime=mytime.strip('"')
        temp = time.mktime(datetime.datetime.strptime(mytime, "%Y-%m-%d %H:%M:%S").timetuple())
        return temp
        
    def LoopScanRXTX(self,devicelist = None):
        """ this routine loops over 
        all the devices and makes graphs """
        #first get the list of devices
        if(devicelist == None):
            self.GetDeviceList()
        else:
            self.item_list = devicelist
            
            
        print(self.item_list)
        self.multig_lrx=[]
        self.multig_ltx=[]
        self.multig_wrx=[]
        self.multig_wtx=[]
        
        self.multigraph_lrx = RO.TMultiGraph()
        self.multigraph_ltx = RO.TMultiGraph()
        self.multigraph_wrx = RO.TMultiGraph()
        self.multigraph_wtx = RO.TMultiGraph()
        
        #determine size according to the number of entries we have.
        number = float(len(self.item_list))
        temp = .05*number
        y2 = .9
        y1 = y2-temp
        if(y1 < .3):
            y1=.5
        
        x1 = .1
        #y1 = .5
        x2 = .48
        y2 = .9
        
         
        self.mgL_tx = RO.TLegend(x1,y1,x2,y2)
        self.mgL_rx = RO.TLegend(x1,y1,x2,y2)
        self.mgL_ltx = RO.TLegend(x1,y1,x2,y2)
        self.mgL_lrx = RO.TLegend(x1,y1,x2,y2)


        self.dcount = 0  #used for setting plot variables
        
        
        for k in self.item_list:
            print("Creating plot for ",k)
            self.ScanRXTX1(k)
    
    def Make2DGraph(self,devicename,variable1,variable2):
        """this returns a 2d graph of the 2 variables"""
        
        # read in the values 
        time = array('f')
        x = array('f')
        y = array('f')
       
        deltaT = array('f')
        newtime = array('f')
        newx = array('f')
        newy = array('f')
       
        for k in range(0,self.myentries):
            self.mychain.GetEntry(k) 
            if(self.mychain.deviceName==devicename):
                time.append(self.GetTimeStamp(self.mychain.dtCreate))
                exec('x.append(self.mychain.%s)' % variable1)
                exec('y.append(self.mychain.%s)' % variable2)
   
                   #exec('h1.Fill(entry.%s)' % variable)
 
        #now normalize on seconds
       
        count=0 
        #check for only one entry:
        if(len(time)<2):
            #print(devicename, len(time))
            self.ErrorHandle(100, devicename)
            return   
        for k in range(0,len(time)-1):    
            
            deltaT.append(time[k+1] - time[k])
            if(deltaT[count] != 0.):
                newtime.append(deltaT[count]/2.+time[k]) # new time in the middle of the time window
                newx.append((x[k+1]-x[k])/deltaT[count]) # normalize to second
                newy.append((y[k+1]-y[k])/deltaT[count]) 
            count+=1

        
        
        #self.gr2 = RO.TGraph2D(len(newtime),newx,newy,newtime)
        self.gr2 = RO.TGraph(len(newtime),newx,newy)
        self.gr2.SetMarkerColor(3)
        self.gr2.SetMarkerStyle(24)
        #self.gr2.GetXaxis().SetTimeDisplay(1);
        #self.gr2.GetXaxis().SetTimeFormat(self.tfmt);        
       
        
    def MakeCanvas(self):
        
        self.c1=TCanvas('c1','LCWA1 Canvas', 200, 10, 700, 500 ) 
 
        self.c2=TCanvas('c2','LCWA2 Canvas', 200, 600, 700, 500 ) 
        return

    def MakeCut(self,cut_expression):
        """ create cuts for selection"""
        c1 = TCut(cut_expression)
        
        return c1
    
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
            
        print(self.timecut)    
 

    def ReadCutList(self,cutfile):
        if path.exists(self.myhome+cutfile):
            with open(self.myhome+cutfile) as f:
                data=f.read()
            self.cutlist=json.loads(data)
            print(self.cutlist)
        else:
            self.ErrorHandle(1,info=cutfile)

    def ReadTree(self):
        
         #Get Number of entries:
        self.mychain = self.myrootfile.Get('example_tree')
        self.myentries = self.mychain.GetEntriesFast()
        
        print(' We have ',self.myentries,' entries')

        return
    
           
    def ScanVar(self,var,colsize=None):
        """ scans the tree for specific variable"""

        if colsize == None:
            self.mychain.Scan(var)
        else:
            width ="colsize="+str(colsize)
            #make sure you don't have a sapce between the colsize and the = sign
            self.mychain.Scan(var,"",width)
        return
    
         
        
        
    
    def ScanRXTX(self, devicename):
        """print tx and RX for a give device"""
        
        #we loop over all the entries
        # first we need to create a few arrays
        time = array('f')
        tx = array('f')
        rx = array('f')
        ltx = array('f')
        lrx = array('f')
       
        deltaT = array('f')
        newtime = array('f')
        newtx = array('f')
        newrx = array('f')
        newltx = array('f')
        newlrx = array('f')
        
        for k in range(0,self.myentries):
            self.mychain.GetEntry(k) 
            if(self.mychain.deviceName==devicename):
                time.append(self.GetTimeStamp(self.mychain.dtCreate))
                tx.append(self.mychain.wlanTxBytes)
                rx.append(self.mychain.wlanRxBytes)
                ltx.append(self.mychain.lanTxBytes)
                lrx.append(self.mychain.lanRxBytes)
         
        count=0 
        #check for only one entry:
        if(len(time)<2):
            #print(devicename, len(time))
            self.ErrorHandle(100, devicename)
            return   
        for k in range(0,len(time)-1):    
            
            deltaT.append(time[k+1] - time[k])
            if(deltaT[count] != 0.):
                newtime.append(deltaT[count]/2.+time[k])
                a =(tx[k+1]-tx[k])/deltaT[count]
                b =(rx[k+1]-rx[k])/deltaT[count]
                c =(ltx[k+1]-ltx[k])/deltaT[count]
                d =(lrx[k+1]-lrx[k])/deltaT[count]
                if a < 0.:
                    a=0
                if b < 0.:
                    b=0
                if c < 0.:
                    c=0
                if d < 0.:
                    d=0
                    
                 # new time in the middle of the time window
                newtx.append(a) # normalize to second
                newrx.append(b) 
                newltx.append(c) # normalize to second
                newlrx.append(d) 
                #print(newtime[count],newtx[count],newrx[count],newltx[count],newlrx[count])
            count+=1
             
       # setup first one dim histo:
        #get low x and high x
        tlow = newtime[0]
        thigh = newtime[len(newtime)-1]
        nchan = 100
        
        
        tfmt = self.tfmt
       
        
        temp_tx=RO.TGraph(len(newtime),newtime,newtx)
        temp_rx=RO.TGraph(len(newtime),newtime,newrx)
        temp_ltx=RO.TGraph(len(newtime),newtime,newltx)
        temp_lrx=RO.TGraph(len(newtime),newtime,newlrx)
        
        self.TG2D = RO.TGraph2D(len(newtime),newltx,newrx,newtime)
        self.TG2D.GetZaxis().SetTimeDisplay(1);
        self.TG2D.GetZaxis().SetTimeFormat(tfmt);  
        self.TG2D.GetXaxis().SetTitle("TX")      
        self.TG2D.GetYaxis().SetTitle("RX")  
        self.TG2D.SetMarkerStyle(21)
        self.TG2D.SetMarkerColor(2)   
        
        # make a multigraph
        
        # work on the graphs
        temp_tx.SetTitle(devicename+'_wlantx')
        temp_tx.SetMarkerColor(2)
        temp_tx.SetMarkerStyle(21)
        temp_tx.GetXaxis().SetTimeDisplay(1);
        temp_tx.GetXaxis().SetTimeFormat(tfmt);        

        temp_rx.SetTitle(devicename+'_wlanrx')
        temp_rx.SetMarkerColor(3)
        temp_rx.SetMarkerStyle(22)
        temp_rx.GetXaxis().SetTimeDisplay(1);
        temp_rx.GetXaxis().SetTimeFormat(tfmt);        

        temp_ltx.SetTitle(devicename+'_lantx')
        temp_ltx.SetMarkerColor(4)
        temp_ltx.SetMarkerStyle(23)
        temp_ltx.GetXaxis().SetTimeDisplay(1);
        temp_ltx.GetXaxis().SetTimeFormat(tfmt);        
 
        temp_lrx.SetTitle(devicename+'_lanlrx')
        temp_lrx.SetMarkerColor(5)
        temp_lrx.SetMarkerStyle(24)
        temp_lrx.GetXaxis().SetTimeDisplay(1);
        temp_lrx.GetXaxis().SetTimeFormat(tfmt);        
           
        self.graph1.append(temp_tx)
        self.graph1.append(temp_rx)
        self.graph1.append(temp_ltx)
        self.graph1.append(temp_lrx)
       
       # create multigraph and add to list
        multigraph = RO.TMultiGraph()
        multigraph.Add(temp_tx)
        multigraph.Add(temp_rx)
        multigraph.Add(temp_ltx)
        multigraph.Add(temp_lrx)
        if(self.compare):
            multigraph.Add(self.multispeed)
        multigraph.GetXaxis().SetTimeDisplay(1);
        multigraph.GetXaxis().SetTimeFormat(tfmt); 
        multigraph.GetXaxis().SetNdivisions(504,False) 
      
        
        self.multig.append(multigraph)

        #create Legend
        x1 = .1
        y1 = .7 
        x2 = .48
        y2 = .9
        mgL = RO.TLegend(x1,y1,x2,y2)
        mgL.SetHeader('tx and rx on lan and wlan  '+devicename)
        mgL.AddEntry(temp_tx,"wlan tx","P")
        mgL.AddEntry(temp_rx,"wlan rx","P")
        mgL.AddEntry(temp_ltx,"lan tx","P")
        mgL.AddEntry(temp_lrx,"lan rx","P")
        if(self.compare):
            mgL.AddEntry(self.speedup,"speedbox upload","P")
            mgL.AddEntry(self.speeddown,"speedbox download","P")
            
        self.multigL.append(mgL)
       
       
       
    def ScanRXTX1(self,devicename):
              #we loop over all the entries
        # first we need to create a few arrays
        # try to have time in MST
        GMT = 7*3600.
        

        time = array('f')
        tx = array('f')
        rx = array('f')
        ltx = array('f')
        lrx = array('f')
       
        deltaT = array('f')
        newtime = array('f')
        newtx = array('f')
        newrx = array('f')
        newltx = array('f')
        newlrx = array('f')
        
        for k in range(0,self.myentries):
            self.mychain.GetEntry(k) 
            if(self.mychain.deviceName==devicename) and  self.GetTimeStamp(self.mychain.dtCreate)>self.timecut[0] and self.GetTimeStamp(self.mychain.dtCreate)<self.timecut[1]:

                time.append(self.GetTimeStamp(self.mychain.dtCreate))
                tx.append(self.mychain.wlanTxBytes)
                rx.append(self.mychain.wlanRxBytes)
                ltx.append(self.mychain.lanTxBytes)
                lrx.append(self.mychain.lanRxBytes)
         
        count=0 
        #check for only one entry:
        if(len(time)<2):
            #print(devicename, len(time))
            self.ErrorHandle(100, devicename)
            return   
        for k in range(0,len(time)-1):    
            
            deltaT.append(time[k+1] - time[k])
            if(deltaT[count] != 0.):
                newtime.append((deltaT[count]/2.+time[k]-GMT)) # new time in the middle of the time window

                a =(tx[k+1]-tx[k])/deltaT[count]
                b =(rx[k+1]-rx[k])/deltaT[count]
                c =(ltx[k+1]-ltx[k])/deltaT[count]
                d =(lrx[k+1]-lrx[k])/deltaT[count]
                if a < 0.:
                    a=0.
                if b < 0.:
                    b=0.
                if c < 0.:
                    c=0.
                if d < 0.:
                    d=0.
                    
                 # new time in the middle of the time window
                newtx.append(a) # normalize to second
                newrx.append(b) 
                newltx.append(c) # normalize to second
                newlrx.append(d) 

                
                
                
                
                
                
                 #print(newtime[count],newtx[count],newrx[count],newltx[count],newlrx[count])
            count+=1
             
       # setup first one dim histo:
        #get low x and high x
        tlow = newtime[0]
        thigh = newtime[len(newtime)-1]
        nchan = 100
        
        
        tfmt = self.tfmt
       
        
        temp_tx=RO.TGraph(len(newtime),newtime,newtx)
        temp_rx=RO.TGraph(len(newtime),newtime,newrx)
        temp_ltx=RO.TGraph(len(newtime),newtime,newltx)
        temp_lrx=RO.TGraph(len(newtime),newtime,newlrx)
        
        
        temp_tx.SetTitle(devicename+'_wlantx')
        temp_tx.SetMarkerColor(self.dcount+2)
        temp_tx.SetMarkerStyle(self.dcount+21)
        temp_tx.GetXaxis().SetTimeDisplay(1);
        temp_tx.GetXaxis().SetTimeFormat(self.tfmt);        

        temp_rx.SetTitle(devicename+'_wlanrx')
        temp_rx.SetMarkerColor(self.dcount+2)
        temp_rx.SetMarkerStyle(self.dcount+21)
        temp_rx.GetXaxis().SetTimeDisplay(1);
        temp_rx.GetXaxis().SetTimeFormat(self.tfmt);        

        temp_ltx.SetTitle(devicename+'_lantx')
        temp_ltx.SetMarkerColor(self.dcount+2)
        temp_ltx.SetMarkerStyle(self.dcount+21)
        temp_ltx.GetXaxis().SetTimeDisplay(1);
        temp_ltx.GetXaxis().SetTimeFormat(self.tfmt);        
 
        temp_lrx.SetTitle(devicename+'_lanrx')
        temp_lrx.SetMarkerColor(self.dcount+2)
        temp_lrx.SetMarkerStyle(self.dcount+21)
        temp_lrx.GetXaxis().SetTimeDisplay(1);
        temp_lrx.GetXaxis().SetTimeFormat(self.tfmt);        


        self.multigraph_wtx.Add(temp_tx)
        self.multigraph_wrx.Add(temp_rx)
        self.multigraph_ltx.Add(temp_ltx)
        self.multigraph_lrx.Add(temp_lrx)
#legend dimensions
        self.mgL_tx.SetHeader('tx wlan')
        self.mgL_rx.SetHeader('rx wlan')
        self.mgL_ltx.SetHeader('tx lan')
        self.mgL_lrx.SetHeader('rx lan')
        self.mgL_tx.AddEntry(temp_tx,"wlan tx"+devicename,"P")
        self.mgL_rx.AddEntry(temp_rx,"wlan rx"+devicename,"P")
        self.mgL_ltx.AddEntry(temp_ltx,"lan tx"+devicename,"P")
        self.mgL_lrx.AddEntry(temp_lrx,"lan rx"+devicename,"P")

        #temp_rx.Delete()
        #temp_tx.Delete()
        #temp_lrx.Delete()
        #temp_ltx.Delete()

        self.dcount+=1
 #here are the utilities functions
 
        
    def ErrorHandle(self,count,info=None):
        """
        Prints out error message and perfoms action
        if the error count is below 100
        the program exits
        """
        #control chracaters for bf
        bfi = " \033[1m "
        bfo = " \033[0m "
        
        
        message =['' for i in range(500)]
        message[0] = 'Problem with rootfile'
        message[1] = 'Problem with Cutfile'
        message[100] = ' not enough data  in plot '
        
        errstr = 'LCWA_c error number > '
        
        print(errstr,count,'  ',message[count],' ',info)
        if(count < 100):
            # this is a reason to exit
            s = ' \n\n\n ************** Severe error, exiting *********'
            print(bfi+s+bfo)
            sys.exit()
        else:
            return
    
        
        

if __name__ == '__main__':

    import ROOT
    ROOT.gROOT.Reset()
    appi=ROOT.gApplication
    
    MyT = MyReadTree("/Users/klein/LCWA/data/new/devicedetail.root")
 
    MyT.ReadTree()
    MyT.GetBranchList()

    #MyT.CreateHisto11('lanTxBytes',name = 'histo1',title = "lanTxBytes",nchan=50,lowx=0.,highx=1.e12)
    #MyT.CreateHisto22('lanTxBytes','lanRxBytes',name = 'histo100',title = "lanTxBytes vs lanRXBytes",nchan=50,lowx=0.,highx=1e12,nchan1=50,lowx1=0.,highx1=1e12)

    MyT.ReadCutList("LCWA/data/cutlist.txt")
    #MyT.DrawVariable("lanRxBytes",devicename = 'AF-Vail')
    #MyT.DrawVariable("lanRxBytes",cut_expression='test1',devicename = 'madre-de-dios')

    #MyT.GetDeviceList()

    #MyT.GetSpeedBoxFile('/Users/klein/scratch/LC04_2020-12-14speedfile.csv' )
    #MyT.ScanRXTX("RidgeRoad5")



    MyT.MakeTimeCut(time_low="2021-01-04 00:32:51", time_high="2021-01-4 18:32:51")

    #devicelist = [ 'madre-de-dios', 'RidgeRoad5', 'camp-stoney', 'camp-stoney-2', 'hampton-road-986', 'la-posta', 'la-posta-0', 'la-posta-4', 'la-posta-5', 'old-santa-fe-trail', 'old-santa-fe-trail-1216', 'old-santa-fe-trail-14', 'stone-canyon-road-1120', 'wild-turkey-way']    
    #devicelist = [ 'camp-stoney', 'camp-stoney-2','wild-turkey-way']    

    devicelist = [  'camp-stoney', 'camp-stoney-2', 'hampton-road-986', 'la-posta', 'la-posta-0', 'la-posta-4', 'la-posta-5', 'old-santa-fe-trail', 'old-santa-fe-trail-1216', 'old-santa-fe-trail-14', 'stone-canyon-road-1120', 'wild-turkey-way']    

    MyT.LoopScanRXTX(devicelist = devicelist)
    #MyT.ScanVar("dtCreate", colsize=40)
    #MyT.GetTimeStamp("2016-12-14 22:58:47")
    #MyT.GetNameFromIP("172.16.8.8")
    #MyT.GetIPFromName("SpiritRidgeJicarrillaRidge")
    #MyT.Make2DGraph("madre-de-dios", 'wlanTxBytes', 'wlanRxBytes')
    MyT.DrawGraph1()
    #MyT.CloseApp()
    #MyT.DrawVariable("lanTxBytes","mydevice")
    #MyT.DrawVariable2("lanTxBytes:lanRxBytes","mydevice")
    #MyT.FillTree()
    appi.Run()    
    
    
    
