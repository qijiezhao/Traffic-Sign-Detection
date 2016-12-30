#__author__ = 'zqj'
import os
file_source='/scratch/zqj/py-faster-rcnn-master2/data/VOCdevkit2007/VOC2007/ImageSets/Main/test.txt'
lines=open(file_source,'r').readlines()

image_list={}
for line in lines:
    tmp_name=line[:6]
    if not image_list.has_key(tmp_name):
        image_list[tmp_name]=1

file_target='/scratch/zqj/py-faster-rcnn-master2/data/new_test_crop2.txt'
fw=open(file_target,'w')

for item in image_list:
    fw.write(item+'\n')

fw.close()