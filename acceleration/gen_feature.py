#coding=utf-8
#########################################  
# gen_feature:根据加速度原始数据 生成特征矩阵 
# 用法说明：filedata(filename)生成特征矩阵          
#########################################  

import numpy as np
import random
import math
import matplotlib.pyplot as plt
from numpy import *
from mpl_toolkits.mplot3d import Axes3D
from collections import Counter
from pandas import Series,DataFrame
import pandas as pd


def avg_data(dataSet):
    #使各个状态的数据量一样多
    sitting = []
    running = []
    walking = []
    standing = []  
    for item in dataSet:
        if item[-1] == 0:
            sitting.append(item)
        elif item[-1] == 1:
            running.append(item)
        elif item[-1] == 2:
            walking.append(item)
        elif item[-1] == 5:
            standing.append(item)
    minNum = min(len(sitting),len(running),len(walking),len(standing))
    dataSet_new = sitting[:minNum] + running[:minNum] + walking[:minNum] + standing[:minNum]
    return np.array(dataSet_new)

def passmean(A,B):
    #均值穿越次数
    n_row,n_line = A.shape
    passmean = repeat(0,n_row)
    for i in range(n_row):
        for j in range(n_line-1):
            if (A[i][j]<B[i]) and (A[i][j+1]>B[i]):
                passmean[i] += 1
            if (A[i][j]>B[i]) and (A[i][j+1]<B[i]):
                passmean[i] += 1
    return passmean

def filedata(filename):
    f=open(filename,'r')
    eigen_list = []
    Act_fact = []
    for line in f.readlines():
        line=line.strip().split(":")
        if  'ACC' in line[0] :
            AccXYZ =[[],[],[]]
            Acc = line[-1].split("*")
            for Accxyz in Acc:
                Accxyz=Accxyz.split(",")
                if len(Accxyz) == 3:
                    AccXYZ[0].append(float(Accxyz[0]))
                    AccXYZ[1].append(float(Accxyz[1]))
                    AccXYZ[2].append(float(Accxyz[2]))
            AccXYZ = np.array(AccXYZ)
            num = float(AccXYZ.shape[1])
            df = DataFrame(AccXYZ)
            skew = df.skew(1) #偏度
            kurt = df.kurt(1) #峰度
            mean = AccXYZ.mean(1)#均值
            std = AccXYZ.std(1)#标准差
            fft = np.fft.fft(AccXYZ)#傅里叶
            pass_mean = passmean(AccXYZ,mean)/num#均值穿越次数
            eigen_choose1 = np.append(np.array(skew),np.array(kurt))
            eigen_choose2= np.append(mean,pass_mean)
            eigen_choose3= np.append(std,pow(abs(fft),2).sum(1)/num)
            eigen_choose12 = np.append(eigen_choose1,eigen_choose2)
            eigen_choose = np.append(eigen_choose12,eigen_choose3) 
        if  'ACT' in line[0] :
            Act = line[-1].split(",")
            eigen_choose = np.append(eigen_choose,int(Act[-1]))
            eigen_list.append(list(eigen_choose))
    f.close()    
    eigen_fact_matrix = avg_data(eigen_list)
    return eigen_fact_matrix




if __name__=='__main__':
    filename = 'D:/sensor_data/dataset_606666/606666/CenceMeRawData2/CenceMeLiteLog7.txt'
    eigen_fact_matrix = filedata(filename)
    
    filename1='D:/sensor_data/dataset_606666/606666/CenceMeRawData2/fft_en_data7.txt'
    f1=open(filename1,'w')
    dataSet = eigen_fact_matrix[:,15:]
    for i in dataSet:    
        f1.write(str(list(i))+'\n')
    f1.close()

    filename2='D:/sensor_data/dataset_606666/606666/CenceMeRawData2/std_data7.txt'
    f2=open(filename2,'w')
    dataSet = eigen_fact_matrix[:,[12,13,14,-1]]
    for i in dataSet:    
        f2.write(str(list(i))+'\n')
    f2.close()   


    filename3='D:/sensor_data/dataset_606666/606666/CenceMeRawData4/std_en_data15.txt'
    f3=open(filename3,'w')
    dataSet = eigen_fact_matrix[:,12:]
    for i in dataSet:    
        f3.write(str(list(i))+'\n')
    f3.close()   
