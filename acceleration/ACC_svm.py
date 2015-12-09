#coding=utf-8
#########################################  
# ACC_svm:  
# 用法说明：输入文件，调用sklearn，输出准确率            
#########################################

import math
import numpy as np
from numpy import *
import random
from sklearn import svm
def dataset(filename):
    f=open(filename,'r')
    trainingSet=[]
    line=f.readline()
    while len(line):
        line1=map(float,line[1:-2].split(','))      
        trainingSet.append(line1)
        line=f.readline()
    return trainingSet

def svm_accuracy(trainingSet,testSet):
    #线性核
    clf =svm.SVC(kernel='linear')
    #多项式核
    #clf = svm.SVC(kernel='poly',degree=3)
    #RBF核(径向基函数)
    #clf = svm.SVC(kernel='rbf') 

    clf.fit(trainingSet[:,:-1], trainingSet[:,-1])
    count = 0
    n_row = testSet.shape[0]
    for i in range(n_row):
        if clf.predict(testSet[:,:-1][i])[0] == testSet[:,-1][i]:
            count += 1
    accuracy = float(count)/n_row
    return  accuracy
    

if __name__=='__main__':
    filename1='D:/sensor_data/sensor/linearaccelero1_std_trainingSet.txt'
    filename2='D:/sensor_data/sensor/linearaccelero1_std_testSet.txt'
    trainingSet = np.array(dataset(filename1))
    testSet = np.array(dataset(filename2))
    print svm_accuracy(trainingSet,testSet)
    
        
        

        

    
    
