'''
Created on Sep 2, 2016

@author: klein
'''
import wx
#import wx.html2 as html2
import webbrowser
import os
 



class MyGuiApp(wx.App):
    """ master subclass"""
 
    def OnInit(self):
        """ initializes the application"""
                # instantitae ANA
        
        self.MyHG = MyHelpGUI(None,"helper window")
        self.MyHG.Show()
        
        return True




class MyHelpGUI(wx.Frame):
    '''
    classdocs
    '''
    def __init__ (self,parent,title="Help on GUI"):
        """ creates the parent frame"""

        super(MyHelpGUI,self).__init__(parent,title=title,style=wx.MINIMIZE_BOX | wx.RESIZE_BORDER | wx.CLOSE_BOX)
        
        
        
        self.panel = MyPanel(self)
        self.panel.SetBackgroundColour('Grey')
        
        
        
class MyPanel(wx.Panel):
    def __init__ (self,parent):
        super(MyPanel,self).__init__(parent)
        
        
        self.button = wx.Button(self,label="press me")
        #find location of the files:
        filename = 'PandaControl.html'
        
        self.help_file = os.getcwd()+'/help_files/'+filename
        if(os.path.isfile(self.help_file)):
            self.help_file ='file://'+self.help_file

            webbrowser.open(self.help_file)
        else:
            home = os.path.expanduser("~")
            for root, dirs, files in os.walk(home):
                for name in files:
                    if name == filename:
                        self.help_file = os.path.abspath(os.path.join(root, name))
            self.help_file ='file://'+self.help_file
            webbrowser.open(self.help_file)
            
        
 



if __name__ == '__main__':
    MyGH = MyGuiApp(redirect = False) 
    MyGH.MainLoop()       