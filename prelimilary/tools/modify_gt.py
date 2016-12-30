import sys
import os

file_path='../train_ground.txt'
fp=open(file_path,'r')
lines=fp.readlines()

target_path='../cropped_train_ground.txt'
fw=open(target_path,'w')

def get_rl(list_line):
    side1=0 #side1:left; side2:right
    side2=0
    xmin=int(list_line[0])
    xmax=int(list_line[2])
    if xmax<=780:
        side1=1
    if xmin>=780:
        side2=1
    if xmin<500 and xmax>500:
        if (float(xmax)-500)/(float(xmax-xmin))>0.7:
            side1=1
            side2=1
        else:
            side1=1
    elif xmin<780 and xmax>780:
        if (780-float(xmin))/(float(xmax-xmin))>0.7:
            side1=1
            side2=1
        else:
            side2=1
    return side1,side2

for line in lines:
    line_list=line.strip().split(' ')
    image_name=line_list[0].split('.')[0]
    label=line_list[1]
    side1,side2=get_rl(line_list[2:])
    tmp_name=image_name
    if side1==1:
        image_name=tmp_name+'a.jpg'
        tmp_str=image_name
        line_list[4]=line_list[4] if int(line_list[4])<780 else 780
        for i in range(5):
            tmp_str+=' '+str(line_list[i+1])
        fw.write(tmp_str+'\n')
    if side2==1:
        image_name=tmp_name+'b.jpg'
        tmp_str=image_name
        xmin=int(line_list[2])-500
        xmin=xmin if xmin>=0 else 0
        xmax=int(line_list[4])-500
        xmax=xmax if xmax>=0 else 0
        line_list[2]=str(xmin)
        line_list[4]=str(xmax)
        if int(line_list[5])>530:
            line_list[5]=str(530)
        for i in range(5):
            tmp_str+=' '+line_list[i+1]
        fw.write(tmp_str+'\n')

