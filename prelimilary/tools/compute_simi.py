import os
import sys
import numpy as np
import scipy.io as sio

source_file='simi/'
vec_dic={}
distance_dic={}
image_names=[]
for file in os.listdir(source_file):
    full_name=os.path.join(source_file,file)
    image_id=file.split('.')[0]
    image_names.append(image_id)
    vec_dic[image_id]=np.load(full_name)
    distance_dic[image_id]={}
print 'read data done!'
distance_all=[]
count=0
flag=np.zeros([10000,10000],dtype=np.int8)
for i in image_names:
    count+=1
    if count%50==0:
        print count
    for j in image_names:
        if i==j:
            distance_dic[i][j]=1
            continue
        if flag[int(i)][int(j)]==1 or flag[int(j)][int(i)]==1:
            distance_dic[i][j]=distance_dic[j][i]
            continue
        flag[int(i)][int(j)]=1
        distance_tmp=np.sum(np.abs(vec_dic[i]-vec_dic[j]))
        distance_dic[i][j]=distance_tmp
        distance_all.append(distance_tmp)

distance_dict=sorted(distance_dic.iteritems(),key=lambda d:d[0])
distance_matrix=[]
for i in distance_dict:
    tmp_dic=i[1]
    tmp_dict=sorted(tmp_dic.iteritems(),key=lambda d:d[0])
    tmp_vec=[]
    for j in tmp_dict:
        tmp_vec.append(j[1])
    distance_matrix.append(tmp_vec)
save_array=np.array(distance_matrix)
sio.savemat('distance_L1.mat',{'dist':save_array})
distance_all.sort()
result_file='distance_result.txt'
fw=open(result_file,'w')
for i in distance_all:
    fw.write(str(i)+'\n')
fw.close()