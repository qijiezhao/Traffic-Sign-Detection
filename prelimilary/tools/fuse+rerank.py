import os
import numpy as np
import math
file1='../result/ensemble_test_new.txt'
file2='../result/detection_others.txt'

with open(file1,'r') as fp1:
    lines1=fp1.readlines()

with open(file2,'r') as fp2:
    lines2=fp2.readlines()
def rename(str_name):
    len_str=len(str_name)
    lack_len=6-len_str
    tmp_str=''
    for i in range(lack_len):
        tmp_str+='0'
    tmp_str+=str_name+'.jpg'
    return tmp_str

def Get_Over(box_center,box_info):
    xmin_c=float(box_center[0])+5
    ymin_c=float(box_center[1])
    xmax_c=float(box_center[2])
    ymax_c=float(box_center[3])
    Sc=(xmax_c-xmin_c)*(ymax_c-ymin_c)

    ymin_c=ymin_c+0.3*(ymax_c-ymin_c)

    xmin_i=float(box_info[0])
    ymin_i=float(box_info[1])
    xmax_i=float(box_info[2])
    ymax_i=float(box_info[3])
    Si=(ymax_i-ymin_i)*(xmax_i-xmin_i)

    rect_xmin=max(xmin_i,xmin_c)
    rect_ymin=max(ymin_c,ymin_i)
    rect_xmax=min(xmax_i,xmax_c)
    rect_ymax=min(ymax_c,ymax_i)


    if rect_xmin<rect_xmax and rect_ymin<rect_ymax:
        s=(rect_xmax-rect_xmin)*(rect_ymax-rect_ymin)
        Is_Over=max(s/Sc,s/Si)
    else:
        Is_Over=0
    return Is_Over

def Is_corner(box_center):
    if float(box_center[0])<10 or float(box_center[2])>1270:
        return True
    else:
        return False

def get_sqrtarea(box_center):
    xmin1=float(box_center[0])
    ymin1=float(box_center[1])
    xmax1=float(box_center[2])
    ymax1=float(box_center[3])
    sqrtarea=math.sqrt((xmax1-xmin1)*(ymax1-ymin1))
    return sqrtarea
image_dic={}
for line in lines1:
    line_list=line.strip().split(' ')
    image_name=line_list[0]
    box_info=line_list[1:]
    boxes_info=[]
    if not image_dic.has_key(image_name):
        image_dic[image_name]=boxes_info
        image_dic[image_name].append(box_info)
    else:
        image_dic[image_name].append(box_info)
num0=0
for line in lines2:
    line_list=line.strip().split(' ')
    image_name=line_list[0].split('.')[0]+'.jpg'
    if not image_dic.has_key(image_name):
        continue
    box_center=line_list[2:]
    boxes_info=image_dic[image_name]
    new_boxes=[]
    for box_info in boxes_info:
        Is_Over=Get_Over(box_center,box_info[:-1])
        if Is_Over==1 and Is_corner(box_center)==False and get_sqrtarea(box_center)<300:
            num0+=1
            box_info[-1]=str(float(box_info[-1])-200)
            new_boxes.append(box_info)
        else:
            new_boxes.append(box_info)
    image_dic[image_name]=new_boxes
print num0
file3='../result/submission_now.txt'
fw=open(file3,'w')
for item in image_dic:
    boxes_info=image_dic[item]
    image_name=item
    for box_info in boxes_info:
        tmp_str=image_name
        for i in range(5):
            tmp_str+=' '+box_info[i]
        fw.write(tmp_str+'\n')

fw.close()




