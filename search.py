#encoding:utf-8
import wx
import main
from data import getData

class My_App(wx.App):
    def OnInit(self):
	self.frame0 = My_Frame0()
	self.frame0.Show()
	self.frame0.Center()
	self.SetTopWindow(self.frame0)
	self.plt = []
	
	return True

class My_Frame0(wx.Frame):
    def __init__(self):
	wx.Frame.__init__(self,None,-1,"Analysis",size=(280,70))	
	mastersizer = wx.BoxSizer(wx.HORIZONTAL)
	self.basicText = wx.TextCtrl(self,-1,u"用户名",size=(200,-1))
	bmp = wx.Bitmap('./search.png')
	button = wx.BitmapButton(self,-1,bmp,size=(bmp.GetWidth()+8,bmp.GetHeight()+8),style=wx.NO_BORDER)
	mastersizer.Add(self.basicText,0,flag=wx.TOP|wx.LEFT,border=20)
	mastersizer.Add(button,0,flag=wx.TOP,border=20)
	self.Bind(wx.EVT_BUTTON,self.OnSearch,button)
	self.SetSizer(mastersizer)

    def OnSearch(self,event):
	string = self.basicText.GetValue()
	self.basicText.Clear()
	
	flaglt = [False,False,False]
	self.client = getData(flaglt)
	data = self.client.searchUser(string)
	frame1 = main.My_Frame1(data,flaglt)
	frame1.Show()
	frame1.Center()
	self.Destroy()

if __name__ == "__main__":
    app = My_App(False)
    app.MainLoop()
