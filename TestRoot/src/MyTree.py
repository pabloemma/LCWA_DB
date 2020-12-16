'''
Created on Nov 30, 2020

@author: klein
Running version
'''

import ROOT
from ROOT import TFile, TTree, gROOT, addressof 
import os
import sys
#import numpy as np
from array  import array

gROOT.ProcessLine(
            "struct info_t {\
           Char_t          afDuplex[30];\
           Char_t          afLinkState[20];\
           Char_t          afOpmode[20];\
           Char_t          afTxmodrate[5];\
           Char_t          apMac[30];\
           Char_t          boardCrc[30];\
           Char_t          cfgCrc[20];\
           Char_t           deviceID[30];\
           Char_t           deviceIp[20];\
           Char_t          deviceName[60];\
           Char_t           dtCreate[30];\
           Char_t          essid[40];\
           Char_t          firmwareVersion[60];\
           Char_t          lanIpAddress[20];\
           Char_t          lanSpeed[15];\
           Char_t           latitude[20];\
           Char_t           longitude[20];\
           Char_t           platform[40];\
           Char_t           remoteIP[20];\
           Char_t           remoteMac[20];\
           Char_t           rxModRate[20];\
           Char_t           txModRate[20];\
           Char_t            wlanIpAddress[20];\
           Char_t            wlanOpmode[15];\
                                        };" );
   







class MyTree(object):
    '''
    classdocs
    '''


    def __init__(self, afile = None,tree_name = None):
        '''
        Constructor
        '''
     
    # Handling the input and output names.  Using the same
    # base name for the ROOT output file.
        output_ROOT_file_name  = os.path.splitext(afile)[0] + '.root'
        self.output_file            = ROOT.TFile(output_ROOT_file_name, 'recreate')
        print("Outputting %s -> %s" % (afile, output_ROOT_file_name))

        self.output_tree            = ROOT.TTree(tree_name, tree_name)
        
        self.file_lines = []
        file1 = open(afile,'r')
        
        count=0
        while True:
            count += 1
            line = str(file1.readline())
            
            #If line is empty we reached EOFError
            if not line:
                break
            else: 
                self.file_lines.append(line)
         
        self.sign = 'LCWA_c> '
     
    def CreateTree1(self):
        info = ROOT.info_t()
    
    
        iddevicedetail =  array('f',[0]) 
        afRxcapacity =  array('f',[0]) 
        afRxchanbw =  array('f',[0]) 
        afRxfreq =  array('f',[0]) 
        afRxpower0 =  array('f',[0]) 
        afRxpower1 =  array('f',[0]) 
        afTxcapacity =  array('f',[0]) 
        afTxchanbw =  array('f',[0]) 
        afTxfreq =  array('f',[0]) 
        afTxpower =  array('f',[0]) 
        afTxpowerEirp =  array('f',[0]) 
        airTime =  array('f',[0]) 
        altitude =  array('f',[0]) 
        chain0Signal =  array('f',[0]) 
        chain1Signal =  array('f',[0]) 
        chanbw =  array('f',[0]) 
        cinr =  array('f',[0]) 
        cpuUsage =  array('f',[0]) 
        distance =  array('f',[0]) 
        evm =  array('f',[0]) 
        freq =  array('f',[0]) 
        gpsFixed =  array('f',[0]) 
        lanPlugged =  array('f',[0]) 
        lanRxBytes =  array('f',[0]) 
        lanRxErrors =  array('f',[0]) 
        lanRxPackets =  array('f',[0]) 
        lanTxBytes =  array('f',[0]) 
        lanTxErrors =  array('f',[0]) 
        lanTxPackets =  array('f',[0]) 
        loadavg =  array('f',[0]) 
        memBuffers =  array('f',[0]) 
        memFree =  array('f',[0]) 
        memTotal =  array('f',[0]) 
        noise =  array('f',[0]) 
        signal =  array('f',[0]) 
        status_flags =  array('f',[0]) 
        uptime =  array('f',[0]) 
        wlanConnections =  array('f',[0]) 
        wlanDownlinkCapacity =  array('f',[0]) 
        wlanPolling =  array('f',[0]) 
        wlanRxBytes =  array('f',[0]) 
        wlanRxErrBmiss =  array('f',[0]) 
        wlanRxErrCrypt =  array('f',[0]) 
        wlanRxErrFrag =  array('f',[0]) 
        wlanRxErrNwid =  array('f',[0]) 
        wlanRxErrors =  array('f',[0]) 
        wlanRxErrOther =  array('f',[0]) 
        wlanRxErrRetries =  array('f',[0]) 
        wlanRxPackets =  array('f',[0]) 
        wlanRxRate =  array('f',[0]) 
        wlanTxBytes =  array('f',[0]) 
        wlanTxErrors =  array('f',[0]) 
        wlanTxLatency =  array('f',[0]) 
        wlanTxPackets =  array('f',[0]) 
        wlanTxRate =  array('f',[0]) 
        wlanUplinkCapacity =  array('f',[0])     

    
        self.output_tree.Branch("iddevicedetail",iddevicedetail,'iddevicedetail/F')
        self.output_tree.Branch("afDuplex",addressof(info,'afDuplex'),'afDuplex/C')
        self.output_tree.Branch("afLinkState",addressof(info,'afLinkState'),'afLinkState/C')
        self.output_tree.Branch("afOpmode",addressof(info,'afOpmode'),'afOpmode/C')
        self.output_tree.Branch("afRxcapacity",afRxcapacity,'afRxcapacity/F')
        self.output_tree.Branch("afRxchanbw",afRxchanbw,'afRxchanbw/F')
        self.output_tree.Branch("afRxfreq",afRxfreq,'afRxfreq/F')
        self.output_tree.Branch("afRxpower0",afRxpower0,'afRxpower0/F')
        self.output_tree.Branch("afRxpower1",afRxpower1,'afRxpower1/F')
        self.output_tree.Branch("afTxcapacity",afTxcapacity,'afTxcapacity/F')
        self.output_tree.Branch("afTxchanbw",afTxchanbw,'afTxchanbw/F')
        self.output_tree.Branch("afTxfreq",afTxfreq,'afTxfreq/F')
        self.output_tree.Branch("afTxmodrate",addressof(info,'afTxmodrate'),'afTxmodrate/C')
        self.output_tree.Branch("afTxpower",afTxpower,'afTxpower/F')
        self.output_tree.Branch("afTxpowerEirp",afTxpowerEirp,'afTxpowerEirp/F')
        self.output_tree.Branch("airTime",airTime,'airTime/F')
        self.output_tree.Branch("altitude",altitude,'altitude/F')
        self.output_tree.Branch("apMac",addressof(info,'apMac'),'apMac/C')
        self.output_tree.Branch("boardCrc",addressof(info,'boardCrc'),'boardCrc/C')
        self.output_tree.Branch("cfgCrc",addressof(info,'cfgCrc'),'cfgCrc/C')
        self.output_tree.Branch("chain0Signal",chain0Signal,'chain0Signal/F')
        self.output_tree.Branch("chain1Signal",chain1Signal,'chain1Signal/F')
        self.output_tree.Branch("chanbw",chanbw,'chanbw/F')
        self.output_tree.Branch("cinr",cinr,'cinr/F')
        self.output_tree.Branch("cpuUsage",cpuUsage,'cpuUsage/F')
        self.output_tree.Branch("deviceID",addressof(info,'deviceID'),'deviceID/C')
        self.output_tree.Branch("deviceIp",addressof(info,'deviceIp'),'deviceIp/C')
        self.output_tree.Branch("deviceName",addressof(info,'deviceName'),'deviceName/C')
        self.output_tree.Branch("distance",distance,'distance/F')
        self.output_tree.Branch("dtCreate",addressof(info,'dtCreate'),'dtCreate/C')
        self.output_tree.Branch("essid",addressof(info,'essid'),'essid/C')
        self.output_tree.Branch("evm",evm,'evm/F')
        self.output_tree.Branch("firmwareVersion",addressof(info,'firmwareVersion'),'firmwareVersion/C')
        self.output_tree.Branch("freq",freq,'freq/F')
        self.output_tree.Branch("gpsFixed",gpsFixed,'gpsFixed/F')
        self.output_tree.Branch("lanIpAddress",addressof(info,'lanIpAddress'),'lanIpAddress/C')
        self.output_tree.Branch("lanPlugged",lanPlugged,'lanPlugged/F')
        self.output_tree.Branch("lanRxBytes",lanRxBytes,'lanRxBytes/F')
        self.output_tree.Branch("lanRxErrors",lanRxErrors,'lanRxErrors/F')
        self.output_tree.Branch("lanRxPackets",lanRxPackets,'lanRxPackets/F')
        self.output_tree.Branch("lanSpeed",addressof(info,'lanSpeed'),'lanSpeed/C')
        self.output_tree.Branch("lanTxBytes",lanTxBytes,'lanTxBytes/F')
        self.output_tree.Branch("lanTxErrors",lanTxErrors,'lanTxErrors/F')
        self.output_tree.Branch("lanTxPackets",lanTxPackets,'lanTxPackets/F')
        self.output_tree.Branch("latitude",addressof(info,'latitude'),'latitude/C')
        self.output_tree.Branch("loadavg",loadavg,'loadavg/F')
        self.output_tree.Branch("longitude",addressof(info,'longitude'),'longitude/C')
        self.output_tree.Branch("memBuffers",memBuffers,'memBuffers/F')
        self.output_tree.Branch("memFree",memFree,'memFree/F')
        self.output_tree.Branch("memTotal",memTotal,'memTotal/F')
        self.output_tree.Branch("noise",noise,'noise/F')
        self.output_tree.Branch("platform",addressof(info,'platform'),'platform/C')
        self.output_tree.Branch("remoteIP",addressof(info,'remoteIP'),'remoteIP/C')
        self.output_tree.Branch("remoteMac",addressof(info,'remoteMac'),'remoteMac/C')
        self.output_tree.Branch("rxModRate",addressof(info,'rxModRate'),'rxModRate/C')
        self.output_tree.Branch("signal",signal,'signal/F')
        self.output_tree.Branch("status_flags",status_flags,'status_flags/F')
        self.output_tree.Branch("txModRate",addressof(info,'txModRate'),'txModRate/C')
        self.output_tree.Branch("uptime",uptime,'uptime/F')
        self.output_tree.Branch("wlanConnections",wlanConnections,'wlanConnections/F')
        self.output_tree.Branch("wlanDownlinkCapacity",wlanDownlinkCapacity,'wlanDownlinkCapacity/F')
        self.output_tree.Branch("wlanIpAddress",addressof(info,'wlanIpAddress'),'wlanIpAddress/C')
        self.output_tree.Branch("wlanOpmode",addressof(info,'wlanOpmode'),'wlanOpmode/C')
        self.output_tree.Branch("wlanPolling",wlanPolling,'wlanPolling/F')
        self.output_tree.Branch("wlanRxBytes",wlanRxBytes,'wlanRxBytes/F')
        self.output_tree.Branch("wlanRxErrBmiss",wlanRxErrBmiss,'wlanRxErrBmiss/F')
        self.output_tree.Branch("wlanRxErrCrypt",wlanRxErrCrypt,'wlanRxErrCrypt/F')
        self.output_tree.Branch("wlanRxErrFrag",wlanRxErrFrag,'wlanRxErrFrag/F')
        self.output_tree.Branch("wlanRxErrNwid",wlanRxErrNwid,'wlanRxErrNwid/F')
        self.output_tree.Branch("wlanRxErrors",wlanRxErrors,'wlanRxErrors/F')
        self.output_tree.Branch("wlanRxErrOther",wlanRxErrOther,'wlanRxErrOther/F')
        self.output_tree.Branch("wlanRxErrRetries",wlanRxErrRetries,'wlanRxErrRetries/F')
        self.output_tree.Branch("wlanRxPackets",wlanRxPackets,'wlanRxPackets/F')
        self.output_tree.Branch("wlanRxRate",wlanRxRate,'wlanRxRate/F')
        self.output_tree.Branch("wlanTxBytes",wlanTxBytes,'wlanTxBytes/F')
        self.output_tree.Branch("wlanTxErrors",wlanTxErrors,'wlanTxErrors/F')
        self.output_tree.Branch("wlanTxLatency",wlanTxLatency,'wlanTxLatency/F')
        self.output_tree.Branch("wlanTxPackets",wlanTxPackets,'wlanTxPackets/F')
        self.output_tree.Branch("wlanTxRate",wlanTxRate,'wlanTxRate/F')
        self.output_tree.Branch("wlanUplinkCapacity",wlanUplinkCapacity,'wlanUplinkCapacity/F')

        count = 0
            
        for line in (self.file_lines):
            if(count> 0):
                a=line.split(',')
                try:
                    a[79] = a[79].strip('\n')
                except:
                    print(count)
                for p in range(0,len(a)):
                    if(a[p] ==''):
                        a[p]='0.0'
                    
                    
                iddevicedetail[0] = float(a[0])
                info.afDuplex = a[1]
                info.afLinkState = a[2]
                info.afOpmode = a[3]
                afRxcapacity[0] = float(a[4])
                afRxchanbw[0] = float(a[5])
                afRxfreq[0] = float(a[6])
                afRxpower0[0] = float(a[7])
                afRxpower1[0] = float(a[8])
                afTxcapacity[0] = float(a[9])
                afTxchanbw[0] = float(a[10])
                afTxfreq[0] = float(a[11])
                info.afTxmodrate = a[12]
                afTxpower[0] = float(a[13])
                afTxpowerEirp[0] = float(a[14])
                airTime[0] = float(a[15])
                altitude[0] = float(a[16])
                info.apMac = a[17]
                info.boardCrc = a[18]
                info.cfgCrc = a[19]
                chain0Signal[0] = float(a[20])
                chain1Signal[0] = float(a[21])
                chanbw[0] = float(a[22])
                cinr[0] = float(a[23])
                cpuUsage[0] = float(a[24])
                info.deviceID = a[25]
                info.deviceIp = a[26]
                info.deviceName = a[27]
                distance[0] = float(a[28])
                info.dtCreate = a[29]
                info.essid = a[30]
                evm[0] = float(a[31])
                info.firmwareVersion = a[32]
                freq[0] = float(a[33])
                gpsFixed[0] = float(a[34])
                info.lanIpAddress = a[35]
                lanPlugged[0] = float(a[36])
                lanRxBytes[0] = float(a[37])
                lanRxErrors[0] = float(a[38])
                lanRxPackets[0] = float(a[39])
                info.lanSpeed = a[40]
                lanTxBytes[0] = float(a[41])
                lanTxErrors[0] = float(a[42])
                lanTxPackets[0] = float(a[43])
                info.latitude = a[44]
                loadavg[0] = float(a[45])
                info.longitude = a[46]
                memBuffers[0] = float(a[47])
                memFree[0] = float(a[48])
                memTotal[0] = float(a[49])
                noise[0] = float(a[50])
                info.platform = a[51]
                info.remoteIP = a[52]
                info.remoteMac = a[53]
                info.rxModRate = a[54]
                signal[0] = float(a[55])
                status_flags[0] = float(a[56])
                info.txModRate = a[57]
                uptime[0] = float(a[58])
                wlanConnections[0] = float(a[59])
                wlanDownlinkCapacity[0] = float(a[60])
                info.wlanIpAddress = a[61]
                info.wlanOpmode = a[62]
                wlanPolling[0] = float(a[63])
                wlanRxBytes[0] = float(a[64])
                wlanRxErrBmiss[0] = float(a[65])
                wlanRxErrCrypt[0] = float(a[66])
                wlanRxErrFrag[0] = float(a[67])
                wlanRxErrNwid[0] = float(a[68])
                wlanRxErrors[0] = float(a[69])
                wlanRxErrOther[0] = float(a[70])
                wlanRxErrRetries[0] = float(a[71])
                wlanRxPackets[0] = float(a[72])
                wlanRxRate[0] = float(a[73])
                wlanTxBytes[0] = float(a[74])
                wlanTxErrors[0] = float(a[75])
                wlanTxLatency[0] = float(a[76])
                wlanTxPackets[0] = float(a[77])
                wlanTxRate[0] = float(a[78])
                wlanUplinkCapacity[0]= float(a[79]) 
                
                self.output_tree.Fill()    

            count += 1
        
        self.output_file.Write()
        self.output_file.Close()
    
     
            
if __name__ == '__main__':
    #if len(sys.argv) < 2:
    #    print("Usage: %s file_to_parse.dat" % sys.argv[0])
    #    sys.exit(1)
    #parse_CSV_file_with_TTree_ReadStream("example_tree", sys.argv[1])
    MyT = MyTree(tree_name = "example_tree", afile = "/Users/klein/LCWA/data/new/devicedetail.csv")
    MyT.CreateTree1()





# crap

         