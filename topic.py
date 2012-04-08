import wx
import main

class My_Frame2(wx.Frame):
    def __init__(self,data,flaglt,mp):
	
	wx.Frame.__init__(self,None,-1,"Top5",size=(1000,635))

	self.data = data
	self.flaglt = flaglt
	self.mp = mp

	mastersizer = wx.BoxSizer(wx.VERTICAL)
	self.putText(mastersizer,self.mp)
	self.SetSizer(mastersizer)
	
	bmp = wx.Bitmap('./close.png')
	button = wx.BitmapButton(self,-1,bmp,size=(bmp.GetWidth()+8,bmp.GetHeight()+8),style=wx.NO_BORDER)
	mastersizer.Add(button,0,wx.LEFT,border=490)
	self.Bind(wx.EVT_BUTTON,self.OnClose,button)

    def OnClose(self,event):
	frame1 = main.My_Frame1(self.data,self.flaglt)
	frame1.Show()
	frame1.Center()
	self.Destroy()
    
    def putText(self,sizer,mp):
        val = []
        label = []
        lst0 = mp.keys()
        lst1 = mp.values()
        if len(lst1) > 5:
           num = 5
        else:
	   num = len(lst1)
        while (num != 0):
            i = lst1.index(max(lst1))
	    label.append(lst0[i])
	    val.append(int(lst1[i]))
            lst0.pop(i)
            lst1.pop(i)
            num -= 1	

	for string in label:
	    text = wx.TextCtrl(self,-1,string,size=(1000,115),style=wx.TE_MULTILINE)
	    text.SetFont(wx.Font(12,wx.SWISS,wx.NORMAL,wx.NORMAL,False))
	    sizer.Add(text,0,flag=wx.DOWN,border=5)
