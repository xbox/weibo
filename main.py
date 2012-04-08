#encoding:utf-8
import wx
import cStringIO
import urllib2
import search
from data import getData
from photo import *
import topic

class My_Frame1(wx.Frame):
    def __init__(self,data,flaglt):
	wx.Frame.__init__(self,None,-1,"Analysis",size=(200,200))
	self.data = data
	self.client = getData(flaglt)
	
	#print data	
	menubar = wx.MenuBar()
	
	followMenu = wx.Menu()
	sexitem0 = followMenu.Append(-1,u'性别图','about the sex')
	localitem0 = followMenu.Append(-1,u'区域图','about the city')
	tagitem0 = followMenu.Append(-1,u'标签图','abouth the tag')
	topitem0 = followMenu.Append(-1,u'Top10','top10 follows')
	menubar.Append(followMenu,u'&粉丝')

	friendMenu = wx.Menu()	
	sexitem1 = friendMenu.Append(-1,u'性别图','about the sex')
	localitem1 = friendMenu.Append(-1,u'区域图','about the city')
	tagitem1 = friendMenu.Append(-1,u'标签图','abouth the tag')
	topitem1 = friendMenu.Append(-1,u'Top10','top10 follows')
	menubar.Append(friendMenu,u'&关注')

	weiboMenu = wx.Menu()
	statusitem = weiboMenu.Append(-1,u'影响力','about his weibo')
	topicitem = weiboMenu.Append(-1,u'关注面','what he cares')
	menubar.Append(weiboMenu,u'微博')
	
	backMenu = wx.Menu()
	menubar.Append(backMenu,u'返回')
	exititem = backMenu.Append(-1,u'返回搜索','back to search')
	self.SetMenuBar(menubar)

	self.Bind(wx.EVT_MENU,self.Sex0,sexitem0)
	self.Bind(wx.EVT_MENU,self.Local0,localitem0)
	self.Bind(wx.EVT_MENU,self.Tag0,tagitem0)
	self.Bind(wx.EVT_MENU,self.Top0,topitem0)

	self.Bind(wx.EVT_MENU,self.Sex1,sexitem1)
	self.Bind(wx.EVT_MENU,self.Local1,localitem1)
	self.Bind(wx.EVT_MENU,self.Tag1,tagitem1)
	self.Bind(wx.EVT_MENU,self.Top1,topitem1)

	self.Bind(wx.EVT_MENU,self.Influence,statusitem)
	self.Bind(wx.EVT_MENU,self.careTopic,topicitem)
	
	self.Bind(wx.EVT_MENU,self.OnBack,exititem)

	mastersizer = wx.BoxSizer(wx.VERTICAL)
	topsizer = wx.BoxSizer(wx.HORIZONTAL)
	middlesizer = wx.BoxSizer(wx.VERTICAL)

 	self.createPhoto(topsizer)
	self.createTitle(topsizer)
	self.createText(middlesizer)

	mastersizer.Add(topsizer)
	mastersizer.Add(middlesizer)
	
	self.SetSizer(mastersizer)

    def createPhoto(self,sizer):
	photourl = self.data[5]
	string = cStringIO.StringIO(urllib2.urlopen(photourl).read())
	bmp = wx.ImageFromStream(string).ConvertToBitmap()
	photobutton = wx.StaticBitmap(self,-1,bmp,size=(72,72),style=wx.NO_BORDER)
	sizer.Add(photobutton,0,flag=wx.LEFT|wx.TOP,border=16)
	
    def createTitle(self,sizer):
	titlename = self.data[0]+ '\n' + self.data[1]
	#titlename = self.data[1]
	font = wx.Font(10,wx.DEFAULT,wx.NORMAL,wx.NORMAL)
	self.title = wx.StaticText(self,-1,titlename,style=wx.ALIGN_LEFT)
	self.title.SetFont(font)
	sizer.Add(self.title,0,flag=wx.ALL,border=16)

    def createText(self,sizer):
	label = (u'粉丝',u'关注',u'微博')
	num = self.data[2:5]
	for index in range(len(label)):
	    string = label[index] + ': ' + str(num[index])
            text = wx.StaticText(self,-1,string)
	    text.SetFont(wx.Font(12,wx.SWISS,wx.NORMAL,wx.NORMAL,False))
	    sizer.Add(text,0,flag=wx.LEFT,border=16)
   
    def Sex0(self,event):
	mp = {}
	self.client.getFollows(self.data[0])
	mp = self.client.getFollowsSexInfo()
	sexPicture(mp)

    def Local0(self,event):
	mp = {}
	self.client.getFollows(self.data[0])
	mp = self.client.getFollowsCityInfo()
	cityPicture(mp)
	
    def Tag0(self,event):
	mp = {}
	self.client.getFollows(self.data[0])
	mp= self.client.getFollowsTagInfo()
	tagPicture(mp)

    def Top0(self,event):
	mp = {}
	self.client.getFollows(self.data[0])
	mp= self.client.getTopFollows()
	#print mp
	followsPicture(mp)

    def Sex1(self,event):
	mp = {}
	self.client.getFriends(self.data[0])
	mp = self.client.getFriendsSexInfo()
	sexPicture(mp)

    def Local1(self,event):
	mp = {}
	self.client.getFriends(self.data[0])
	mp = self.client.getFriendsCityInfo()
	cityPicture(mp)

    def Tag1(self,event):
	mp = {}
	self.client.getFriends(self.data[0])
	mp= self.client.getFriendsTagInfo()
	tagPicture(mp)

    def Top1(self,event):
	mp = {}
	self.client.getFriends(self.data[0])
	mp= self.client.getTopFriends()
	#print mp
	followsPicture(mp)


    def Influence(self,event):
	self.client.getWeibo(self.data[0])
	rt,comment = self.client.getTrend()
	trendPicture(rt,comment)
	
    def careTopic(self,event):
		
	mp = {}
	self.client.getWeibo(self.data[0])
	mp = self.client.getTopic()
	#print mp
	flaglt = self.client.getFlagStatus()
	data = self.data
	frame2 = topic.My_Frame2(data,flaglt,mp)
	frame2.Show()
	frame2.Center()
	self.Destroy()
	
    def OnBack(self,event):
	self.client.deleteFollowsData()
	self.client.deleteFriendsData()
	self.client.deleteWeiboData()
	frame0 = search.My_Frame0()
	frame0.Show()
	frame0.Center()
	self.Destroy()

	
