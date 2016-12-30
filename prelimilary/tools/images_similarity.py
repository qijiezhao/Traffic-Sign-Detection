import os
import sys
import numpy as np

caffe_root='/n/zqj/caffe/'
sys.path.insert(0,caffe_root+'python')
import caffe

model_deploy='/n/traffic_sign2/code/alexnet/deploy_alexnet.prototxt'
model_file='/n/traffic_sign2/code/alexnet/alexnet.caffemodel'
mean_file='/n/traffic_sign2/code/alexnet/ilsvrc_2012_mean.npy'

caffe.set_mode_gpu()
caffe.set_device(0)
net=caffe.Net(model_deploy,model_file,caffe.TEST)
transformer=caffe.io.Transformer({'data':net.blobs['data'].data.shape})
transformer.set_transpose('data',(2,0,1))
transformer.set_mean('data',np.load(mean_file).mean(1).mean(1))
net.blobs['data'].reshape(50,3,227,227)

target_file='/n/traffic_sign2/train_images_jpg/'
for file in os.listdir(target_file):
    full_name=os.path.join(target_file,file)

    transformed_image=transformer.preprocess('data',caffe.io.load_image(full_name))
    net.blobs['data'].data[...]=transformed_image
    print file
    out=net.forward()
    result=net.blobs['prob'].data
    np.save(os.path.join('/n/traffic_sign2/code/simi/',file.split('.')[0]),result)