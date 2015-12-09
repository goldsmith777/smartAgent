# -*- coding: utf8 -*-
################################################
#                                              #
# 使用knn算法，输出k在(3,30)范围内的准确率           #
#                                              #
################################################

import numpy as np
import random
import math
import matplotlib.pyplot as plt
import operator


def kNNClassify(testSamples,testLabels,samples, labels,k):
    numSamples = samples.shape[0]
    countLabels = []
    for newInput in testSamples:
        diff = np.tile(newInput, (numSamples, 1)) - samples # Subtract element-wise
        squaredDiff = diff ** 2 # squared for the subtract
        squaredDist = np.sum(squaredDiff, axis = 1) # sum is performed by row
        distance = squaredDist ** 0.5
        sortedDistIndices = np.argsort(distance)
        classCount = {} # define a dictionary (can be append element)
        for i in xrange(k):
            voteLabel = labels[sortedDistIndices[i]]
            classCount[voteLabel] = classCount.get(voteLabel, 0) + 1
        maxCount = 0
        for key, value in classCount.items():
            if value > maxCount:
                maxCount = value
                maxIndex = key
        countLabels.append(maxIndex)
    f = [testLabels[i] for i in range(len(countLabels)) if countLabels[i] == testLabels[i]]
    return len(f)


def dataset(filename):
    f=open(filename,'r')
    trainingSet=[]
    line=f.readline()
    while len(line):
        line1=map(float,line[1:-2].split(','))      
        trainingSet.append(line1)
        line=f.readline()
    return trainingSet

if __name__ =='__main__':
    filename1='D:/sensor_data/dataset_606666/606666/CenceMeRawData2/std_data7trainingSet.txt'
    filename2='D:/sensor_data/dataset_606666/606666/CenceMeRawData2/std_data7testSet.txt'
    a = np.array(dataset(filename1))
    b = np.array(dataset(filename2))
    sta = {}
    for k in range(3,30):
        f = kNNClassify(a[:,:-1],a[:,-1],b[:,:-1], b[:,-1],k)
        sta[k] = float(f)/a.shape[0]
    print max(sta.values())
    print sta


