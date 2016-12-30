import os
import sys
import numpy as np
root_path='/n/traffic_sign'
source_path1=os.path.join(root_path,'test_images')
source_path2=os.path.join(root_path,'train_images')
source_path3=os.path.join(root_path,'train.csv')
target_path1=os.path.join(root_path,'metadata','test_list.txt')
target_path2=os.path.join(root_path,'metadata','train_list.txt')
target_path3=os.path.join(root_path,'metadata','train_sign_bounds.txt')

fp=open(source_path3,'r')

if not os.path.exists(target_path1):
    fw1=open(target_path1,'w')
    for i in os.listdir(source_path1):
        tmp=os.path.join(source_path1,i)
        fw1.write(tmp+'\n')
    fw1.close()
if not os.path.exists(target_path2):
    fw2=open(target_path2,'w')
    for i in os.listdir(source_path2):
        tmp=os.path.join(source_path2,i)
        fw2.write(tmp+'\n')
    fw2.close()

if not os.path.exists(target_path3):
    fw3=open(target_path3,'w')
    index_info=fp.readline()
    for line_info in fp.readlines():
        tmp_list=line_info.strip().split(',')
        fw3.write(tmp_list[0]+'.jpg sign')
        for i in range(4):
            fw3.write(' '+tmp_list[i+1])
        fw3.write('\n')
    fw3.close()

'''
belows: generating faster-rcnn's training data-type file in /n/traffic_sign/metadata/train_set/
'''
trainlist_path=os.path.join(root_path,'metadata','train_set','ImageSets','Main','train.txt')
vallist_path=os.path.join(root_path,'metadata','train_set','ImageSets','Main','val.txt')
trainvallist_path=os.path.join(root_path,'metadata','train_set','ImageSets','Main','trainval.txt')
testlist_path=os.path.join(root_path,'metadata','train_set','ImageSets','Main','test.txt')

n_train=len(os.listdir(source_path2))
train_fp=open(trainlist_path,'w')
val_fp=open(vallist_path,'w')
trainval_fp=open(trainvallist_path,'w')
test_fp=open(testlist_path,'w')

times=0
perc_part1=1 #set 30% validation set and 70% training set
perc_part2=3
for i in os.listdir(source_path2):
    times+=1
    tmp=i.split('.')[0]
    if times%10>=perc_part1:
        trainval_fp.write(tmp+'\n')
        if times%10>=perc_part2:
            train_fp.write(tmp+'\n')
        else:
            val_fp.write(tmp+'\n')
    else:
        test_fp.write(tmp+'\n')

trainval_fp.close()
train_fp.close()
val_fp.close()
test_fp.close()