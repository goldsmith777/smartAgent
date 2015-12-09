# -*- coding: UTF-8 -*-  
#########################################  
# wifi_dbscan_oneDay： 
# 用法说明：输入：读取mongodb中locations的数据
#         功能：对经纬度利用dbscan方法聚类（1天）
#         输出： 上传数据userprofiles_copy \
#         （urseid，家的wii，公司的wifi，家的经纬度，\
#         离家5/10分钟的点（经纬度，wifi环境，id），\
#         所有链接过的wifi（位置，时长））
#########################################  
from dateutil.parser import parse
import dateutil
from pymongo import MongoClient
from collections import defaultdict  
import random
from math import *
import numpy as np
import numpy 
from dateutil.parser import parse
import datetime
import time
import json
from bson import json_util
from datetime import timedelta, date
import copy

class log_item:
    timestamp = ""
    userid = 0
    lat = 0.0
    lon = 0.0
    conwifi = {}
    conssid = ""
    conbssid = ""
    activity = ""
    wifienv =[]
    def __init__(self,line_str):
        self.line_str = line_str
        j = line_str
        if j.get("userid") :
            self.userid = j["userid"]
        if j.get("timestamp") :
            self.timestamp = j[u"timestamp"]
        if j.get("latitude") :
            self.lat = j[u"latitude"]
        if j.get("longitude") :
            self.lon = j[u"longitude"] 
        if j.get("connectedwifi") :
            self.conwifi = j["connectedwifi"]
            self.conssid = j["connectedwifi"]["ssid"]
            self.conbssid = j["connectedwifi"]["bssid"]
        if j.get("wifienv") :
            self.wifienv = j["wifienv"]
        if j.get("activity") :
            self.activity = j["activity"]


def time_max(d):
    #输入：字典：d ={key:[time,lon,lat],...}
    #功能：time最大的key
    #输出：(ssid,bssid)
    max_value = 0
    key = ""
    for i in d:
        if d[i][0] > max_value:
            max_value = d[i][0]
            key = i
    return key


def time_merge(a,b,c):
    #输入：字典：a ={key:[time,[lon1,],[lat1,]],...},b ={key:[time,[lon1,],[lat1,]],...},\
    #       c = {key:[time,[lon1,],[lat1,]],...}
    #功能：合并a,b,c
    #输出：c ={key:[time,lon,lat],...}
    for i in a:
        if i in c:
            c[i][0] = c[i][0]+ a[i][0]
        else:
            c.setdefault(i,a[i])
    for i in b:
        if i in c:
            c[i][0] = c[i][0]+ b[i][0]
        else:
            c.setdefault(i,b[i])
    for i in c:
        if c[i][1]:
            c[i][1] = sum(c[i][1])/len(c[i][1])
            c[i][2] = sum(c[i][2])/len(c[i][2])
    return c

def dictsetdefault(d,wifi,time,lon,lat):
    d.setdefault(wifi,[0,[],[]])
    d[wifi][0] += time
    if len(d[wifi][1]) < 10 and lon != 0:
        d[wifi][1].append(lon)
        d[wifi][2].append(lat)
    return d

def home_companywifi(userid,lines,l,collection):
    #输入userid，及datas
    #输出家的wifi[ssid,bssid]
    wifidaytime = {}
    wifinighttime = {}
    wifiothertime = {}
    lat_list = []
    lon_list = []
    lon = 0
    lat = 0
    for i in range(1,l):
        m = log_item(lines[i-1])
        n = log_item(lines[i])
        if m.timestamp.isoweekday() != 6 and m.timestamp.isoweekday() != 7:
            if m.conbssid and  n.conbssid and m.conbssid == n.conbssid:
                wifi = (n.conssid,n.conbssid)
                time_hour = m.timestamp.hour
                time = (n.timestamp- m.timestamp).seconds
                if time_hour > 21 or time_hour < 6:
                    dictsetdefault(wifinighttime,wifi,time,m.lon,m.lat)
                elif time_hour > 10 and time_hour < 17:
                    dictsetdefault(wifidaytime,wifi,time,m.lon,m.lat)  
                else:
                    dictsetdefault(wifiothertime,wifi,time,m.lon,m.lat)
        del m
        del n                    
    allconwifitime = time_merge(wifinighttime,wifidaytime,wifiothertime)
    homewifi = time_max(wifinighttime)
    companywifi = time_max(wifidaytime)
    if homewifi:
        lon = allconwifitime[homewifi][1]
        lat = allconwifitime[homewifi][2]
        db.userprofiles_copy.update(userid,{"$set":{"timestamp":datetime.datetime.now(), "homewifi":{"ssid":homewifi[0],"bssid":homewifi[1]},"longitude":lon,"latitude":lat}})
    if companywifi:
        db.userprofiles_copy.update(userid,{"$set":{"timestamp":datetime.datetime.now(),\
                                           "companywifi":{"ssid":companywifi[0],"bssid":companywifi[1]}}})        
    allconwifi_list = []
    for i in allconwifitime:
        allconwifi_list.append({"ssid":i[0],"bssid":i[1],"timelong":allconwifitime[i][0],"longitude":allconwifitime[i][1],"latitude":allconwifitime[i][2]})
    db.userprofiles_copy.update(userid,{"$set":{"timestamp":datetime.datetime.now(),\
                                           "allconwifitime" :allconwifi_list}})
    return homewifi

def dist(p1, p2):
    a = cos(p1[0])*cos(p2[0])
    b = sin(p1[0])*sin(p2[0])*cos(p2[1]-p1[1])
    if a+b >=1:
        return 0
    return acos(float(a+b))*6371*pi/180

def find_core(all_points,E,minPts):
    # 查找核心点
    other_points =[]  
    core_points=[]  
    plotted_points=[]
    for point in all_points:
        point.append(0)
        total = 0
        for otherPoint in all_points:
            distance = dist(otherPoint,point)
            if distance <= E:
               total += 1
        if total > minPts:
            core_points.append(point)
            plotted_points.append(point)
        else:
            other_points.append(point)
    return core_points,plotted_points,other_points

def find_border(core_points,plotted_points,other_points,E):
    # 查找边界点
    border_points=[]
    for core in core_points:
        for other in other_points:
            if dist(core,other) <= E:
                border_points.append(other)
                plotted_points.append(other)
    return border_points,plotted_points


def algorithm(all_points,core_points,border_points,plotted_points,E):
    # 返回簇，噪声点  
    cluster_label = 0
    for point in core_points:
        if point[-1] == 0:
            cluster_label += 1
            point[-1] = cluster_label
        for point2 in plotted_points:
            distance = dist(point2,point)
            if point2[-1] ==0 and distance <= E:
                point2[-1] =point[-1]
            
    cluster_dict = {}
    for point in plotted_points:
        if cluster_dict.get(point[-1]) is None:
            cluster_dict[point[-1]] = [point[0:-1]]
        else:
            cluster_dict[point[-1]].append(point[0:-1])
        
    noise_points=[]
    for point in all_points:
        if  point not in core_points and  point not in border_points:
            noise_points.append(point[0:-1])
    return cluster_dict,noise_points

def max_value(d):
    # 输入：字典
    # 功能：求出字典key-value中value最大的key
    # 输出：字典的键
    maxvalue = 0
    key = -1
    for i in d:
        if d[i] > maxvalue:
            maxvalue = d[i]
            key = i
    return key

def home_border(cluster_dict,noise_points,homewifi):
    # 输入：簇，噪声点，homwfi
    # 功能：根据wifi环境确定家的边界和重新更新噪声点
    # 输出：噪声点
    home_lable = {}
    for lable in cluster_dict:
        home_lable.setdefault(lable,0)
        for eachpoint in cluster_dict[lable]:
            if eachpoint[3] and eachpoint[3]["bssid"] == homewifi:
                home_lable[lable] += 1
    key = max_value(home_lable)
    if key != -1:
        homeborder = cluster_dict[key]
        for eachpoint in homeborder:
            if  not eachpoint[2] :
                break
            else:
                flag = 0
                for i in eachpoint[2]: 
                    if i["bssid"] == homewifi:
                        flag = 1
                if flag == 0:
                    noise_points.append(eachpoint)
                else:
                    break
    return noise_points
                
def durtime(noise_points,difftime):
    # 输入：噪声点，时间间隔
    # 功能：分成不同的路径
    # 输出：路径点[[],[]]
    no =  np.array(noise_points)
    no_sort = no[no[:,-1].argsort()]
    l = len(no_sort)
    k = [0]
    for i in range(l-1):
        diff_time = (no_sort[i+1][-1] - no_sort[i][-1]).seconds
        if diff_time > difftime:
            k.append(i+1)
    k.append(l)
    no_split = []
    for i in range(len(k)-1):
        no_split.append(no_sort[k[i]:k[i+1]])
    return no_split

def settime_point(timepoint300,num,settime1,eachpath):
    global timepoint_id
    for i in range(num-1,-1,-1):
        time =(eachpath[-1][-1] - eachpath[i][-1]).seconds
        if time < settime1 + 60 and time > settime1 - 60:
            print eachpath[i][-1],eachpath[-1][-1]
            timepoint_id += 1
            timepoint300.append( {"longitude":float(list(eachpath[i])[0]),"latitude":float(list(eachpath[i])[1]),"wifienv":eachpath[i][2],"remindnums":0,"id":time.time()})
            break
        if time > settime1 + 60:
            break    

def home_path(no_split,placehome,settime1,settime2):
    # 输入:噪声点，家的位置，时间1，时间2
    # 功能：1，确定是回家的路径；2，回家路径往前推时间1，时间2的点
    # 返回：回家settime1,settime2的{"longitude"：lon,"latitude":lat,"wifienv":[],"remindnums":0}
    timepoint300 = []
    timepoint600 = []
    for eachpath in no_split:
        if dist(list(placehome), list(np.array(eachpath[-1][:2],dtype = float))) < 0.5:
            print "dist",dist(list(placehome), list(np.array(eachpath[-1][:2],dtype = float)))
            num = len(eachpath)
            settime_point(timepoint300,num,settime1,eachpath)
            settime_point(timepoint600,num,settime2,eachpath)
    return timepoint300,timepoint600


def datas_day(lines,l):
    # 输入：userid，l
    # 功能：数据按天划分
    # 输出：按天划分的数据[[day1],[day2],……]
    dataday = []
    datasday = []
    for i in range(1,l):
        m = log_item(lines[i-1])
        n = log_item(lines[i])
        if  m.timestamp.isoweekday() != 6 and m.timestamp.isoweekday() != 7:
            if  m.timestamp.day == n.timestamp.day:
                if n.lat != 0 :
                    dataday.append([n.lon,n.lat,n.wifienv,n.conwifi,n.timestamp])
            else:
                if len(dataday) > 10:
                    datasday.append(dataday)
                dataday = []
            if i == l-1:
                datasday.append(dataday)
    return datasday


def dbscan(all_points,settime1,settime2,userid,collection,homewifi,placehome):
    # 功能：dbscan算法
    E,minPts = 0.1,10
    core_points,plotted_points,other_points = find_core(all_points,E,minPts)
    border_points,plotted_points =  find_border(core_points,plotted_points,other_points,E)
    cluster_dict,noise_points = algorithm(all_points,border_points,core_points,plotted_points,E)
    noise_points = home_border(cluster_dict,noise_points,homewifi)
    difftime = 3600
    if noise_points and cluster_dict:
        no_split = durtime(noise_points,difftime)
        return home_path(no_split,placehome,settime1,settime2)
    else:
        return [],[]
    
def all_user(lines_userid):
    # 功能：查找所有的userid
    alluser = []
    for line in lines_userid:
        if  line["userid"] not in alluser:
            alluser.append(line["userid"])
    return alluser    


    
if __name__ == '__main__':
    A = datetime.datetime.now()
    client = MongoClient('10.120.22.209',27017)
    db = client['smartHome']
    collection = db.userprofiles_copy
    lines_userid = db.locations.find({}, {"userid" : 1,"_id":0})
    alluser =  all_user(lines_userid)
    t0 = date.today()-timedelta(days = 1)
    d = datetime.datetime(t0.year, t0.month, t0.day,0,0,0)
    for each in alluser:
        userid = {"userid": each}
        print userid
        lines = db.locations.find( { "$and": [ userid,{ "timestamp": { "$gt": d }}]}).sort("timestamp",1)
        l = lines.count()
        homewifi  =  home_companywifi(userid,lines,l,collection)
        userline = db.userprofiles_copy.find_one(userid) 
        if  userline and homewifi and userline.get("homewifi") and userline.get( "longitude") :
            datasday = datas_day(lines,l)
            #print homewifi
            homewifi = homewifi[1]
            placehome = [userline["longitude"],userline["latitude"]]
            timepoint_id = 0
            timepoints300 = []
            timepoints600 = []
            for i in range(len(datasday)):
                all_points =copy.deepcopy( datasday[i])
                timepoint300,timepoint600  =  dbscan(all_points,300,600,userid,collection,homewifi,placehome)
                timepoints300.extend(timepoint300)
                timepoints600.extend(timepoint600)
            db.userprofiles_copy.update(userid,{"$set":{"timestamp":datetime.datetime.now(),"timepoints(300s)":timepoints300,\
                                               "timepoints(600s)":timepoints600}})
    B = datetime.datetime.now()
    print (A - B).seconds 
                
