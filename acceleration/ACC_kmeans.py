#coding=utf-8
#########################################  
# ACC_kmeans:  
# 用法说明：输入文件，输出图像及准确率            
#########################################  


import numpy as np
import random
import math
import matplotlib.pyplot as plt
from numpy import *
from mpl_toolkits.mplot3d import Axes3D
from collections import Counter


def autoNorm(dataSet):
    #数据标准化处理
    minVals=dataSet.min(0)
    maxVals=dataSet.max(0)
    ranges=maxVals-minVals
    normMat=zeros(shape(dataSet))
    size=normMat.shape[0]
    normMat=dataSet-tile(minVals,(size,1))
    normMat=normMat/tile(ranges,(size,1))
    return normMat       

def euclDistance(vector1, vector2):
    #计算欧式距离
    return sqrt(sum(power(vector2 - vector1, 2)))          


def initCentroids(dataSet, k):
    #选取初始点，取距离较远的点
    numSamples, dim = dataSet.shape  
    centroids = zeros((k, dim))
    index = int(random.uniform(0, numSamples))
    centroids[0, :] = dataSet[index, :]
    for i in range(1,k):
        maxDistance = 0
        maxindex = 0
        for j in range(numSamples):
                Distance = sum([euclDistance(centroids[m-1, :], dataSet[j,:]) for m in range(1,i+1)])
                if maxDistance < Distance:
                      maxDistance = Distance
                      maxindex = j
        centroids[i, :] = dataSet[maxindex,:]                    
    #print 'centroids' ,centroids
    return centroids         


# k-means cluster  
def kmeans(dataSet, k):  
    numSamples = dataSet.shape[0]   
    clusterAssment = mat(zeros((numSamples, 2)))  
    clusterChanged = True  
  
    #1：质心初始化
    centroids = initCentroids(dataSet, k)  
  
    while clusterChanged:  
        clusterChanged = False  
        for i in xrange(numSamples):  
            minDist  = 100000.0  
            minIndex = 0  
            #2：对每个样本点，找到最近的质心，clusterAssment第一列存储样本点所属类的标号，第一列存储存储这个示例及其质心之间的误差
            for j in range(k):
                distance = euclDistance(centroids[j, :], dataSet[i, :])
                if distance < minDist:  
                    minDist  = distance  
                    minIndex = j  
      
            #3：更新集合，直到clusterChanged 存储样本点所属类的标号不再发生变化
            if clusterAssment[i, 0] != minIndex:  
                clusterChanged = True  
                clusterAssment[i, :] = minIndex, minDist**2

  
        #4：更新质心  
        for j in range(k):
            pointsInCluster = dataSet[nonzero(clusterAssment[:, 0].A == j)[0]]
            centroids[j, :] = np.mean(pointsInCluster,axis = 0)

    return centroids, clusterAssment    


def showCluster(dataSet, k, centroids, clusterAssment):
    #画图
    numSamples, dim = dataSet.shape
    mark = ['r', 'b', 'g', 'k']
    if k > len(mark):  
        print "Sorry! Your k is too large! please contact Zouxy"  
        return 1
    if dim > 3:  
        print "Sorry! Your dim is too large! please contact Zouxy"  
        return 1 
    if dim == 2:
        #二维图
        mark = ['or', 'ob', 'og', 'ok', '^r', '+r', 'sr', 'dr', '<r', 'pr']
        for i in xrange(numSamples):
            markIndex = int(clusterAssment[i, 0])  
            plt.plot(dataSet[i, 0], dataSet[i, 1], mark[markIndex])
        plt.show()
    if dim == 3:
        #三维图
        cm = plt.get_cmap("RdYlGn")
        fig = plt.figure()
        ax3D = fig.add_subplot(111, projection='3d')
        mark = ['r', 'b', 'g', 'k']
        for i in xrange(numSamples):
            markIndex = int(clusterAssment[i, 0])
            ax3D.scatter(dataSet[i, 0], dataSet[i, 1],dataSet[i, 2], c=mark[markIndex])
        plt.show()
    
def accuracy(dataSet,clusterAssment):
    # 计算准确率
    dataSet = np.append( dataSet, eigen_fact_matrix[:,-1], 1)
    numSamples, dim = dataSet.shape
    mark_fact = {}
    for i in xrange(numSamples):
        markIndex = int(clusterAssment[i, 0])
        if mark_fact.get(markIndex) is None:
            mark_fact[markIndex]=[]
        mark_fact[markIndex].append(dataSet[i,-1])
    for i in mark_fact:
         a=Counter(mark_fact[i])
         print a, "   the max class :" ,float(max(a.values()))/sum(a.values())

if __name__=='__main__':
    filename = 'D:/sensor_data/dataset_606666/606666/CenceMeRawData1/CenceMeLiteLog1_en_std.txt'
    f=open(filename,'r')
    dataSet=[]
    line=f.readline()
    while len(line):
        line=line.replace("0.0]","5]")
        line1=map(float,line[1:-2].split(','))      
        dataSet.append(line1)
        line=f.readline()
    eigen_fact_matrix = mat(dataSet)
    dataSet = eigen_fact_matrix[:,:-1]
    k = 3
    centroids, clusterAssment = kmeans(dataSet, k)
    print "show the result..."
    showCluster(dataSet, k, centroids, clusterAssment)
    accuracy(dataSet,clusterAssment)
    f.close()

    
  
