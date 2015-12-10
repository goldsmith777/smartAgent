#coding:utf-8

# 根据加速度原始数据 生成特征矩阵

import random
import math
import matplotlib.pyplot as plt
from numpy import *
import numpy as np
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
        line=line.strip().split(" ")
        if '#' in line[0]:
            print(' ')
        else:
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
    filename = 'D:/SmartAgent/Data/LenovoSportCollectData.txt'
    f=open(filename,'r')
    classify = 0
    count=0
    allAccWithLabel = [[],[],[],[]]
    singleAcc =[]
    Act_fact = []
    for line in f.readlines():
    # 将数据读入allAccWithLabel列表中，并按类别存放在4个子列表中
        line=line.strip().split(" ")
        if '####' in line[0]:
            # print('tagline')
            if 'static' in line[0]:
                classify = 1
            elif 'walk' in line[0]:
                classify = 2
            elif 'run' in line[0]:
                classify = 3
        # elif 'GYRO' in line[3]:
        #       print('GYRO_data')
        # elif 'GRA' in line[3]:
        #       print('GRA_data')
        elif 'ACC' in line[3]:
            singleAcc =[float(line[6].strip().split(":")[-1]),float(line[7].strip().split(":")[-1]),float(line[8].strip().split(":")[-1]),classify]
            allAccWithLabel[classify].append(singleAcc)
    # print len(allAccWithLabel[0]),len(allAccWithLabel[1]),len(allAccWithLabel[2]),len(allAccWithLabel[3])
    # 以上
    accDataSet=[[],[],[],[]]
    temp=[]
    for i in range(4):
    # 将单次传感器数据组织为15次一组的形式，存放于accDataSet中，形式如：[[[...0]...[...0]],[[...1]...[..1]],[],[]]
        for singleAccData in allAccWithLabel[i]:
            for item in singleAccData[:-1]:
                temp.append(item)
                if len(temp)>=45:
                    temp.append(i)
                    accDataSet[i].append('')
                    accDataSet[i][-1]= temp
                    temp=[]
    # print accDataSet[1][10][-1],accDataSet[0][10][-1],accDataSet[2][10][-1],len(accDataSet[1][10])
    # 以上
    accFeatureXYZ =[[],[],[]]
    for i in range(4):
        accDataSetArray=np.array(accDataSet[i])
        print type(accDataSetArray)





    # accDatasetWithLabel = np.array(allAccWithLabel)
    # for i in range(4):
    #     print len(allAccWithLabel[i])
    # else:
    #         AccXYZ =[[],[],[]]
    #         Acc = line[-1].split("*")
    #         for Accxyz in Acc:
    #             Accxyz=Accxyz.split(",")
    #             if len(Accxyz) == 3:
    #                 AccXYZ[0].append(float(Accxyz[0]))
    #                 AccXYZ[1].append(float(Accxyz[1]))
    #                 AccXYZ[2].append(float(Accxyz[2]))
    #         AccXYZ = np.array(AccXYZ)
    #         num = float(AccXYZ.shape[1])
    #         df = DataFrame(AccXYZ)
    #         skew = df.skew(1) #偏度
    #         kurt = df.kurt(1) #峰度
    #         mean = AccXYZ.mean(1)#均值
    #         std = AccXYZ.std(1)#标准差
    #         fft = np.fft.fft(AccXYZ)#傅里叶
    #         pass_mean = passmean(AccXYZ,mean)/num#均值穿越次数
    #         eigen_choose1 = np.append(np.array(skew),np.array(kurt))
    #         eigen_choose2= np.append(mean,pass_mean)
    #         eigen_choose3= np.append(std,pow(abs(fft),2).sum(1)/num)
    #         eigen_choose12 = np.append(eigen_choose1,eigen_choose2)
    #         eigen_choose = np.append(eigen_choose12,eigen_choose3)
    #     if  'ACT' in line[0] :
    #         Act = line[-1].split(",")
    #         eigen_choose = np.append(eigen_choose,int(Act[-1]))
    #         eigen_list.append(list(eigen_choose))
    # f.close()
    # eigen_fact_matrix = avg_data(eigen_list)
    # return eigen_fact_matrix
    #





    # filename3='D:/sensor_data/dataset_606666/606666/CenceMeRawData4/std_en_data15.txt'
    # f3=open(filename3,'w')
    # dataSet = eigen_fact_matrix[:,12:]
    # for i in dataSet:
    #     f3.write(str(list(i))+'\n')
    # f3.close()
