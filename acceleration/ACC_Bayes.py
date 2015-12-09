#coding=utf-8
#########################################  
# ACC_Bayes: 贝叶斯 
# 用法说明：读取文件
#         输出分类准确率  
#########################################  

import math
import numpy as np
from numpy import *
import random


def separateByClass(dataset):
# 将训练集按照类标号进行划分，返回字典形式
  separated = {}
  for i in range(len(dataset)):
    vector = dataset[i]
    if (vector[-1] not in separated):
      separated[vector[-1]] = []
    separated[vector[-1]].append(vector)
  return separated

def mean(numbers):
  return sum(numbers)/float(len(numbers))

def stdev(numbers):
  avg = mean(numbers)
  variance = sum([pow(x-avg,2) for x in numbers])/float(len(numbers)-1)
  return math.sqrt(variance)

def summarize(dataset):
  summaries = [(mean(attribute), stdev(attribute)) for attribute in zip(*dataset)] 
  del summaries[-1]
  return summaries

def summarizeByClass(dataset):
  separated = separateByClass(dataset)
  summaries = {}
  for classValue, instances in separated.iteritems():
    summaries[classValue] = summarize(instances)
  return summaries


def calculateProbability(x, mean, stdev):
  exponent = math.exp(-(math.pow(x-mean,2)/(2*math.pow(stdev,2))))
  return (1 / (math.sqrt(2*math.pi) * stdev)) * exponent


def calculateClassProbabilities(summaries, inputVector):
  probabilities = {}
  for classValue, classSummaries in summaries.iteritems():
    probabilities[classValue] = 1
    for i in range(len(classSummaries)):   
      mean, stdev = classSummaries[i]
      x = inputVector[i]
      probabilities[classValue] *= calculateProbability(x, mean, stdev)
    probabilities[classValue] *= float(len(separated[classValue]))/len(separated.values())
  return probabilities


def predict(summaries, inputVector):
  probabilities = calculateClassProbabilities(summaries, inputVector)
  bestLabel, bestProb = None, -1
  for classValue, probability in probabilities.iteritems():
    if bestLabel is None or probability > bestProb:
      bestProb = probability
      bestLabel = classValue
  return bestLabel

def getPredictions(summaries, testSet):
  predictions = []
  for i in range(len(testSet)):
    result = predict(summaries, testSet[i])
    predictions.append(result)
  return predictions

def getAccuracy(testSet, predictions):
  correct = 0
  for x in range(len(testSet)):
    if testSet[x][-1] == predictions[x]:
      correct += 1
  return (correct/float(len(testSet))) * 100.0

def dataset(filename):
# 将文件数据转化为集合的形式
    f=open(filename,'r')
    trainingSet=[]
    line=f.readline()
    while len(line):
        line1=map(float,line[1:-2].split(','))      
        trainingSet.append(line1)
        line=f.readline()
    return trainingSet

if __name__=='__main__':
    filename1='D:/sensor_data/dataset_606666/606666/CenceMeRawData2/std_data7trainingSet.txt'
    filename2='D:/sensor_data/dataset_606666/606666/CenceMeRawData2/std_data7testSet.txt'
    trainingSet = dataset(filename1)
    testSet = dataset(filename2)
    print('Split {0} rows into train={1} and test={2} rows').format(len(trainingSet)+len(testSet), len(trainingSet), len(testSet))
    separated = separateByClass(trainingSet)
    for i in separated:
        print i ,len(separated[i])
    separated1 = separateByClass(testSet)
    for i in separated1:
        print i ,len(separated1[i])   
    summaries = summarizeByClass(trainingSet)
    predictions = getPredictions(summaries, testSet)
    accuracy = getAccuracy(testSet, predictions)
    print('Accuracy: {0}%').format(accuracy)



