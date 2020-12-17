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
        self.MakeCanvas() 
        
        
        # get home directory

        self.myhome = expanduser("~") +'/' 
 
        self.histo1 = []  #list of one dimensional histos
        self.histo100 = [] #list of two dimensional histos
        self.graph1 = []  #list of one dimensional histos for tx and rx
        self.graph200 = [] #list of two dimensional histos
            
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
 
    
        
    def DrawVariable(self,variable,cut_expression = None):
        #1 dimensional drawing
        self.c3=TCanvas('c3','LCWA3 Canvas', 950, 10, 700, 500 ) 

        self.c3.cd()
        
        if(cut_expression != None):
            self.mychain.Draw(variable,self.MakeCut(self.cutlist[cut_expression]))
        else:
            self.mychain.Draw(variable)
         
        self.c3.Modified()
        self.c3.Update()
        
      

    def DrawVariable2(self,variable1,cut_expression = None):
        #1 dimensional drawing
        self.c4=TCanvas('c4','LCWA4 Canvas', 950, 600, 700, 500 ) 

        self.c4.cd()
        
        if(cut_expression != None):
            self.mychain.Draw(variable1,self.MakeCut(self.cutlist[cut_expression]))
        else:
            self.mychain.Draw(variable1)
         
        self.c4.Modified()
        self.c4.Update()

    def DrawHisto(self):
        """ draws the one and two dimensional histos"""
        #self.c1.Draw()


    
        count = 0
        self.c1.Divide(2,2,0,0)
        #self.c1.Draw()
        for k in self.graph1:
            self.c1.cd(count+1)
            #self.c1.Draw()
            k.Draw("AP")
            count+=1
            #a = input("press any character to continue")
        self.c1.Modified()
        self.c1.Update()
        self.c1.Draw()
 
        self.c2.cd()
        self.multigraph.Draw("AP")
        self.mgL.Draw()
        self.c2.Modified()
        self.c2.Update()
        self.c2.Draw()
        
        
        
        #for k in self.histo100:
        #    self.c2.cd()
        #    self.c2.Draw()
        #    k.Draw()
        #    self.c2.Modified()
        #    self.c2.Update()
            #a = input("press any character to continue")
            

    def GetBranchList(self):
        """ Get list of branches"""
        self.Blist = []

        self.branches_list = self.mychain.GetListOfBranches() #this is an iterator TobjArray

        
        for k in range(0,len(self.branches_list)):
            self.Blist.append(self.branches_list.At(k).GetName())
        
        print(self.Blist)
     
    

    
    def GetTimeStamp(self,mytime):
        """calculates the unix time stamp"""
        temp = time.mktime(datetime.datetime.strptime(mytime, "%Y-%m-%d %H:%M:%S").timetuple())
        
            
        
        return temp

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
        for k in range(0,len(time)-1,2):    
            
            deltaT.append(time[k+1] - time[k])
            if(deltaT[count] != 0.):
                newtime.append(deltaT[count]/2.+time[k]) # new time in the middle of the time window
                newtx.append((tx[k+1]-tx[k])/deltaT[count]) # normalize to second
                newrx.append((rx[k+1]-rx[k])/deltaT[count]) 
                newltx.append((ltx[k+1]-ltx[k])/deltaT[count]) # normalize to second
                newlrx.append((lrx[k+1]-lrx[k])/deltaT[count]) 
                #print(newtime[count],newtx[count],newrx[count],newltx[count],newlrx[count])
                count+=1
                
        # setup first one dim histo:
        #get low x and high x
        tlow = newtime[0]
        thigh = newtime[len(newtime)-1]
        nchan = 100
        
        
        
        #temp_tx = RO.TH1F(devicename+'tx',devicename+'tx',nchan,tlow,thigh)
        #temp_rx = RO.TH1F(devicename+'rx',devicename+'rx',nchan,tlow,thigh)
        #temp_ltx = RO.TH1F(devicename+'ltx',devicename+'ltx',nchan,tlow,thigh)
        #temp_lrx = RO.TH1F(devicename+'lrx',devicename+'lrx',nchan,tlow,thigh)

        temp_tx=RO.TGraph(len(newtime),newtime,newtx)
        temp_rx=RO.TGraph(len(newtime),newtime,newrx)
        temp_ltx=RO.TGraph(len(newtime),newtime,newltx)
        temp_lrx=RO.TGraph(len(newtime),newtime,newlrx)
        
        # make a multigraph
        
        
        # work on the graphs
        temp_tx.SetTitle(devicename+'_wlantx')
        temp_tx.SetMarkerColor(2)
        temp_tx.SetMarkerStyle(21)
        
        temp_rx.SetTitle(devicename+'_wlanrx')
        temp_rx.SetMarkerColor(3)
        temp_rx.SetMarkerStyle(22)

        temp_ltx.SetTitle(devicename+'_lantx')
        temp_ltx.SetMarkerColor(4)
        temp_ltx.SetMarkerStyle(23)
 
        temp_lrx.SetTitle(devicename+'_lanlrx')
        temp_lrx.SetMarkerColor(5)
        temp_lrx.SetMarkerStyle(24)
        
        # Now fill the histos
        #for k in range(0,len(newtime)-1):
        #    temp_tx.Fill(newtime,newtx)
        #    temp_rx.Fill(newtime,newrx)
        #    temp_ltx.Fill(newtime,newltx)
        #    temp_lrx.Fill(newtime,newlrx)
            
        self.graph1.append(temp_tx)
        self.graph1.append(temp_rx)
        self.graph1.append(temp_ltx)
        self.graph1.append(temp_lrx)
       
       # create multigraph
        self.multigraph = RO.TMultiGraph()
        self.multigraph.Add(temp_tx)
        self.multigraph.Add(temp_rx)
        self.multigraph.Add(temp_ltx)
        self.multigraph.Add(temp_lrx)
        #create Legend
        x1 = .1
        y1 = .7 
        x2 = .48
        y2 = .9
        self.mgL = RO.TLegend(x1,y1,x2,y2)
        self.mgL.SetHeader('tx and rx on lan and wlan  '+devicename)
        self.mgL.AddEntry(temp_tx,"wlan tx","P")
        self.mgL.AddEntry(temp_rx,"wlan rx","P")
        self.mgL.AddEntry(temp_ltx,"lan tx","P")
        self.mgL.AddEntry(temp_lrx,"lan rx","P")
       
       
       
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
        
        
        message =[500]
        message[0] = 'Problem with rootfile'
        message[1] = 'Problem with Cutfile'
        
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
    MyT.MakeTimeCut(time_low="2020-06-21 00:32:51", time_high="2020-12-21 00:32:51")
    #MyT.DrawVariable("lanRxBytes")

    #MyT.CreateHisto11('lanTxBytes',name = 'histo1',title = "lanTxBytes",nchan=50,lowx=0.,highx=1.e12)
    #MyT.CreateHisto22('lanTxBytes','lanRxBytes',name = 'histo100',title = "lanTxBytes vs lanRXBytes",nchan=50,lowx=0.,highx=1e12,nchan1=50,lowx1=0.,highx1=1e12)

    MyT.ReadCutList("LCWA/data/cutlist.txt")
    MyT.ScanRXTX("madre-de-dios")
    
    #MyT.ScanVar("dtCreate", colsize=40)
    #MyT.GetTimeStamp("2016-12-14 22:58:47")
    #MyT.GetNameFromIP("172.16.8.8")
    #MyT.GetIPFromName("SpiritRidgeJicarrillaRidge")
    MyT.DrawHisto()
    #MyT.CloseApp()
    #MyT.DrawVariable("lanTxBytes","mydevice")
    #MyT.DrawVariable2("lanTxBytes:lanRxBytes","mydevice")
    #MyT.FillTree()
    appi.Run()            
