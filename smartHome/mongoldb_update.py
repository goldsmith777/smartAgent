# -*- coding: UTF-8 -*-  
#########################################  
# wifi_dbscan_oneDay： 
# 用法说明：功能：更新数据        
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

def all_user(lines_userid):
    # 功能：查找所有的userid
    alluser = []
    for line in lines_userid:
        if  line["userid"] not in alluser:
            alluser.append(line["userid"])
    return alluser

def timepointaddtable(userid,timepoint_str):
    # 功能：更新5分钟的点
    lines_copy =  db.userprofiles_copy.find(userid,{timepoint_str:1,"_id":0})
    lines_temp =  db.userprofiles_temp.find(userid,{timepoint_str:1,"_id":0})
    timepoint300,timepoint1,timepoint2 = [],[],[]
    for i in  lines_copy:
        if i :
            timepoint1 = i[timepoint_str]
        
    for i in  lines_temp:
        if i:
            timepoint2 = i[timepoint_str]
    if timepoint1 != timepoint2:
        timepoint300 = timepoint1 + timepoint2
        db.userprofiles_copy.update(userid,{"$set":{"timestamp":datetime.datetime.now(),timepoint_str:timepoint300}})

def wifiaad(list1,list2):
    # 功能：list1，list2 相同wifi时间相加，不同wifi合并
    for i in list1:
        for j in list2:
            if "bssid" in i.keys() and  "bssid" in j.keys()and  i["bssid"] == j["bssid"]:
                i['timelong'] += j['timelong']
                list2.remove(j)
    list1 += list2
    return list1

def allconwifitimeaddtable(userid,allconwifitime_str):
    # 功能：更新wifi连接时长
    lines_copy =  db.userprofiles_copy.find(userid,{allconwifitime_str:1,"_id":0})
    lines_temp =  db.userprofiles_temp.find(userid,{allconwifitime_str:1,"_id":0})
    list1,list2 = [],[]
    for i in lines_copy:
        if i:
            list1 = i[allconwifitime_str]
    for i in lines_temp:
        if i:
            list2 = i[allconwifitime_str]
    allconwifitime = wifiaad(list1,list2)
    db.userprofiles_copy.update(userid,{"$set":{"timestamp":datetime.datetime.now(),allconwifitime_str:allconwifitime}})

if __name__ == '__main__':
    client = MongoClient('10.120.22.209',27017)
    db = client['smartHome']
    lines_userid = db.locations.find({}, {"userid" : 1,"_id":0})
    alluser =  all_user(lines_userid)
    for each in alluser:
        userid = {"userid": each}
        print userid
        timepointaddtable(userid,"timepoints(300s)")
        timepointaddtable(userid,"timepoints(600s)")
        allconwifitimeaddtable(userid,"allconwifitime")
        
            

            
