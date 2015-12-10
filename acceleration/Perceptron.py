#coding:utf-8

import matplotlib.pyplot as plt
import numpy as np

# 简单感知机学习算法
# 感知机模型:f(x)=sign(w*x+b)
# 算法策略:损失函数:L(w,b)=y(w*x+b)
# 学习算法:梯度下降法



class Perceptron:
  # 感知机类，一共八个方法，分别是:
  # __init__:构造函数
  # isError:判断是不是误分点
  # adjust:利用梯度下降法修改参数
  # train:开始训练数据
  # add:两个向量的加法
  # vtimesv:两个向量的乘法
  # vtimesi:向量乘实数
  # plot:迭代图的过程

  def __init__(self,eta,w0,b0,data):
    # eta是学习率（步长），w0是权值向量w的初值，b0是偏置b的初值
    self.eta = eta
    self.w = w0
    self.b = b0
    self.data = data
    self.markers = ['dr', 'ob', 'og', 'ok', '^r', '+r', 'sr', 'dr', '<r', 'pr']

  def isError(self,x):
    # 用来判断是否是误分类点，如果计算结果大于0，则表示被正确分类的，否则是误分类点
    result=(self.vtimesv(self.w , x[:-1]) + self.b)*x[-1]
    if result > 0:
      return False
    else:
      return True 


  def adjust(self,x):
    # 沿着梯度方向更新权值向量w和偏置b
    self.w = self.add(self.w, self.vtimesi(x[:-1], self.eta * x[-1]))
    self.b = self.b + self.eta * x[-1]
    return
	
  def train(self):
    #开始训练数据
    #获得数据个数
    flag=True
    count=0
    print('-'*30)
    print('initialing...')
    self.visualization(self.w,self.b,count)
    while flag:
      for i in range(len(self.data)):
        if self.isError(self.data[i]):
          count+=1
          self.adjust(self.data[i])
          print('No.{0} adjustment...'.format(count))
          print('Error data:'+str(self.data[i]))
          print('(w,b)=:'+str(self.w)+' '+str(self.b))
          flag = True
          break
        else:
          flag = False
      if flag==True:
          self.visualization(self.w,self.b,count)
    #返回训练好的模型参数
    return (self.w, self.b, count)

  def visualization(self, w, b, count):
    # 用于画图，包括分类的样本点和线段
    for i in range(len(self.data)):
        j = self.data[i][-1]+1
        plt.plot(self.data[i][0],self.data[i][1], self.markers[j])
    plt.ylim(-3,5)
    plt.xlim(-3,5)
    x = np.arange(-3,5,0.1)
    if w[1]!=0:
        y = -float(w[0])*x/float(w[1]) - float(b)/float(w[1])
        plt.title("No.{0} adjustment, {1}x1+{2}x2+{3}=0....".format(count,w[0],w[1],b))
        plt.plot(x,y,'b')
    elif w[1]==0 and w[0]!=0:
        # xline = -b/w[1]
        y = np.arange(-3,5,0.1)
        xline1 = []
        for i in range(len(x)):
            xline1.append(-float(b)/float(w[0]))
        plt.title("No.{0} adjustment, {1}x1+{2}x2+{3}=0....".format(count,w[0],w[1],b))
        plt.plot(xline1,y,'b')
    elif w[0]==0 and w[0]==0:
        y= np.arange(-3,5,0.1)
        xline2=[]
        for i in range(len(x)):
            xline2.append(b)
        plt.title("No.{0} adjustment, {1}x1+{2}x2+{3}=0....".format(count,w[0],w[1],b))
        plt.plot(xline2,y,'b')
    plt.show()


  @staticmethod
  def add(x,y):
    '''
    计算两个向量相加，返回一个新的向量
    '''
    if len(x)!=len(y):
      raise Exception
    else:
      return [x[t]+y[t] for t in range(len(x))]


  @staticmethod
  def vtimesv(x,y):
    # 计算两个向量相乘，返回一个实数
    if len(x)!=len(y):
      raise Exception
    else:
      z = [x[t]*y[t] for t in range(len(x))]
      return sum(z)
	
  @staticmethod
  def vtimesi(vector,n):
    # 返回列表
    return [vector[t]*n for t in range(len(vector))]


if __name__=='__main__':
    #书上的原始数据
    #data = [[3,3,1],[4,3,1],[1,1,-1]]
    #线性可分的测试数据
    #data = [[3,3,1],[4,3,1],[1,1,-1],[2,2,-1],[5,4,1],[1,3,-1]]
    #线性不可分，导致死循环
    #data = [[3,3,1],[4,3,1],[1,1,-1],[1,3,-1],[2,2,1],[3,1,-1]]
    # data1 = [[3,3,1],[4,3,1],[1,1,-1],[1,3,-1],[2,2,-1],[3,1,-1]]
    data2 = [[3,3,1],[4,3,1],[1,1,-1]]
    data2_= [[3,3,-1],[4,3,-1],[1,1,1]]
    data3 = [[0,0,-1],[0,1,-1],[1,0,-1],[1,1,1]]
    p = Perceptron(1,[1,1],0,data2)
    answer = p.train()
    print('-'*60)
    print('answer'+str(answer))
