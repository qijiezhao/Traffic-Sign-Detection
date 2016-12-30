import numpy as np
import os
import sys

#file_source='E:/myd/traffic_sign/scratch/zqj/resnet101_rfcn_crop_test_nms045.txt'
file_source='../result/resnet50_rfcn_crop_test_nms045_min10_2b1.txt'
lines=open(file_source,'r').readlines()
#file_target='E:/myd/traffic_sign/scratch/zqj/fusion_resnet101_rfcn_crop_test_nms045_dot01.txt'
file_target='../result/fusion_resnet50_rfcn_crop_test_nms045_min10_2b1.txt'
fw=open(file_target,'w')
def get_side(subimage_name):
    tmp_side=0 if subimage_name[6]=='a' else 1 #left:0; right:1
    image_name=subimage_name[0:6]+subimage_name[7:]
    return image_name,tmp_side

def get_Is_overlap(box1_info,box2_info):
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
        Is_overlap=min(s/S1,s/S2)
    else:
        Is_overlap=0
    return Is_overlap

image_dic={}
for line in lines:
    line_list=line.strip().split(' ')
    subimage_name=line_list[0]
    box_info=line_list[1:6]
    #score_info=line_list[5]
    box_info[4]=float(box_info[4])
    image_name,side=get_side(subimage_name)
    if side==1:
        box_info[0]=str(float(box_info[0])+500)
        box_info[2]=str(float(box_info[2])+500)

    if not image_dic.has_key(image_name):
        boxes_list=[]
        boxes_list.append(box_info)
        image_dic[image_name]=boxes_list
    else:
        Is_overlap=0
        for each_info in image_dic[image_name]:
            Is_overlap=get_Is_overlap(each_info,box_info)
            if Is_overlap>0.65:
                break
        if Is_overlap>0.65:
            continue
        image_dic[image_name].append(box_info)

for item in image_dic:
    boxes_list=image_dic[item]
    boxes_list.sort(lambda x,y:cmp(x[-1],y[-1]),reverse=True)


for item in image_dic:
    image_name=item
    for box_info in image_dic[item]:
        str_tmp=image_name
        if float(box_info[4])>0:
            for j in range(5):
                if j==4:
                    box_info[j]=str(100*float(box_info[j]))
                else:
                    box_info[j]=int(float(box_info[j]))
                str_tmp+=' '+str(box_info[j])
            fw.write(str_tmp+'\n')