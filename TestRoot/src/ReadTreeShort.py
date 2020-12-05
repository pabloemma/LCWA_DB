'''
Created on Dec 5, 2020

@author: klein
'''

import ROOT as RO
from ROOT import  TFile, TCut, TCanvas, TH1F,TH2F
#import strucDef
import array




from os import path 
from os.path import expanduser

import time
import datetime
import sys
import json # needed for reading in cutfiles. They are written as a dictionary

class MyReadTreeSh(object):
    '''
    classdocs
    '''


    def __init__(self, rootfile):
        '''
        Constructor
        '''
        
        if path.exists(rootfile):
            self.myrootfile = TFile(rootfile,"r")
        else:
            self.ErrorHandle(0,info=rootfile)
         
        
        # get home directory

        self.myhome = expanduser("~") +'/' 
 
#        RO.gApplication.Run() 
        self.histo1 = []  #list of one dimensional histos
        self.histo100 = [] #list of two dimensional histos
           
    def CreateHisto11(self,variable,name='histo1',title='histo1',nchan=50,lowx=0.,highx=1000.):
        h1 = TH1F(name,title,nchan,lowx,highx)
        for entry in self.mychain:
            if self.GetTimeStamp(entry.dtCreate)>self.timecut[0] and self.GetTimeStamp(entry.dtCreate)<self.timecut[1]:
                exec('h1.Fill(entry.%s)' % variable)
 
        self.histo1.append(h1)
         

    def CreateHisto22(self,variable1,variable2,name='histo100',title='histo100',nchan=50,lowx=0.,highx=1e12,nchan1=50,lowx1=0.,highx1=1e12):
        h100 = TH2F(name,title,nchan,lowx,highx,nchan1,lowx1,highx1)
        for entry in self.mychain:
            if self.GetTimeStamp(entry.dtCreate)>self.timecut[0] and self.GetTimeStamp(entry.dtCreate)<self.timecut[1]:
                exec('h100.Fill(entry.%s,entry.%s)' % (variable1 , variable2))
            
        self.histo100.append(h100)

    def DrawHisto(self):
        """ draws the one and two dimensional histos"""
        
        self.c1.Draw()
    
  
  
        for k in self.histo100:
            self.c1.cd()
            self.c1.Draw()
            k.Draw()
            self.c1.Modified()
            self.c1.Update()
            a = input("press any character to continue")

        for k in self.histo1:
            self.c1.cd()
            self.c1.Draw()
            k.Draw()
            self.c1.Modified()
            self.c1.Update()
            a = input("press any character to continue")
        
    def GetTimeStamp(self,mytime):
        """calculates the unix time stamp"""
        temp = time.mktime(datetime.datetime.strptime(mytime, "%Y-%m-%d %H:%M:%S").timetuple())
 
        return temp
 
    def MakeCanvas(self):
        
        self.c1=TCanvas('c1','LCWA Canvas', 200, 10, 700, 500 ) 
        self.c1.Draw()
        return

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
    
    
    def ReadTree(self):
        
         #Get Number of entries:
        self.mychain = self.myrootfile.Get('example_tree')
        self.myentries = self.mychain.GetEntriesFast()
        
        print(' We have ',self.myentries,' entries')

        return
if __name__ == '__main__':
    import ROOT
    ROOT.gROOT.Reset()
    appi=ROOT.gApplication
    
    filename = ("/Users/klein/kun/device_detail_sh1.root")
    
    MyT = MyReadTreeSh(filename)
 
    MyT.ReadTree()
    MyT.MakeCanvas()
    MyT.MakeTimeCut(time_low="2020-06-21 00:32:51", time_high="2020-12-21 00:32:51")
    #MyT.DrawVariable("lanRxBytes")

    MyT.CreateHisto11('lanTxBytes',name = 'histo1',title = "lanTxBytes",nchan=50,lowx=0.,highx=1.e12)
    MyT.CreateHisto22('lanTxBytes','lanRxBytes',name = 'histo100',title = "lanTxBytes vs lanRXBytes",nchan=50,lowx=0.,highx=1e12,nchan1=50,lowx1=0.,highx1=1e12)
    MyT.DrawHisto()
    appi.Run()
 