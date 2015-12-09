#coding:utf-8
__author__ = 'GaoTian'

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

class animationPlot：
    def __init__(self):
        fig = plt.figure()
        # 1. 多子图画法
        # ax1 = fig.add_subplot(2,1,1,xlim=(0, 2), ylim=(-4, 4))
        # ax2 = fig.add_subplot(2,1,2,xlim=(0, 2), ylim=(-4, 4))
        # line, = ax1.plot([], [], lw=2)
        # line2, = ax2.plot([], [], lw=2)
        # 2. 单子图
        # ylim(-2,5)
        # xlim(-2,5)
        # 画点
        # plot(data1,data2, markers)
        # 画线
        # plot([data1,data2],[data3,data4])
        # x = np.arange(-2,5,0.1)
        # y = 10x+20
        # ylim(-2,5)
        # xlim(-2,5)


    def init():
        line.set_data([], [])
        line2.set_data([], [])
        return line,line2

    # animation function.  this is called sequentially
    def animate(i):
        x = np.linspace(0, 2, 100)
        y = np.sin(2 * np.pi * (x - 0.01 * i))
        line.set_data(x, y)
        # x2 = np.linspace(0, 2, 100)
        # y2 = np.cos(2 * np.pi * (x2 - 0.01 * i))* np.sin(2 * np.pi * (x - 0.01 * i))
        # line2.set_data(x2, y2)
        return line,line2

if __name__ == '__main__':
    # 建立子图和空白线
    ap = animationPlot()
    anim1 = animation.FuncAnimation(ap.fig, ap.animate, init_func=ap.init, frames=50, interval=10)
    plt.show()