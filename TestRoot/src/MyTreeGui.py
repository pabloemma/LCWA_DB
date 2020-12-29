'''
Created on Dec 19, 2020

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

sys.path.insert(2,'/Users/klein/git/LCWA/src')
sys.path.insert(3,'/Users/klein/git/LCWA_UNMS/RRD_SNMP/src')

from ReadTree import MyReadTree
from MyError import MyError 


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
 
        
        self.version = 'MyTree GUI Control for LCWA'
        self.author = 'Andi Klein'
        self.date = 'Winter 2020 '
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
   


        
        self.CreateStatusBar()
        self.CreateToolBar()

        self.CreateMenu()
        pub.subscribe(self.my_listener, "panel_listener") #for passing event handler back and forth

        self.ME=MyError()
        
        
        self.program_name = os.path.basename(__file__)
        
        
 
        #log into the system
        #self.OnLogin(0)
 
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
        self.CreateMenuItem(file_menu, "InputFile",self.OnOpenTreeFile)
        self.CreateMenuItem(file_menu, "Output file",self.OnSetOutputFile)

        #section for action
        action_menu = wx.Menu()
        menubar.Append(action_menu,"&Action \tCTRL+A")

        self.CreateMenuItem(action_menu, "Login",self.OnLogin)
        self.CreateMenuItem(action_menu, "Logout",self.OnLogout)
        
        
        self.CreateMenuItem(action_menu, "Debug Level",self.OnDebugLevel)
        
        action_menu.InsertSeparator(2)
        
        #section for services
        service_menu = wx.Menu()
        menubar.Append(service_menu,"Services")

        self.CreateMenuItem(service_menu, "Get Branch List",self.OnGetBranchList)
        self.CreateMenuItem(service_menu, "Get Device List",self.OnGetDeviceList)
        self.CreateMenuItem(service_menu, "Get SpeedBoxFile",self.OnGetSpeedBoxFile)
        self.CreateMenuItem(service_menu, "Get Variables",self.OnGetVariables)




 
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
 
    def OnOpenTreeFile(self,event):  
        """this will ask for the file to open"""
        
        with wx.FileDialog(self, "Open root file", wildcard="root file (*.root)|*.root",
                       style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed their mind

        # Proceed loading the file chosen by the user
            self.rootfile = fileDialog.GetPath()
        
        #instantiate the ReadTree system
        
        self.MyT = MyReadTree(self.rootfile)
        
        # Now read the tree from the file
        self.MyT.ReadTree()
        
         
    def OnLogin(self,event):
        """
        Asks for IP,username and password
        """
        print("OnLogin")
        TF=LoginFrame()


        TF.Show()
        return 
    
    def OnLogout(self,event):
        print("Logging out of UNMS server")
        self.UNMS.Logout()
        
    def OnGetUser(self,event):
        """
        Print out username and email of device
        """
        self.user = self.UNMS.GetUser()
        
    def OnGetBranchList(self,event):
        """ Gives a list of the branches in the ROOT tree"""
        self.MyT.GetBranchList()
        
    def OnGetDeviceList(self,event):
        """ print all the available devices"""
        
        print(self.startline,"Getting list of devices")
        self.MyT.GetDeviceList()
        
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
        """ provides alits of variables to choose from"""
        
        # Chek if Branchlists has already been filled
        
        if not(hasattr(self.MyT, 'Blist')):
            print(self.startline ,'no branchlist, will call GetBranchList')
            self.MyT.GetBranchList()

        frame = wx.Frame(parent = None,title ='variable list',size = (400,800),pos =(100,100))
        panel = wx.Panel(frame,-1) 
        self.FrameListPanel = frame  # so tha we can close this from a different function
        frame.Show(show=True)

        # first add a cancel and save button
        
        saveBtn =  wx.Button(panel,-1,"Save")
        cancelBtn =  wx.Button(panel,-1,"Cancel")
        
        topLbl = wx.StaticText(panel,-1,"Available branches")
        topLbl.SetFont(wx.Font(18,wx.SWISS,wx.NORMAL,wx.BOLD))
            
        myclb = wx.CheckListBox(panel,-1,(60,60),(300,600),self.MyT.Blist,wx.LB_MULTIPLE)
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
        
        mainSizer.Add(branchSizer,0,wx.EXPAND|wx.ALL,30)
        mainSizer.Add(btnSizer,0,wx.EXPAND|wx.BOTTOM,10)
        
        panel.SetSizer(mainSizer)
        myclb.Show(show=True)
        
        var_list = myclb.GetCheckedItems()
        print('list',var_list)
            
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

        
       
    def OnSetOutputFile(self,event):   
        """
        When called all output from UNMS will go to this outputfile
        """
        OF=OutputFileDialog()
        OF.Show()
        
    def OnSetAirCubeNetwork(self,event):
      
      
        self.aircube_system = self.UNMS.GetAircubeSystem()
        MIL=MyInputList('this is the UNMS gui')
        MIL.ReadData(self.aircube_system)
        MIL.CreateLayout()
        MIL.Show()
        

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
    
        
        
    
    def OnDebugLevel(self,event):
        """
        Sets the debug level of UNMSControl
        """
        choices = ["0","1","2"]
        dialog = wx.SingleChoiceDialog(None , "select debug level" ,"Set Debug Level",choices)
        if dialog.ShowModal() == wx.ID_OK:
            debuglevel = int(dialog.GetStringSelection())
            self.UNMS.SetDebugLevel(debuglevel)
        dialog.Destroy()
    
    def OnSaveList(self,event):
        """ this routine gets called from OnGetVariables, when you press save"""
        print("saving")
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
            self.UNMS.SetOutputFile(message[1], message[2])
        elif (message[0] == "AircubeControl"):
            self.UNMS.SetAirCubeNetwork(message[1])
        
        #print(f"Received the following message: {message}")
        if arg2:
            print("Received another arguments: {arg2}")

    

    def PrintDict(self,dict):
        #pprint.pprint(dict, width = 1 ,depth =2,sort_dicts=True)
        
        print('\n ***************w New Block ****************** \n')
            #self.PrintDict(self.allAP[k])
        print( yaml.dump(dict, default_flow_style=False))
        test = yaml.dump(dict, default_flow_style=False)
        try:
            print (dict['name'])
        except:
            pass
        print('\n ************************************************* \n \n \n')
        self.gen_dict_extract('id',dict)



    def gen_dict_extract(self,key, var):
        if hasattr(var,'iteritems'):
            for k, v in var.iteritems():
                if k == key:
                    yield v
                if isinstance(v, dict):
                    for result in self.gen_dict_extract(key, v):
                        yield result
                elif isinstance(v, list):
                    for d in v:
                        for result in self.gen_dict_extract(key, d):
                            yield result

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
        

 

class UNMS_GUI(wx.App):

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
    
    MA = UNMS_GUI(redirect=False)
    MA.MainLoop()



       