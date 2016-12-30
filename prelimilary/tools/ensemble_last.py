import os
import sys
import numpy as np

file_centre='../result/resnet50_finetune_test_fusion.txt'
file_ensemble='../result/submission_065.csv'
file_output='../result/ensemble_test_new.txt'
# file_centre='fusion_val_crop2_dot01_nms45_ov65.txt'
# file_ensemble='result7w_dot45_fuse.txt'
# file_output='ensemble_last_val16.txt'

fw=open(file_output,'w')
fpc=open(file_centre,'r')
fpe=open(file_ensemble,'r')

lines_c=fpc.readlines()
lines_e=fpe.readlines()
def rename(num):
    len_lack=len(str(num))
    tmp_name=''
    for i in range(6-len_lack):
        tmp_name+='0'
    tmp_name+=str(num)+'.jpg'
    return tmp_name
def get_overlap(box1_info,box2_info):
    B1xmin=float(box1_info[0])
    B1ymin=float(box1_info[1])
    B1xmax=float(box1_info[2])
    B1ymax=float(box1_info[3])
    S1=(B1xmax-B1xmin)*(B1ymax-B1ymin)

    B2xmin=float(box2_info[0])
    B2ymin=float(box2_info[1])
    B2xmax=float(box2_info[2])
    B2ymax=float(box2_info[3])
    S2=(B2xmax-B2xmin)*(B2ymax-B2ymin)

    rect_xmin=max(B1xmin,B2xmin)
    rect_ymin=max(B1ymin,B2ymin)
    rect_xmax=min(B1xmax,B2xmax)
    rect_ymax=min(B1ymax,B2ymax)

    Is_overlap=1
    if rect_xmin<rect_xmax and rect_ymin<rect_ymax:
        s=(rect_xmax-rect_xmin)*(rect_ymax-rect_ymin)
        Is_overlap=s/(S1+S2-s)
    else:
        Is_overlap=0
    return Is_overlap

image_dic={}

for i in range(len(lines_c)):
    line_list=lines_c[i].strip().split(' ')
    image_name=line_list[0]
    box_list=line_list[1:]
    box_list[-1]=str(float(box_list[-1])*100)
    if not image_dic.has_key(image_name):
        boxes_list=[]
        boxes_list.append(box_list)
        image_dic[image_name]=boxes_list
    else:
        image_dic[image_name].append(box_list)
num0=0
for i in range(len(lines_e)):
    if i==0:
        continue
    num0+=1
    if num0%1000==0:
        print num0
    line_list=lines_e[i].strip().split(',')
    image_name=rename(line_list[0])
    box_info=line_list[1:]
    if not image_dic.has_key(image_name):
        print 'error',image_name
    centre_list=image_dic[image_name]
    Is_overlap=0
    for j in range(len(centre_list)):
        Is_overlap=get_overlap(box_info[:4],centre_list[j][:4])#get IOU
        #flag=0
        if Is_overlap>0.6:
            # if flag==0:
            #     centre_list[j][-1]=str(float(centre_list[j][-1])+0.01)
            #     flag=1
            break
        # print Is_overlap
    if Is_overlap<0.6:
        box_info[-1]=str(float(box_info[-1])-100)
        image_dic[image_name].append(box_info)
        #print image_name,box_info
for i in image_dic:
    list_box=image_dic[i]
    for j in list_box:
        tmp_str=i
        for s in range(5):
            tmp_str+=' '+j[s]
        fw.write(tmp_str+'\n')