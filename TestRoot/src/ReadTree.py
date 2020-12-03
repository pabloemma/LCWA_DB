'''
Created on Dec 2, 2020

@author: klein
'''

import ROOT as RO
from ROOT import  TFile, TCut, TCanvas

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
        
        if path.exists(rootfile):
            self.myrootfile = TFile(rootfile,"r")
        else:
            self.ErrorHandle(0,info=rootfile)
         
        # Create default Canvas
        self.MakeCanvas() 
        
        
        # get home directory

        self.myhome = expanduser("~") +'/' 
            
    
    def DrawVariable(self,variable,cut_expression = None):
        #1 dimensional drawing
        self.c1.cd()
        
        if(cut_expression != None):
            self.mychain.Draw(variable,self.MakeCut(self.cutlist[cut_expression]))
        else:
            self.mychain.Draw(variable)
        
        self.c1.Modified()
        self.c1.Update()
        RO.gApplication.Run()  


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
        print(temp)
        return temp


    def MakeCanvas(self):
        
        self.c1=TCanvas('c1','LCWA Canvas', 200, 10, 700, 500 ) 
        return

    def MakeCut(self,cut_expression):
        """ create cuts for selection"""
        c1 = TCut(cut_expression)
        
        return c1
 

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
    #if len(sys.argv) < 2:
    #    print("Usage: %s file_to_parse.dat" % sys.argv[0])
    #    sys.exit(1)
    #parse_CSV_file_with_TTree_ReadStream("example_tree", sys.argv[1])
    
    MyT = MyReadTree("/Users/klein/LCWA/data/device_detail.root")
    MyT.ReadTree()
    MyT.GetBranchList()
    
    MyT.ReadCutList("LCWA/data/cutlist.txt")
    
    MyT.ScanVar("dtCreate", colsize=40)
    MyT.GetTimeStamp("2016-12-14 22:58:47")
    MyT.DrawVariable("lanRxBytes","mydevice")
    
    #MyT.FillTree()
                    
