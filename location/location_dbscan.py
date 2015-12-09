#coding=utf-8
#########################################  
# dbscan： 
# 用法说明：读取文件
#       生成路径文件及簇文件，输出分类准确率  
#########################################  


from matplotlib.pyplot import *
import matplotlib.pyplot as plt
from collections import defaultdict  
import random
from math import *
import numpy
import datetime
from dateutil.parser import parse
import datetime
import time



def dataset(filename):
    #读取原始文件
    lines = open(filename,'r').readlines()
    l = len(lines)
    all_points = [] 
    for i in range(l):
        if lines[i].strip():
            line = lines[i].split()
            time = line[0] +' '+ line[1]
            lat = float(line[4])
            lon = float(line[6])
            all_points.append([lat,lon,time])
    return all_points

def datarevise(all_points):
    #数据平滑处理
    point_new = []
    all_points1 = np.array(all_points)
    l = len(all_points)
    for i in range(2,l-3):
        lat_lon = np.array(all_points1[i-2:i+3,:-1],dtype = float).mean(0)
        point_new.append([lat_lon[0],lat_lon[1],all_points1[i][-1]])
    return point_new

 
def dist(p1, p2):
    #计算亮点之间的距离
    a = cos(p1[0])*cos(p2[0])
    b = sin(p1[0])*sin(p2[0])*cos(p2[1]-p1[1])
    if a+b >=1:
        return 0
    return acos(float(a+b))*6371*pi/180

def find_core(all_points,E,minPts):
    #查找核心点
    #输出：核心点，要绘制的点，非核心点
    other_points =[]  
    core_points=[]  
    plotted_points=[]
    for point in all_points:
        point.append(0) # 初始点标号为0
        total = 0 #计数：对每个点周围大于给定距离的点的个数
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
    #在非核心点查找边界点
    #输出：边界点，要绘制的点
    border_points=[]
    for core in core_points:
        for other in other_points:
            if dist(core,other) <= E:#边界点的与核心点的距离小于E
                border_points.append(other)
                plotted_points.append(other)
    return border_points,plotted_points


def algorithm(all_points,core_points,border_points,plotted_points,E):
    # 返回簇，噪声点
    
    #将所有的核心点分成不同的簇
    cluster_label = 0
    for point in core_points:
        if point[-1] == 0:
            cluster_label += 1
            point[-1] = cluster_label
        for point2 in plotted_points:
            distance = dist(point2,point)
            if point2[-1] ==0 and distance <= E:
                point2[-1] =point[-1]
    #将点集标号类型写成字典格式        
    cluster_dict = {}
    for point in plotted_points:
        if cluster_dict.get(point[-1]) is None:
            cluster_dict[point[-1]] = [point[0:-1]]
        else:
            cluster_dict[point[-1]].append(point[0:-1])

    #将簇中各个点按时间排序
    cluster_dict_sort = {}
    for lable in  cluster_dict:
        cluster_dict_sort.setdefault(lable,[])
        cl = np.array(cluster_dict[lable])
        cl_sort = cl[cl[:,-1].argsort()]
        cluster_dict_sort[lable] = cl_sort
        
    #噪声点，既不在边界点也不在核心点中    
    noise_points=[]
    for point in all_points:
        if  point not in core_points and  point not in border_points:
            noise_points.append(point[0:-1])
    return cluster_dict_sort,noise_points



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

def matplotshow(cluster_dict,no_split,name):
    #画出各个簇
    markers = ['or', 'ob', 'og', 'ok', '^r', '+r', 'sr', 'dr', '<r', 'pr']
    i=0
    for lable in cluster_dict:
        for j in cluster_dict[lable]:
            plot(j[0], j[1],markers[i])
        i += 1
        i = i%10
        print i            
    #画出路径
    markers = ['r', 'b', 'g', 'k', 'c', 'y', 'm',]
    l =len(no_split)
    for i in range(l):
        path = np.array(no_split[i])
        plt.plot(path[:,0],path[:,1],markers[i%7])
        print i
    title(" clusters created with E ="+str(E)+" Min Points="+str(minPts)+" total points="+str(len(all_points))+" noise Points = "+ str(len(noise_points)))
    savefig(name)
    show()

            
def datewrite(no_split,filename,mark): 
    f = open(filename,'w+')
    for path in no_split:
        f.write( str(mark) +'\n')
        for no_path in path:
            f.write(str(list(no_path))+'\n')     
    f.close()

def datewrite1(no_split,filename,mark): 
    f = open(filename,'w+')
    for path in no_split:
        for no_path in path:
            f.write( str(mark) +'\n')
            for j in no_path:
                f.write(str(list(j))+'\n')     
    f.close()
    
if __name__ == '__main__':
    filename = 'D:/sensor_data/sensor/gps/location_zh0710.txt'
    all_points_old = dataset(filename)
    all_points = datarevise(all_points_old)
    E,minPts = 0.1,10
    core_points,plotted_points,other_points = find_core(all_points,E,minPts)
    border_points,plotted_points =  find_border(core_points,plotted_points,other_points,E)
    cluster_dict,noise_points = algorithm(all_points,border_points,core_points,plotted_points,E)
    difftime = 1200
    no_split = durtime(noise_points,difftime)
    matplotshow(cluster_dict,no_split,"location_zh0710.png")
    filename = 'D:/sensor_data/sensor/gps/location_zh0710_no_split.txt'
    datewrite(no_split,filename,'path')
    filename = 'D:/sensor_data/sensor/gps/location_zh0710_cluster.txt'
    datewrite(cluster_dict.values(),filename,'lable')


