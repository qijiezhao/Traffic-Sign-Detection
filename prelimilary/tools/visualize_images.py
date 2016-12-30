import os
import sys
import cv2
import matplotlib.pyplot as plt
import scipy.io as sio
import numpy as np


fp=open('../result/submission_now.txt','r')
root_path='../test_images'
lines=fp.readlines()
len_signs=len(lines)

def rename(num):
    len_lack=len(str(num))
    tmp_name=''
    for i in range(6-len_lack):
        tmp_name+='0'
    tmp_name+=str(num)+'.jpg'
    return tmp_name

def vis_detections(image_name,im,class_name,dets):
    if len(dets)==0:
        return
    im=im[:,:,(2,1,0)]
    fig,ax=plt.subplots(figsize=(12,12))
    ax.imshow(im,aspect='equal')
    for i in range(len(dets)):
        bbox=dets[i][:4]
        score=dets[i][-1]

        ax.add_patch(
            plt.Rectangle((bbox[0],bbox[1]),
                          bbox[2]-bbox[0],
                          bbox[3]-bbox[1],fill=False,
                          edgecolor='red',linewidth=1)
            )
        ax.text(bbox[0],bbox[1]-2,
                '{:.3f}'.format(score),
                bbox=dict(facecolor='blue',alpha=0.2),
                fontsize=10,color='white')
    ax.set_title(image_name+'  '+str(len(dets)),
                  fontsize=14)
    plt.axis('off')
    #plt.tight_layout()
    plt.draw()
    image_name=image_name.split('.')[0]+'.jpg'
    #plt.savefig('../submit5_testimages/'+image_name)
    plt.show()
    plt.close()

image_dics={}
for i in range(len_signs):
    line_list=lines[i].strip().split(' ')
    #get image path
    #tmp_name=rename(line_list[0])
    tmp_name=line_list[0]
    dets=[]
    if float(line_list[5])>50:
        for i in range(5):
            dets.append(float(line_list[i+1]))
        if not image_dics.has_key(tmp_name):
            image_dics[tmp_name]=[]
            image_dics[tmp_name].append(dets)
        else:
            image_dics[tmp_name].append(dets)
ss=0
for item in image_dics:
    image_name=item.split('.')[0]+'.png'
    image_path=os.path.join(root_path,image_name)
    #im=128 * np.ones((300,500,3),dtype=np.uint8)
    im=cv2.imread(image_path)
    sign_list=image_dics[item]

    len_signs=len(sign_list)
    class_name=['sign' for i in range(len_signs)]

    vis_detections(image_name,im,class_name,sign_list)
