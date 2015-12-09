#-*- coding: utf-8 -*-

from dateutil.parser import parse
from pymongo import MongoClient
import random
from math import *
import numpy as np
import numpy 
import datetime
import time
import json
from bson import json_util
from datetime import timedelta, date

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
            self.timestamp = j["timestamp"]
        if j.get("latitude") :
            self.lat = j["latitude"]
        if j.get("longitude") :
            self.lon = j["longitude"] 
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
        db.userprofiles.update(userid,{"$set":{"timestamp":datetime.datetime.now(),\
                                           "homewifi":{"ssid":homewifi[0],"bssid":homewifi[1]},\
                                           "longitude":lon,"latitude":lat}})
    if companywifi:
        db.userprofiles.update(userid,{"$set":{"timestamp":datetime.datetime.now(),\
                                           "companywifi":{"ssid":companywifi[0],"bssid":companywifi[1]}}})        
    allconwifi_list = []
    for i in allconwifitime:
        allconwifi_list.append({"ssid":i[0],"bssid":i[1],"timelong":allconwifitime[i][0],"longitude":allconwifitime[i][1],"latitude":allconwifitime[i][2]})
    db.userprofiles.update(userid,{"$set":{"timestamp":datetime.datetime.now(),\
                                           "allconwifitime" :allconwifi_list}})
    return homewifi


        
def wifienv_compare(wifienv1,wifienv2):
    #功能:比较wifienv1环境与wifienv2中，wiif相同的个数
    wifienv1_bssid = []
    for i in wifienv1:
        if  i["bssid"] is not None and i["bssid"] not in wifienv1_bssid:
           wifienv1_bssid.append( i["bssid"])
    count = 0
    for j in wifienv2:
        if  j["bssid"] in wifienv1_bssid:
            count += 1
    print count
    return count

def settime_point(timepoint300,k,settime,m):
    global timepoint_id
    for j in range(k,-1,-1):
        n = log_item(lines[j])
        time = (m.timestamp- n.timestamp).seconds
        if n.lat != 0 and m.wifienv and n.wifienv and time > settime - 60 and time < settime + 60:
            count = wifienv_compare(m.wifienv,n.wifienv)
            if count < 2:
                timepoint_id += 1
                timepoint300.append({"latitude":n.lat,"longitude":n.lon,"wifienv":n.wifienv,"remindnums":0,"id":timepoint_id})
                print n.timestamp
                break
        if time > settime + 60:
            break    

def time_point(lines,l,settime1,settime2,collection):
    print l
    timepoint300 = []
    timepoint600 = []
    print homewifi
    k = 0
    i = 0
    while(i < l):
        m = log_item(lines[i])
        if m.activity :
            print m.timestamp,m.activity
            k = i
            if k != 0:
                settime_point(timepoint300,k,settime1,m)
                settime_point(timepoint600,k,settime2,m)
            i = i + 300
        else:
            i = i+1
    db.userprofiles.update(userid,{"$set":{"timestamp":datetime.datetime.now(),"timepoints(300s)":timepoint300,\
                                               "timepoints(600s)":timepoint600}})

    
def all_user(lines_userid):
    # 功能：查找所有的userid
    alluser = []
    for line in lines_userid:
        if  line["userid"] not in alluser:
            alluser.append(line["userid"])
    return alluser  

       
if __name__=='__main__':
    A = datetime.datetime.now()
    client = MongoClient('10.120.22.209',27017)
    db = client['smartHome']
    collection = db.userprofiles
    lines_userid = db.locations.find({}, {"userid" : 1,"_id":0})
    alluser =  all_user(lines_userid)
    t0 = date.today()-timedelta(days = 14)
    d = datetime.datetime(t0.year, t0.month, t0.day,0,0,0,0)
    for each in alluser:
        userid = {"userid": each}
        print userid
        timepoint_id = 0
        userline = db.userprofiles_copy.find_one(userid)
        if userline  is None:
            db.userprofiles_copy.insert(userid)   
        lines = db.locations.find( {"$and": [ userid,{ "timestamp": { "$gt": d }}]}).sort("timestamp",1)
        l = lines.count()
        homewifi  =  home_companywifi(userid,lines,l,collection)
        print homewifi
        time_point(lines,l,300,600,collection)
    B = datetime.datetime.now()
    print (A - B).seconds/60.0



