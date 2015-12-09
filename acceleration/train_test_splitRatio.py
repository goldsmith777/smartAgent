#coding=utf-8
#########################################  
# train_test_splitRatio: 
# 用法说明：输入：读取文件
#         功能：按照比例将原始数据随机集分割训练集和测试集
#         输出：写入训练集和测试集文件
#########################################  
import numpy as np
import random
import math
def splitDataset(dataset, splitRatio):
    trainSize = int(len(dataset)*splitRatio)
    trainSet = []
    copy = list(dataset)
    while len(trainSet) < trainSize:
        index = random.randrange(len(copy))    
        trainSet.append(copy.pop(index))    
    return np.array(trainSet), np.array(copy)


def writefilename(filename,trainingSet):
    f1=open(filename,'w')
    for i in trainingSet:    
        f1.write(str(list(i))+'\n')
    f1.close()


if __name__=='__main__':
    filename = 'D:/sensor_data/dataset_606666/606666/CenceMeRawData2/std_data7.txt'
    f=open(filename,'r')
    dataSet=[]
    line=f.readline()
    while len(line):
        line=line.replace("0.0]","5]")
        line1=map(float,line[1:-2].split(','))      
        dataSet.append(line1)
        line=f.readline()
    splitRatio = 0.15
    trainingSet, testSet = splitDataset(dataSet, splitRatio)
    filename1='D:/sensor_data/dataset_606666/606666/CenceMeRawData2/std_data7trainingSet.txt'
    filename2='D:/sensor_data/dataset_606666/606666/CenceMeRawData2/std_data7testSet.txt'
    writefilename(filename1,trainingSet)
    writefilename(filename2,testSet)

