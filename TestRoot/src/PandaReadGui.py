'''
Created on Jan 21, 2021

@author: klein
'''
import wx
import sys
import os
import socket
import pprint
import subprocess as sp
import json
import yaml
from datetime import datetime
from asyncio.locks import Event
#from builtins import False

sys.path.insert(2,'/Users/klein/git/LCWA/src')
sys.path.insert(3,'/Users/klein/git/LCWA_UNMS/RRD_SNMP/src')


from PandaRead import PandaRead
from MyError import MyError 
from OutputFileDialog import OutputFileDialog


from pubsub import pub


class MyWindow(wx.Panel):
    """
    Creates a panel
    with a box sizer
    label: str for different Texctrl boxes
    
    
    """
    
    
    def __init__(self,parent,ID=-1,label="",pos =(800,200),size = (100,50)):
        wx.Panel.___init(self,parent,ID,pos,size,wx.RAISED_BORDER, label )
        
        self.label = label
        self.BackgroundColour("white")
        self.SetMinSize(size)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
    
    
    def OnPaint(self,event):
        sz = self.GetClientSize()
        dc = wx.PaintDC()
        w,h = dc.CanGetTextExtent(self.label)
        dc.SetFont(self.GetFont())
        dc.DrawText(self.label,(sz.width-w)/2,(sz.height-h)/2)
        
        
        

class MyFrame(wx.Frame):
    """
    The main Frame class
    """
    
    def __init__(self,parent,id,title):
        
        
        #define the Frame style
        mystyle = wx.DEFAULT_FRAME_STYLE | wx.STAY_ON_TOP
        
        
        
        wx.Frame.__init__(self,parent,id,title,style = mystyle)
     
     
             #instantiate UNMSControl
 
        
        self.version = 'Panda GUI Control for LCWA'
        self.author = 'Andi Klein'
        self.date = 'Winter 2020/21 '
        self.versionnumber = "0.1"
        now=datetime.now()
        self.dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        self.startline='MyTree >'
 
        panel = wx.Panel(self,-1)
        vs =wx.StaticText(panel,-1,self.version, (100,20),(160,-1),wx.ALIGN_LEFT)
        font1 = wx.Font(30,wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, True)
        font2 = wx.Font(30,wx.FONTFAMILY_MODERN, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_BOLD, True)
        vs.SetFont(font1)
        vk =wx.StaticText(panel,-1,self.author, (100,70),(160,-1),wx.ALIGN_LEFT)
        vl =wx.StaticText(panel,-1,self.date, (100,100),(160,-1),wx.ALIGN_LEFT)
        vm =wx.StaticText(panel,-1,self.versionnumber, (100,130),(160,-1),wx.ALIGN_CENTER)
        vn =wx.StaticText(panel,-1,self.dt_string, (100,160),(160,-1),wx.ALIGN_RIGHT)
        font = wx.Font(20,wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, True)
        vk.SetFont(font2)
        vl.SetFont(font)
        vm.SetFont(font)
        vn.SetFont(font)
   

        pub.subscribe(self.my_listener, "panel_listener") #for passing event handler back and forth

        
        self.CreateStatusBar()
        self.CreateToolBar()

        self.CreateMenu()

 
        self.ME=MyError()
        
        
        self.program_name = os.path.basename(__file__)
        
        
        #instantiate the PANDAREAD
        
        self.PRI = PandaRead()
        
        #log into the system
        #self.OnLogin(0)
        self.looplist = ['RidgeRoad5','madre-de-dios', 'camp-stoney', 'camp-stoney-2', 'hampton-road-986', 'la-posta', 'la-posta-0', 'la-posta-4', 'la-posta-5', 'old-santa-fe-trail', 'old-santa-fe-trail-1216', 'old-santa-fe-trail-14', 'stone-canyon-road-1120', 'wild-turkey-way']    

        self.ReduceList = ["apMac","cpuUsage","deviceIp","deviceName","dtCreate","lanRxBytes", \
              "lanRxErrors","lanRxPackets","lanTxBytes","lanTxErrors","lanTxPackets",\
              "loadavg","memBuffers","memFree","memTotal","remoteIP",\
              "remoteMac","wlanRxBytes","wlanRxErrors","wlanRxErrOther",\
              "wlanRxErrRetries","wlanRxPackets","wlanRxRate","wlanTxBytes",\
              "wlanTxErrors","wlanTxPackets","wlanTxRate"]

 
        # Set size of Frame
        
    def CreateMenu(self):
        """
        creates the menu on the frame
        """
        menubar = wx.MenuBar()
        



        
        # section for quit, file etc
        file_menu = wx.Menu()
        menubar.Append(file_menu,"&File \tCTRL+F")

        self.CreateMenuItem(file_menu, "Quit",self.OnExit)
        self.CreateMenuItem(file_menu, "Input File",self.OnOpenCSVFile)
        self.CreateMenuItem(file_menu, "Output file",self.OnSetOutputFile)

        #section for action
        #action_menu = wx.Menu()
        #menubar.Append(action_menu,"&Action \tCTRL+A")

        #self.CreateMenuItem(action_menu, "Login",self.OnLogin)
        #self.CreateMenuItem(action_menu, "Logout",self.OnLogout)
        
        
        #self.CreateMenuItem(action_menu, "Debug Level",self.OnDebugLevel)
        
        #action_menu.InsertSeparator(2)
        
        #section for services
        service_menu = wx.Menu()
        menubar.Append(service_menu,"Services")

        self.CreateMenuItem(service_menu, "Reduce Table",self.OnReduceTable)
        self.CreateMenuItem(service_menu, "Loop over devices",self.OnLoopDevices)
        self.CreateMenuItem(service_menu, "Get SpeedBoxFile",self.OnGetSpeedBoxFile)
        self.CreateMenuItem(service_menu, "Get Variables",self.OnGetVariables)
        self.CreateMenuItem(service_menu, "Set Device",self.OnSetDevice)
        
        self.CreateMenuItem(service_menu, "Create tests",self.OnSetTest)

        plot_menu = wx.Menu()
        menubar.Append(plot_menu,"plots")

        self.CreateMenuItem(plot_menu, "Draw variable",self.OnDrawVariable)



 
        #Help Menu
        help_menu = wx.Menu()
        menubar.Append(help_menu,"Help")
        #self.CreateMenuItem(help_menu, "General overview",self.OnHelpGeneral)

        self.CreateMenuItem(help_menu, "General overview",self.OnHelpGui)

 
        self.SetMenuBar(menubar)
        return 
    
 
    def CreateMenuItem(self, menu, label, func, icon=None, id=None):
        if id:
            item = wx.MenuItem(menu, id, label)
        else:
            item = wx.MenuItem(menu, -1, label)

        if icon:
            item.SetBitmap(wx.Bitmap(icon))

        if id:
            self.Bind(wx.EVT_MENU, func, id=id)
        else:
            self.Bind(wx.EVT_MENU, func, id=item.GetId())

        menu.Append(item)
        return item 
 
 
 
 
 
    
    def OnExit(self,event):
        print("Program is terminating")
        self.Close(True)
        return 1 # needed
 
    def OnOpenCSVFile(self,event):  
        """this will ask for the file to open"""
        
        with wx.FileDialog(self, "Open CSV file", wildcard="csv file (*.csv)|*.csv",
                       style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed their mind

        # Proceed loading the file chosen by the user
            self.csvfile = fileDialog.GetPath()
            
        
        #instantiate the ReadTree system
        
        self.PRI.ReadFile(self.csvfile)
        
        #self.OnSetOutputFile(event)

          
    def OnReduceTable(self,event):
        
        
         

        self.ReduceFile = self.outputdir+self.outputfile
        self.PRI.ReduceTable(ReduceList = self.ReduceList , ReduceFile = self.ReduceFile)

        return

        # Now read the tree from the file
        
    def OnLoopDevices(self,event):
        
        
        
        self.Plot=False
        self.Screen = False
        frame = wx.Frame(parent = None,title ='Loop Plot Control',size = (400,140),pos =(100,100))
        panel = wx.Panel(frame,-1) 
        frame.Show(show=True)

        self.cb1=wx.CheckBox(panel,-1,'Plot?',(10,40),(350,20))
        self.cb2=wx.CheckBox(panel,-1,'Screen?',(10,60),(350,20))
        self.button = wx.Button(panel,-1,"Close",pos = (10,80),size=(40,40))
        self.cb1.Bind(wx.EVT_CHECKBOX,self.OnLoopChecked) 
        self.cb2.Bind(wx.EVT_CHECKBOX,self.OnLoopChecked) 
        self.Centre() 
        self.Show(True) 
        self.button.Bind(wx.EVT_BUTTON, self.OnClose)
        print(self.Plot)


    # hide ourself on close, don't destroy
    def OnClose(self, event):
        print("in close")
        self.PRI.LoopDevices(looplist = self.looplist,Plot=self.Plot,plotdir=self.outputdir,plotting = self.Screen)
        
        self.Destroy()

         
    def OnLoopChecked(self,event):
        """ controls what has been checked in the loodevice"""
        cb = event.GetEventObject() 
        print(cb.GetLabel(),' is clicked',cb.GetValue())
        if(cb.GetLabel() == 'Plot?'):
            self.Plot=cb.GetValue()
        if(cb.GetLabel() == 'Screen?'):
            self.Screen=cb.GetValue()
        print(self.Plot,' ' ,self.Screen)
   
      
    def onChecked(self, event): 
        cb = event.GetEventObject() 
        print(cb.GetLabel(),' is clicked',cb.GetValue())

         
  
         
        
         
    def OnGetLoopList(self,event):    
        """ create the list to loop over"""
        print('not implemented yet')
 
    def OnGetSpeedBoxFile(self,event):
        """ reads the filename and file for the speedbox comparison"""
        
        with wx.FileDialog(self, "Open speedboxfile file", wildcard="csv file (*.csv)|*.csv",
                       style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed their mind

        # Proceed loading the file chosen by the user
            self.speedboxfile = fileDialog.GetPath()
            
        self.MyT.GetSpeedBoxFile(self.speedboxfile)
 
        
    def OnGetVariables(self,event):
        """ provides a list of variables to choose from"""
        
         
        frame = wx.Frame(parent = None,title ='variable list',size = (400,800),pos =(100,100))
        panel = wx.Panel(frame,-1) 
        self.FrameListPanel = frame  # so tha we can close this from a different function
        frame.Show(show=True)

        # first add a cancel and save button
        
        saveBtn =  wx.Button(panel,-1,"Save")
        cancelBtn =  wx.Button(panel,-1,"Cancel")
        
        topLbl = wx.StaticText(panel,-1,"Available branches")
        topLbl.SetFont(wx.Font(18,wx.SWISS,wx.NORMAL,wx.BOLD))
            
        myclb = wx.CheckListBox(panel,-1,(20,100),(300,600),self.PRI.GetVariableList(),wx.LB_MULTIPLE)
        # set the variables from reducelist to checked, since those will be mostly used
        myclb.SetCheckedStrings(self.ReduceList)
        
        
        panel.Bind(wx.EVT_LISTBOX, self.EvtListBox, myclb)
        panel.Bind(wx.EVT_CHECKLISTBOX, self.EvtCheckListBox, myclb)
        myclb.SetSelection(0)
        self.myclb = myclb
        
        
        # Now we need to bind te two buttons:
        
        panel.Bind(wx.EVT_BUTTON,self.OnSaveList, saveBtn)
        panel.Bind(wx.EVT_BUTTON,self.OnCancelList, cancelBtn)
        
        
        # now do the sizer
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(topLbl,0,wx.ALL,15)
        
        branchSizer = wx.BoxSizer(wx.VERTICAL)
        branchSizer.Add(myclb,0,wx.EXPAND)
        
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer.Add((20,20),1)
        btnSizer.Add(saveBtn)
        btnSizer.Add((20,20),1)
        btnSizer.Add(cancelBtn)
        btnSizer.Add((20,20),1)
        
        mainSizer.Add(branchSizer,0,wx.EXPAND,30)
        mainSizer.Add(btnSizer,0,wx.EXPAND|wx.BOTTOM,30)
        
        panel.SetSizer(mainSizer)
        myclb.Show(show=True)
        
        var_list = list(myclb.GetCheckedStrings())
        #print('list',var_list)
        
        # new reduce list
        self.ReduceList=var_list
            
    def OnGetLogWarnings(self,event):
        
        
        #first get tag for logging
        TA=TagBox()
        TA.SetCode('Warning')

        TA.Show()
         
        
    def OnGetLogErrors(self,event): 

        #first get tag for logging

        TA=TagBox()
        TA.SetCode('Error')
        TA.Show()

    
    def OnSetDevice(self,event):
        """here we choose the device"""
        self.devicename = ''
        dialog = wx.TextEntryDialog(None," Give name of the device",value="madre-de-dios",style=wx.OK | wx.CANCEL,pos=(800,500))
        if dialog.ShowModal() == wx.ID_OK:
            self.devicename = dialog.GetValue()
        dialog.Destroy()

    def OnSetTest(self,Event):
        """ creates the test for reading the database"""
        # create the panel
        frame = wx.Frame(parent = None,title ='Setting up the test',size = (400,140),pos =(100,100))
        panel = wx.Panel(frame,-1) 
        frame.Show(show=True)
        multitext = wx.TextCtrl(panel,-1,"    \n\n\n",size=(390,120),style=wx.TE_MULTILINE)
        multitext.SetInsertionPoint(0)
    
        
       
    def OnSetOutputFile(self,event):   
        """
        When called all output from UNMS will go to this outputfile
        """
        OF=OutputFileDialog(default_dir = '/LCWA/data/new/',default_file='reduce_devicedetail.csv')
        OF.Show()
        
        
        
    def GetAllDevices(self):
        """gets called at initialization, determines all the available devices"""
        
        self.device_list = self.MyT.GetDeviceList()    
        
    ############Help system
    
    def OnHelpGeneral(self,event): 
        """
        provides an overview
        """
        frame = wx.Frame(parent = None,title ='Help System',size = (400,300))
        panel = wx.Panel(frame,-1) 
        
        
        text = " This is an overview of the UNMS_GUI \n and how to use it. First you need to make sure that you are connecetd to the VPN "
        
        help = wx.StaticText(panel,-1,text)
        help.Wrap(400)
        frame.Show(show=True)
        
    def OnHelpGui(self,event):
        """ give help on how to use the Control"""
        #open a panel
        print ("help gui")
        MyGH = HelpGUI.MyGuiApp(redirect = False) 
        MyGH.MainLoop()       
    
        
           
    
    
    def OnSaveList(self,event):
        """ this routine gets called from OnGetVariables, when you press save"""
        print("saving")
        self.blist = self.myclb.GetCheckedStrings()
        print(self.blist)
        self.FrameListPanel.Destroy() 
   

    def OnCancelList(self,event):
        """ this routine gets called from OnGetVariables, when you press save"""
        print("cancelling")
        self.FrameListPanel.Destroy()    



    def my_listener(self, message, arg2=None):
        """
        Listener function; each message starts with the identifier
        ;"login" : this comes from the login panel and includes IP,username and password
        """
        if (message[0] == "Login"):
            self.UNMS.host = self.ip_adress = message[1]
            self.UNMS.user = self.user_name = message[2]
            self.UNMS.password = self.password = message[3]
            self.UNMS.Initialize(self.UNMS.host)
            self.UNMS.Login()
            
            # here we get the token back
            self.auth_token = self.UNMS.auth_token
        elif (message[0]=='Tag' and message[1]=='Warning' ):
            self.UNMS.logtag = message[2]
            self.UNMS.GetLogWarnings()
        elif (message[0]=='Tag' and message[1]=='Error' ):
            self.UNMS.logtag = message[2]
            self.UNMS.GetLogErrors()
 
        elif (message[0] == "OutFile"):
            self.outputdir = message[1]
            self.outputfile = message[2]
        elif (message[0] == "AircubeControl"):
            self.UNMS.SetAirCubeNetwork(message[1])
        
        #print(f"Received the following message: {message}")
        if arg2:
            print("Received another arguments: {arg2}")

    



    def EvtListBox(self, event):
        print('EvtListBox: %s\n' % event.GetString())

    def EvtCheckListBox(self, event):
        index = event.GetSelection()
        label = self.myclb.GetString(index)
        status = 'un'
        if self.myclb.IsChecked(index):
            status = ''
        print('Box %s is %schecked \n' % (label, status))
        self.myclb.SetSelection(index)    # so that (un)checking also selects (moves the highlight)
        
    def OnDrawVariable(self,event):
        """ Draws variables according to selected list
        If variables have been selected previously they are listed here 
        and can be reduced
         """
         
         # determine if there are already selected variables
        if self.devicename == None:
            self.OnSetDevice(event)
        # check that devicename has been selected:
        
        try:    
            print(self.startline, ' selected variables ',self.blist)
        except:
            self.OnGetVariables(event)
            
        if(len(self.blist)> 1):
            print(self.startline,' multi var drawings not possible')
            print(self.startline,' Pick one variable')
            self.OnGetVariables()
        
        
        self.MyT.DrawVariable(self.blist[0],devicename=self.devicename)
            
 

class Panda_GUI(wx.App):

    def __init__(self,redirect = True,filename=None):
        wx.App.__init__(self,redirect,filename)

    def OnInit(self):
        """
        Needs to be called to initailize the wx App
        """
        self.version = "1.0.0"
        self.author = "Andi Klein"
        
        print ("oninit")
        self.UF = MyFrame(parent = None , id = -1, title ='LCWA display')
        self.UF.Show()

        self.SetTopWindow(self.UF)

        self.UF.SetSize((600,300))
        #self.UF.Centre()
        self.UF.SetPosition((90,900))
        
        
        
       

        
        
        
        

        
        return True
    
    
        
 
        

  





if __name__ == '__main__':
    
    MA = Panda_GUI(redirect=False)
    MA.MainLoop()



        