#encoding:utf-8
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

def sexPicture(mp):
    sexmp = {}
    sexmp['m'] = u'男性'
    sexmp['f'] = u'女性'
    sexmp['n'] = u'不明'
    plt.figure(1,figsize=(6,6))
    ax = plt.axes([0.1,0.1,0.8,0.8])
	
    labels = []
    fracs = []
    num = 0
    for key,value in mp.items():
	labels.append(sexmp[key])
	fracs.append(value)
	num += value
    for x in fracs:
	x = x/num*1.0

    string = u"统计人数:" + str(num)
    plt.title(string)
    plt.pie(fracs,None,labels,autopct='%1.1f%%',shadow=True)
    plt.show()

def cityPicture(mp):
    citymp = {'34':u'安徽','11':u'北京','50':u'重庆','35':u'福建','62':u'甘肃','44':u'广东 ','45':u'广西','52':u'贵州','46':u'海南','13':u'河北','23':u'黑龙江','41':u'河南','42':u'湖北','43':u'湖南','15':u'内蒙古','32':u'江苏','36':u'江西','22':u'吉林','21':u'辽宁 ','64':u'宁夏','63':u'青海','14':u'山西','37':u'山东','31':u'上海 ','51':u'四川','12':u'天津','54':u'西藏','65':u'新疆 ','53':u'云南','33':u'浙江','61':u'陕西','71':u'台湾 ','81':u'香港','82':u'澳门','400':u'海外','100':u'其他'}

    val = []
    label = []
    num = 0
    for key,value in mp.items():
	#print key
	label.append(citymp[key])
	val.append(value)
	num += value

    pos = np.arange(len(val)) + .5
    plt.figure(1)
    plt.bar(pos,val,color='y',align='center')
    plt.xticks(pos,label,rotation='vertical')
    plt.ylabel(u'人数')
    string = u"统计人数:" + str(num)  
    plt.title(string)
    plt.show()


def tagPicture(mp):

    val = []
    label = []
    lst0 = mp.keys()
    #print lst0
    lst1 = mp.values()
    if len(lst1) > 10:
        num = 10
    else:
	num = len(lst1)
 
    while (num != 0):
        i = lst1.index(max(lst1))
	label.append(lst0[i])
	#print type(lst1[i])
	val.append(int(lst1[i]))
        lst0.pop(i)
        lst1.pop(i)
        num -= 1
		
    #print label
    pos = np.arange(len(val)) +.5
    plt.figure(1)
    plt.bar(pos,val,color='c',align='center')
    plt.xticks(pos,label)
    plt.ylabel(u'人数')
    string = u"热门标签"  
    plt.title(string)
    plt.show()
	
def followsPicture(mp):

    val = []
    label = []
    lst0 = mp.keys()
    #print lst0
    lst1 = mp.values()
    if len(lst1) > 10:
        num = 10
    else:
	num = len(lst1)
    while (num != 0):
        i = lst1.index(max(lst1))
	label.append(lst0[i])
	#print type(lst1[i])
	val.append(int(lst1[i]))
	lst0.pop(i)
        lst1.pop(i)
        num -= 1

    pos = np.arange(10) + .5
    plt.figure(1)
    plt.barh(pos,val,align='center')
    plt.yticks(pos,label)
    plt.xlabel(u'粉丝数目')
    string = u"统计人数:" + str(len(mp.keys()))  
    plt.title(string)
    plt.show()	

def trendPicture(rt,comment):
     
    colorList = ['b','g','r','c','m','y','k']
 
    threadList = []
    for i in range(len(rt)):
	threadList.append(i)
   
    dataList1 = [int(x) for x in rt]
    dataList2 = [int(x) for x in comment]
   
    string = str(len(dataList1)) + u'条微博趋势图'
    plt.title(string)

    
    lines = []

    titles = []

   
    line1 = plt.plot(threadList, dataList1)
    plt.setp(line1, color=colorList[0], linewidth=2.0)
    titles.append(u'转发')
    lines.append(line1)

   
    line2 = plt.plot(threadList, dataList2)
    plt.setp(line2, color=colorList[1], linewidth=2.0)
    titles.append(u'评论')
    lines.append(line2)

    plt.legend(lines, titles)
    plt.show()
    

