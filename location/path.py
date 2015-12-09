#coding=utf-8
#########################################  
# path： 
# 用法说明：读取由dbscan生成的路径文件及簇文件
#         输出x分钟的点  
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


def dataset(filename,all_path):
    lines = open(filename,'r').readlines()
    l = len(lines)
    path = []
    for i in range(l):
        if len(lines[i])<10:
            if i >0:
                all_path.append(path)
                path = []
        else:
             line = lines[i].replace("[","").replace("]","").replace("'","").split(",")
             path.append([float(line[0]),float(line[1]),line[2].strip()])
        if i == l-1:
            all_path.append(path)           
    return  all_path

            
def dist(p1, p2):
    a = cos(p1[0])*cos(p2[0])
    b = sin(p1[0])*sin(p2[0])*cos(p2[1]-p1[1])
    if a+b >=1:
        return 0
    return acos(float(a+b))*6371*pi/180

def same_cluster(all_cluster,discluster):
    #相似簇合并
    l = len(all_cluster)
    samecluster = []
    for each in range(l):
        samecluster1 = []
        for other in range(each+1,l):
            m = min(len(all_cluster[each]),len(all_cluster[other]))
            if m >10:
                    centre1 = np.array(np.array(all_cluster[each])[:,:2],dtype = float).mean(0)
                    centre2 = np.array(np.array(all_cluster[other])[:,:2],dtype = float).mean(0)
                    if dist(centre1, centre2) < discluster: 
                        if all_cluster[each] not in samecluster1:
                            samecluster1.append(all_cluster[each])
                        samecluster1.append(all_cluster[other])
        if len(samecluster1) != 0:
            samecluster.append(samecluster1)
    add_samecluster = []
    for i in samecluster:
        add_samecluster += i     
    for j in all_cluster:
        if j not in add_samecluster:    
            samecluster.append([j])
    return samecluster


def large_cluster(samecluster):
    # 返回点数最大的两个簇
    large_clu = []
    l = []
    for i in samecluster:
        l.append( sum([len(j)for j in i]))
    l = np.array(l)
    index_sort = l.argsort()[::-1]
    for i in  index_sort[0:2]:
        cluster = []
        for j in samecluster[i]:
                cluster += j
        large_clu.append(cluster)
    return large_clu

def find_homecom(large_clu):
    # 区分公司与家的两个簇，home_comp[0]是家，home_comp[1]是公司
    home_comp = [[],[]]
    for clu in large_clu:
        count = [0,0]
        for each_point in clu:
            time_point = parse(each_point[2].split()[-1])
            if time_point > parse('00:00:00') and time_point < parse('06:00:00'):
                count[0] += 1
            if time_point > parse('10:00:00') and time_point < parse('16:00:00'):
                count[1] += 1
        if count[0] > count[1]:
            home_comp[0].extend(clu)
        else:
            home_comp[1].extend(clu)
    return home_comp

def home_comp_wify( home_comp):
    # 找到公司与家的wifi,home_comp_wify[0]是家的wifi，home_comp_wify[1]是公司的wifi，
    home_comp_wify = [[],[]]
    for i in range(len(home_comp)):
        wifi_dict = {}
        for point in home_comp[i]:
            wifi = point[3]
            wifi_dict.setdefault(wifi,0)
            wifi_dict[wifi] += 1
        a=sorted(wifi_dict.items(),key = lambda asd:asd[1],reverse = True )
        home_comp_wify[i] = a[0][0]
    return home_comp_wify

def round_wify(home_comp):
    # 找到家附近的wifi
    round_wify = [[],[]]
    for i in range(len(home_comp)):
        wifi_dict = {}
        for point in home_comp[i]:
            wifi = point[4].split()
            for each_wifi in wifi:
                wifi_dict.setdefault(each_wifi,0)
                wifi_dict[each_wifi] += 1
        wifi_sort = sorted(wifi_dict.items(),key = lambda asd:asd[1],reverse = True )
        round_wify[i] = wifi_sort[:10]
    return round_wify
    
               
def same_path(home_comp,all_path):
    # 找到回家/回公司的两大条路，samepath[1]是回家的路，samepath[0]是去公司的路
    samepath = [[],[]]
    for path in all_path:
        dis_list = []
        for clu in home_comp:
            centre = np.array(np.array(clu)[:,:2],dtype = float).mean(0)
            dis_list.append(dist(centre, path[-1][:2]))
        mindis = min(dis_list)
        if mindis < 1: 
            samepath[dis_list.index(mindis)].append(path)
    return samepath

            
def time_point(samepath,settime):
    # 在每条路上找到20分钟的点(取左右2min内的点)，point_time[1]是回家的路上20分钟的点，point_time[0]是去公司的路上20分钟的点
    point_time = [[],[]]
    for i in range(2):
        for eachpath in samepath[i]:
            path_point = []
            time_dur =(parse(eachpath[-1][2]) - parse(eachpath[0][2])).seconds
            if time_dur > settime:
                print "start_time:",parse(eachpath[0][2]),"  end_time:",parse(eachpath[-1][2]),"  time spend on the road(min):",time_dur/60.0
                for j in range(len(eachpath)-1,0,-1):
                    if (parse(eachpath[-1][2]) - parse(eachpath[j][2])).seconds >settime:
                        break
                    k_list = []
                    for k in  range(len(eachpath)-1,0,-1):
                        if (parse(eachpath[k][2]) - parse(eachpath[j][2])).seconds < 120:
                            k_list.append(k)
                        if (parse(eachpath[k][2]) - parse(eachpath[j][2])).seconds < 120:
                            k_list.append(k)                                                       
                path_point.extend(eachpath[min(k_list):max(k_list)+1])                       
            if len(path_point) != 0:
                point_time[i].append(path_point)
    return point_time    


def same_point(point_time,dispoint):
    # 合并相同20分钟的点放在同一个list中，samepoint[1]是回家的路上20分钟的点，samepoint[0]是去公司的路上20分钟的点
    samepoint = [[],[]]
    for i in range(2):
        samepoint2 = []
        path_point = point_time[i]
        l = range(len(path_point))
        for each in l:
            samepoint1 = []
            l.remove(each)
            for other in l:
                centre1 = np.array(np.array(path_point[each])[:,:2],dtype = float).mean(0)
                centre2 = np.array(np.array(path_point[other])[:,:2],dtype = float).mean(0)
                if dist(centre1, centre2) < dispoint: 
                    if path_point[each] not in samepoint1:
                            samepoint1.append(path_point[each])
                    samepoint1.append(path_point[other])
                    l.remove(other)
            if len(samepoint1) != 0:
                samepoint[i].append(samepoint1)
        for index in l:
            samepoint[i].append([path_point[index]])
        samepoint[i] = samepoint2
    return samepoint                    
   

def path_timecentre(samepoint):
    # 合并20分钟的点取均值，time_centre[1]是回家的路上20分钟的均值点，time_centre[0]是回家的路上20分钟的均值点
    time_centre = [[],[]]
    for i in range(2):
        centre2 = []
        for path in samepoint[i]:
            centre1 = []
            for pathpoint in path:
                centre1.append(list(np.array(np.array(pathpoint)[:,:2],dtype = float).mean(0)))
            time_centre[i].append(list(np.array(centre1).mean(0)))             
    return time_centre
                


def matplotshow(samecluster,all_path,time_centre):
    #画图
    markers = ['or', 'ob', 'og', 'om', '^r', '+r', 'sr', 'dr', '<r', 'pr']
    i=0
    for paircluster in samecluster:
        for each_cluster in paircluster:
            for each_point in each_cluster:
                plot(each_point[0], each_point[1],markers[i])
        i += 1
        i = i%10
        print i
        
    markers = ['r', 'b', 'g', 'k', 'c', 'y', 'm',]
    i=0
    l = len(all_path)
    for j in range(l):
        each_path = np.array(all_path[i])
        plt.plot(each_path[:,0],each_path[:,1],markers[i%7])
        i += 1
        i = i%10
        print i

    for k in range(len(time_centre)):
        for eachcentre in time_centre[k]:
            plot(eachcentre[0],eachcentre[1],'b*')
    show()
    

if __name__=='__main__':
    all_path =[]
    filename = 'D:/sensor_data/sensor/gps/location_zh0710_no_split.txt'
    all_path=dataset(filename,all_path)
    print len(all_path)
    all_cluster = []
    filename = 'D:/sensor_data/sensor/gps/location_zh0710_cluster.txt'
    all_cluster =dataset(filename,all_cluster)
    print len(all_cluster)



    dispoint = 1
    discluster = 0.2
    samecluster = same_cluster(all_cluster,discluster)
    large_clu = large_cluster(samecluster)
    home_comp = find_homecom(large_clu)
    samepath = same_path(large_clu,all_path)
    settime = 300
    point_time1 = time_point(samepath,settime)
    samepoint1 = same_point(point_time1,dispoint)
    time_centre1 = path_timecentre(samepoint1)

    settime = 0
    dispoint = 0.8
    point_time = time_point(samepath,settime)
    samepoint = same_point(point_time,dispoint)
    time_centre = path_timecentre(samepoint)
