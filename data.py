#encoding:utf-8
import pickle
import MySQLdb
from weibopy.auth import OAuthHandler
from weibopy.api import API
from weibopy.error import WeibopError
from weibopy.binder import bind_api
import time

class getData():

    def __init__(self,flaglt):
	APP_KEY = '190802369'
        APP_SECRET = 'fb4ce1e3a4b049abb75f104d7a7439d7'
        BACK_URL = ''
        self.auth = OAuthHandler(APP_KEY,APP_SECRET,BACK_URL)
        with open('entry.pickle','rb') as f:
            entry = pickle.load(f)
        self.key = entry['key']
        self.secret = entry['secret']
	
	self.followflag = flaglt[0]
	self.friendflag = flaglt[1]
	self.weiboflag = flaglt[2]

    def getFlagStatus(self):
	return (self.followflag,self.friendflag,self.weiboflag)
	
    def searchUser(self,name):
        self.auth.setToken(self.key,self.secret)
        api = API(self.auth)
        try :
            user = api.get_user(screen_name=name)
	    #print user.id
            data = (user.screen_name.encode('utf-8'),user.location.encode('utf-8'),user.followers_count,user.friends_count,user.statuses_count,user.profile_image_url)
            return data
        except Exception ,e:
            pass

    def getUser(self,uid):
	self.auth.setToken(self.key,self.secret)
        api = API(self.auth)
        try :
            user = api.get_user(id=uid)
	    string = self.getTag(uid)
	    #print string
	    #print type(string)
	    #print type(user.screen_name)
            data = (user.screen_name.encode('utf-8'),user.id,user.gender,user.province,user.followers_count,string)
	    #print data
            return data
        except Exception ,e:
            pass
	
    def getTag(self,uid):
	self.auth.setToken(self.key,self.secret)
        api = API(self.auth)
	try:
	    tag = api.tags(uid)
    	    #print tag
    	    string = ""
    	    for node in tag:
                for attr,value in node.__dict__.items():
                    if attr != '_api' and attr != 'id':
			#print type(value)
                        string += value.encode('utf-8')+" "
	    return string
	except Exception ,e:
	    pass
       

    def getFollows(self,name):
        self.auth.setToken(self.key,self.secret)
        api = API(self.auth)
        try:
            follows = api.followers_ids(screen_name=name)
        except Exception ,e:
            print e
	mp = {}
        #print len(follows.ids)
	start = time.time()
	if self.followflag == False:
	    if len(follows.ids) > 100:
	        for index in range(0,100):
                    data = self.getUser(follows.ids[index])
                    if data != None:
	                #print data
                        self.updateFollows(data) 
	    else:	
                for index in range(len(follows.ids)):
                    data = self.getUser(follows.ids[index])
                    if data != None:
	                #print data
            		self.updateFollows(data)
	    self.followflag = True
	end = time.time()
	print "time is :", end-start

    def getFriends(self,name):
        self.auth.setToken(self.key,self.secret)
        api = API(self.auth)
        try:
            friends = api.friends_ids(screen_name=name)
        except Exception ,e:
            print e
	mp = {}
        
	start = time.time()
	if self.friendflag == False:
	    if len(friends.ids) > 100:
	        for index in range(0,100):
                    data = self.getUser(friends.ids[index])
                    if data != None:
	                #print data
                        self.updateFriends(data) 
	    else:	
                for index in range(len(friends.ids)):
                    data = self.getUser(friends.ids[index])
                    if data != None:
	                #print data
            		self.updateFriends(data)
	    self.friendflag = True
	end = time.time()
	print "time is :", end-start
	
       
    def updateFollows(self,data):
        try:
            conn = MySQLdb.connect(host='localhost',user='root',passwd='shch89',db='sina')
        except Exception ,e:
            print e

        cursor = conn.cursor()
        sql = "insert into follows values(%s,%s,%s,%s,%s,%s)"
        try :
            cursor.execute(sql,data)
        except Exception ,e:
            print  e
	cursor.close()
        conn.close()

    def updateFriends(self,data):
        try:
            conn = MySQLdb.connect(host='localhost',user='root',passwd='shch89',db='sina')
        except Exception ,e:
            print e

        cursor = conn.cursor()
        sql = "insert into friends values(%s,%s,%s,%s,%s,%s)"
        try :
            cursor.execute(sql,data)
        except Exception ,e:
            print  e
	cursor.close()
        conn.close()

    def deleteFollowsData(self):
	try:
            conn = MySQLdb.connect(host='localhost',user='root',passwd='shch89',db='sina')
        except Exception ,e:
            print e
	mp = {}
        cursor = conn.cursor()
        sql = "truncate table follows"
        try :
            cursor.execute(sql)
        except Exception ,e:
            pass
	cursor.close()
        conn.close()

    def deleteFriendsData(self):
	try:
            conn = MySQLdb.connect(host='localhost',user='root',passwd='shch89',db='sina')
        except Exception ,e:
            print e
	mp = {}
        cursor = conn.cursor()
        sql = "truncate table friends"
        try :
            cursor.execute(sql)
        except Exception ,e:
            pass
	cursor.close()
        conn.close()
	
    def getFollowsSexInfo(self):
	try:
            conn = MySQLdb.connect(host='localhost',user='root',passwd='shch89',db='sina')
        except Exception ,e:
            print e
	mp = {}
        cursor = conn.cursor()
        sql = "select sex from follows"
        try :
            cursor.execute(sql)
	    data = cursor.fetchall()
	    mp = self.sexDict(data)
	    return mp
        except Exception ,e:
            pass
	cursor.close()
        conn.close()

    def getFriendsSexInfo(self):
	try:
            conn = MySQLdb.connect(host='localhost',user='root',passwd='shch89',db='sina')
        except Exception ,e:
            print e
	mp = {}
        cursor = conn.cursor()
        sql = "select sex from friends"
        try :
            cursor.execute(sql)
	    data = cursor.fetchall()
	    mp = self.sexDict(data)
	    return mp
        except Exception ,e:
            pass
	cursor.close()
        conn.close()

    def getFollowsCityInfo(self):
	try:
            conn = MySQLdb.connect(host='localhost',user='root',passwd='shch89',db='sina')
        except Exception ,e:
            print e
	mp = {}
        cursor = conn.cursor()
        sql = "select city from follows"
        try :
            cursor.execute(sql)
	    data = cursor.fetchall()
	    #print data
	    mp = self.cityDict(data)
	    #print mp
	    return mp
        except Exception ,e:
            pass
	cursor.close()
        conn.close()
 
    def getFriendsCityInfo(self):
	try:
            conn = MySQLdb.connect(host='localhost',user='root',passwd='shch89',db='sina')
        except Exception ,e:
            print e
	mp = {}
        cursor = conn.cursor()
        sql = "select city from friends"
        try :
            cursor.execute(sql)
	    data = cursor.fetchall()
	    #print data
	    mp = self.cityDict(data)
	    #print mp
	    return mp
        except Exception ,e:
            pass
	cursor.close()
        conn.close()

    def getFollowsTagInfo(self):
	try:
            conn = MySQLdb.connect(host='localhost',user='root',passwd='shch89',db='sina')
        except Exception ,e:
            print e
	mp = {}
        cursor = conn.cursor()
        sql = "select tag from follows"
        try :
            cursor.execute(sql)
	    data = cursor.fetchall()
	    #print data
	    mp = self.tagDict(data)
	    #print mp
	    return mp
        except Exception ,e:
            pass
	cursor.close()
        conn.close()

    def getFriendsTagInfo(self):
	try:
            conn = MySQLdb.connect(host='localhost',user='root',passwd='shch89',db='sina')
        except Exception ,e:
            print e
	mp = {}
        cursor = conn.cursor()
        sql = "select tag from friends"
        try :
            cursor.execute(sql)
	    data = cursor.fetchall()
	    #print data
	    mp = self.tagDict(data)
	    #print mp
	    return mp
        except Exception ,e:
            pass
	cursor.close()
        conn.close()
	
    def getTopFollows(self):
	try:
            conn = MySQLdb.connect(host='localhost',user='root',passwd='shch89',db='sina')
        except Exception ,e:
            print e
	mp = {}
        cursor = conn.cursor()
        sql = "select name,count from follows"
        try :
            cursor.execute(sql)
	    data = cursor.fetchall()
	    #print data
	    mp = self.topDict(data)
	    #print mp
	    return mp
        except Exception ,e:
            pass
	cursor.close()
        conn.close()

    def getTopFriends(self):
	try:
            conn = MySQLdb.connect(host='localhost',user='root',passwd='shch89',db='sina')
        except Exception ,e:
            print e
	mp = {}
        cursor = conn.cursor()
        sql = "select name,count from friends"
        try :
            cursor.execute(sql)
	    data = cursor.fetchall()
	    #print data
	    mp = self.topDict(data)
	    #print mp
	    return mp
        except Exception ,e:
            pass
	cursor.close()
        conn.close()
    
    def topDict(self,data):
	mp = {}
	for node in data:
	    k = node[0].decode('utf-8')
	    mp[k] = node[1]
	return mp

    def tagDict(self,data):
	mp = {}
	for node in data:
    	    #print node[0]
    	    for x in node[0].split(' ')[:-1]:
	        y = x.decode('utf-8')
		if mp.has_key(y):
	    	    mp[y] += 1
		else:
	    	    mp[y] =1
	return mp


    def sexDict(self,data):
	#print data
	mp = {}
	for node in data:
    	    if str(node)[2:3] == 'f':
		if mp.has_key('f'):
	    	    mp['f'] += 1
	        else :
	            mp['f'] = 1
            elif str(node)[2:3] == 'm':
	        if mp.has_key('m'):
	            mp['m'] += 1
		else :
		    mp['m'] = 1
	return mp

    def cityDict(self,data):
	#print data
	mp = {}
	for node in data:
    	    tmp = str(node)[1:-3]
    	    if mp.has_key(tmp):
 		mp[tmp] += 1
    	    else :
		mp[tmp] =1
        #print mp
	return mp


    def getWeibo(self,name):
        self.auth.setToken(self.key,self.secret)
        api = API(self.auth)
       	start = time.time()
	if self.weiboflag == False:
            try:
                timeline = api.user_timeline(screen_name=name,count=50)
            except Exception ,e:
                print e
   	
            for node in timeline:
	        lst = []
	        lst.append(node.text.encode('utf-8'))
	        tmp = self.getStatus(api,node.id)
	        if tmp == []:
	            lst.extend([0,0])
	        else:
	            lst.extend(tmp)
	
	        refer = getattr(node,'retweeted_status',None)
	        if refer:
	            lst.append(refer.text.encode('utf-8'))
		    #print refer.mid
		    #print refer.id
	            tmp = self.getStatus(api,refer.mid)
		    #print tmp
		    if tmp == []:
		        lst.extend[0,0]
		    else:
	                lst.extend(tmp)    
	        else:
	            lst.extend(['None',0,0])
	        #print (len(lst))
	       
	        self.updateWeibo(lst)
	self.weiboflag = True
	end = time.time()
	print "time is :",end-start
	    

    def getStatus(self,api,uid):
        lst = []
        weibo = api.counts(ids=uid)
        for node in weibo:
	    for attr,value in node.__dict__.items():
 	        if attr == 'rt' or attr == 'comments':
		    lst.append(value)
        return lst

    def updateWeibo(self,data):
	#print data
        try:
            conn = MySQLdb.connect(host='localhost',user='root',passwd='shch89',db='sina')
        except Exception ,e:
            print e
        cursor = conn.cursor()
        sql = "insert into weibo values(%s,%s,%s,%s,%s,%s)"
        try :
            cursor.execute(sql,data)
        except Exception ,e:
            print  e
	cursor.close()
        conn.close()

    def getTrend(self):
	try:
            conn = MySQLdb.connect(host='localhost',user='root',passwd='shch89',db='sina')
        except Exception ,e:
            print e
	mp = {}
        cursor = conn.cursor()
        sql = "select rt,comment from weibo"
        try :
            cursor.execute(sql)
	    data = cursor.fetchall()
	    #print "hello"
	    #print data
	    rt,comment = self.trendList(data)
	    
	    return rt,comment
        except Exception ,e:
            pass
	cursor.close()
        conn.close()

    def trendList(self,data):
	#print "hello"	
	#print data
	rt = []
	comment = []
	for node in data:
	    rt.append(node[0])
	    comment.append(node[1])
	#print rt
	#print comment	
	return rt,comment

    def getTopic(self):
	try:
            conn = MySQLdb.connect(host='localhost',user='root',passwd='shch89',db='sina')
        except Exception ,e:
            print e
	mp = {}
        cursor = conn.cursor()
        sql = "select tweet,retweet,rert,recomment from weibo"
        try :
            cursor.execute(sql)
	    data = cursor.fetchall()
	   
	    mp = self.topList(data)
	    
	    return mp
        except Exception ,e:
            pass
	cursor.close()
        conn.close()

    def topList(self,data):
	mp = {}
	for node in data:
	    string = node[1] + '\n评论:\n' + node[0]
	    #print string
	    mp[string] = int(node[2] + node[3])
	    
	return mp

    def deleteWeiboData(self):
	try:
            conn = MySQLdb.connect(host='localhost',user='root',passwd='shch89',db='sina')
        except Exception ,e:
            print e
	mp = {}
        cursor = conn.cursor()
        sql = "truncate table weibo"
        try :
            cursor.execute(sql)
        except Exception ,e:
            pass
	cursor.close()
        conn.close()

  
	
 		
	
if __name__ == '__main__':
    string = 'shch1289'
    client = getData()
    client.searchUser(string)
   
