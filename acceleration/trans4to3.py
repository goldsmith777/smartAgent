# -*- coding: utf8 -*-

################################################
#                                              #
#修改类标号                                      #
#                                              #
################################################

from numpy import *
def trans_lable()
    f = open('D:\GT\Code\User_context\CenceMeLiteLog1_en_std.txt','r')
    a = []
    for line in f.readlines():
    line_float = map(float,line[1:-2].split(','))
    if line_float[-1]==0:
        line_float[-1] = 5
    a.append(line_float)
    f.close()
    f = open('D:\GT\Code\User_context\CenceMeLiteLog1_class3_en_std.txt','w')
    for item in a:
        f.writelines(str(item) + '\n')
    f.close()

if __name__ =='__main__':
    trans_lable()

