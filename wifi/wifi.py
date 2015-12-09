#coding=utf-8
#########################################  
# wifi： 
# 用法说明：读取数据
#         输出wifi强度经过加权后的值
#########################################

from matplotlib.pyplot import *
import matplotlib.pyplot as plt
from collections import defaultdict  
from math import *
import numpy
import datetime
from dateutil.parser import parse
import datetime
import time

def dataset(filename):
    #原始数据处理
    lines = open(filename,'r').readlines()
    l = len(lines)
    data = []
    for i in range(l):
        if lines[i].strip():
            data_list = []
            line = lines[i].split('\t')
            data_list.extend([" ".join(line[0].split(" ")[:-1]),line[1],line[2].replace("\"","")+" "+ line[3],line[4]])
            data_list.extend(line[5:-1])
            data.append(data_list)
    return data

def home_wifi(data):
    #输出家里的wifi
    homewifi = {}
    for i in data:
        if not i[2].startswith("0x"):
            #if parse(i[0].split()[-1]) > parse('20:00:00') and parse(i[0].split()[-1]) < parse('23:00:00'):
            #if parse(i[0].split()[-1]) > parse('00:00:00') and parse(i[0].split()[-1]) < parse('08:30:00'):
                homewifi.setdefault(i[2],0)
                homewifi[i[2]] += 1
    wifi_sort = sorted(homewifi.items(),key = lambda asd:asd[1],reverse = True )
    print wifi_sort[0][0]
    return wifi_sort[0][0]
            


def data_wifi(data):
    #生成wifi字典
    l = len(data)
    datawifi = []
    for i in range(1,l):
        j = data[i]
        wifi_dict = {}
        wifi_time_dict = [[j[0],j[1],j[2],j[3]],wifi_dict]
        wifi_round = j[4:]
        for k  in range(0,len(wifi_round),3):
            wifi_dict.setdefault(wifi_round[k]+" "+wifi_round[k+1],int(wifi_round[k+2]))
        datawifi.append(wifi_time_dict)
    return datawifi



def  wifi_compare(datawifi,rssi):
    #比较wifi强度差值
    l = len(datawifi)
    wificompare = []
    for i in range(1,l):
        wifi_diff = {}
        wifi_time_diff = [datawifi[i][0],wifi_diff]
        wifi_dict = datawifi[i-1][1]
        wifi_dict1 = datawifi[i][1]
        for wifi in wifi_dict1:
            if wifi in wifi_dict:
                diff = wifi_dict1[wifi] - wifi_dict[wifi]
            else:
                 diff = wifi_dict1[wifi] - (rssi)
            if abs(diff) > 0 :
                wifi_diff.setdefault(wifi,diff)
        for wifi in wifi_dict:
            if wifi not in wifi_dict1:
                diff = rssi - wifi_dict[wifi]
            if abs(diff) > 0 :
                wifi_diff.setdefault(wifi,diff)
        #print wifi_time_diff[0][0],wifi_time_diff[0][1],wifi_time_diff[0][2],wifi_time_diff[0][3],wifi_time_diff[1]
        wificompare.append(wifi_time_diff)
    return wificompare



def change_wifi(wificompare,homewifi,num,settime):
    #在检测有家里wifi出现时，有剧烈变化的前10个，（包括家里的wifi）
    chang_dict = {}
    chang_list = []
    l = len(wificompare)
    for i in range(l):
        if homewifi in wificompare[i][1].keys():
            break
    for j in range(i+1,l): 
        diff_time = (parse(wificompare[j][0][0]) - parse(wificompare[i][0][0])).seconds
        if diff_time  > settime:
            break   
    for k in range(i,j+1):
        for wifi in  wificompare[k][1]:
            chang_dict.setdefault(wifi,0)
            chang_dict[wifi] += abs(wificompare[k][1][wifi])
    chang_dict_sort = sorted(chang_dict.items(),key = lambda asd:asd[1],reverse = True )
    changewifi = []
    for wifi_assi in chang_dict_sort:
        chang_list.append(wifi_assi[0])
        print wifi_assi
    changewifi = chang_list[:num]
    if homewifi in changewifi:
        return  changewifi
    else:
        changewifi = changewifi +[homewifi]
        return changewifi    
def all_wifi(wificompare):
    #输出所有wifi变化的名字
    allwifi = []
    for i in wificompare:
        for wifi in  i[1].keys():
            if wifi not in allwifi:
                allwifi.append(wifi)
    return allwifi

def wifi_weigh(wificompare,homewifi,weigh,num,settime):
    #输出wifi 权重
    wifiweigh = []
    allwifi = all_wifi(wificompare)
    l = len(allwifi)
    changewifi = change_wifi(wificompare,homewifi,num,settime)
    m = len(changewifi)
    for i in wificompare:
        get_rssi = 0
        if  len(i[1]) != 0:
            for wifi in i[1]:
                if  wifi in changewifi :
                    if wifi in homewifi :
                        get_rssi += weigh/m*3*abs(i[1][wifi])
                    else:
                        get_rssi += weigh/m*abs(i[1][wifi])
                else:
                    get_rssi += (1-weigh)/(l-1)*abs(i[1][wifi])
            if  get_rssi > 1:
                #print i[0],"\t",get_rssi
                wifiweigh.append([i[0],get_rssi,i[1]])
    return wifiweigh


def rssi0(wifiweigh,homewifi):
    l = len(wifiweigh)
    for i in range(l):
        if homewifi in  wifiweigh[i][2].keys():
            break
    for j in range(i+1,l):
        diff_time = (parse(wifiweigh[j][0][0]) - parse(wifiweigh[i][0][0])).seconds
        if diff_time  > 20:
            break
    if (parse(wifiweigh[l-1][0][0]) - parse(wifiweigh[i][0][0])).seconds <20:
        j = l-1
    rssi = np.array(np.array(wifiweigh)[:,1],dtype = float)[i:j+1].mean(0)
    print rssi
    return rssi        
          
def pass_rssi(wifiweigh,homewifi):
    # 输出wifi变化强度 > 前25项的均值
    l = len(wifiweigh)
    passrssi = []
    rssi = rssi0(wifiweigh,homewifi)
    for i in range(l):
        if wifiweigh[i][1] >= rssi :
            passrssi.append(wifiweigh[i])
    for i in passrssi:
        print i[0][0], i[0][1], i[0][2], i[0][3], "\t",i[1]
    return passrssi
        
if __name__ == '__main__':
    filename = 'D:/sensor_data/sensor/wifi/wifi_leave_gt0722.txt'
    data = dataset(filename)
    homewifi = home_wifi(data)
    #homewifi = 'oldwifi 20:76:93:24:4e:a4'
    datawifi = data_wifi(data)
    rssi = -96
    wificompare = wifi_compare(datawifi,rssi)
    weigh = 0.8
    num = 5
    settime = 20
    wifiweigh = wifi_weigh(wificompare,homewifi,weigh,num,settime)
    pass_rssi(wifiweigh, homewifi)

