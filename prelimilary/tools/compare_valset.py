import os
import sys
import cv2
import matplotlib.pyplot as plt
import scipy.io as sio
import numpy as np
import matplotlib

fp=open('../result/fusion_trainsample_crop2_dot01_nms45_rawimage_9w_ov65.txt','r')
fc=open('../train_ground.txt','r')
root_path='../train_images/'
lines=fp.readlines()
lines_fc=fc.readlines()
len_fc=len(lines_fc)
len_signs=len(lines)

def vis_detections(image_name,im,class_name,dets1,dets2):
    if len(dets1)==0:
        return
    im=im[:,:,(2,1,0)]
    fig,ax=plt.subplots(figsize=(12,12))
    ax.imshow(im,aspect='equal')
    for i in range(len(dets1)):
        bbox=dets1[i][:4]
        score=dets1[i][-1]

        if score>0.7:
            ax.add_patch(
                plt.Rectangle((bbox[0],bbox[1]),
                              bbox[2]-bbox[0],
                              bbox[3]-bbox[1],fill=False,
                              edgecolor='red',linewidth=2)
                )
            ax.text(bbox[0],bbox[1]-2,
                    '{:.3f}'.format(score),
                    bbox=dict(facecolor='blue',alpha=0.1),
                    fontsize=10,color='white')
        else:
            ax.add_patch(
                plt.Rectangle((bbox[0],bbox[1]),
                              bbox[2]-bbox[0],
                              bbox[3]-bbox[1],fill=False,
                              edgecolor='yellow',linewidth=2)
                )
            ax.text(bbox[0],bbox[1]-2,
                    '{:.3f}'.format(score),
                    bbox=dict(facecolor='blue',alpha=0.1),
                    fontsize=10,color='white')
    # ax.set_title(('{} detections with '
    #               'p({} | box)>={:.1f}').format(class_name,class_name,0.8),
    #               fontsize=14)
    for i in range(len(dets2)):
        bbox=dets2[i][:4]
        #score=dets1[i][-1]
        ax.add_patch(
            plt.Rectangle((bbox[0],bbox[1]),
                          bbox[2]-bbox[0],
                          bbox[3]-bbox[1],fill=False,
                          edgecolor='green',linewidth=2))
    plt.axis('off')
    #plt.tight_layout()
    plt.draw()
    #plt.show()
    image_name=image_name.split('.')[0]+'.jpg'
    plt.savefig('../submit2_trainsample/'+image_name)
    plt.close()
image_dics={}
for i in range(len_signs):
    line_list=lines[i].strip().split(' ')
    #get image path
    tmp_name=line_list[0]
    dets=[]
    if float(line_list[5])>0.8:
        for i in range(5):
            dets.append(float(line_list[i+1]))
        if not image_dics.has_key(tmp_name):
            image_dics[tmp_name]=[]
            image_dics[tmp_name].append(dets)
        else:
            image_dics[tmp_name].append(dets)

image_dics2={}
for i in range(len_fc):
    line_list=lines_fc[i].strip().split(' ')
    #get image path
    tmp_name=line_list[0]
    dets=[]
    for i in range(4):
        dets.append(float(line_list[i+2]))
    if not image_dics2.has_key(tmp_name):
        image_dics2[tmp_name]=[]
        image_dics2[tmp_name].append(dets)
    else:
        image_dics2[tmp_name].append(dets)

for item in image_dics:
    image_name=item.split('.')[0]+'.png'
    image_path=os.path.join(root_path,image_name)
    #im=128 * np.ones((300,500,3),dtype=np.uint8)
    im=cv2.imread(image_path)
    sign_list1=image_dics[item]
    sign_list2=image_dics2[item]
    len_signs=len(sign_list1)
    class_name=['sign' for i in range(len_signs)]
    vis_detections(image_name,im,class_name,sign_list1,sign_list2)