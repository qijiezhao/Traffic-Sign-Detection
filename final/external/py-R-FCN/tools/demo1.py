#!/usr/bin/env python

# --------------------------------------------------------
# Faster R-CNN
# Copyright (c) 2015 Microsoft
# Licensed under The MIT License [see LICENSE for details]
# Written by Ross Girshick
# --------------------------------------------------------

"""
Demo script showing detections in sample images.

See README.md for installation instructions before running.
"""

import _init_paths
from fast_rcnn.config import cfg
from fast_rcnn.test import im_detect
from fast_rcnn.nms_wrapper import nms
from utils.timer import Timer
import matplotlib.pyplot as plt
import numpy as np
import scipy.io as sio
import caffe, os, sys, cv2
import argparse
from IPython import embed

CLASSES = ('__background__',
           'sign')

NETS = {'vgg16': ('VGG16',
                  'VGG16_faster_rcnn_final.caffemodel'),
        'zf': ('ZF',
                  'ZF_faster_rcnn_final.caffemodel'),
	'resnet101': ('RESNET101',
		'RESNET101_faster_rcnn_final.caffemodel')}

def demo(net, image_name):
    """Detect object classes in an image using pre-computed object proposals."""

    # Load the demo image
    #test_image_path='/n/traffic_sign/test_images'
    #im_file = os.path.join(test_image_path, image_name)
    im = cv2.imread(image_name)
    # Detect all object classes and regress object bounds
    timer = Timer()
    timer.tic()
    scores, boxes = im_detect(net, im)
    timer.toc()
    print ('Detection took {:.3f}s for '
           '{:d} object proposals').format(timer.total_time, boxes.shape[0])

    # Visualize detections for each class
    CONF_THRESH = 0.01
    NMS_THRESH = 0.45
    for cls_ind, cls in enumerate(CLASSES[1:]):
        cls_ind += 1 # because we skipped background
        cls_boxes = boxes[:, 4*cls_ind:4*(cls_ind + 1)]
        cls_scores = scores[:, cls_ind]
        dets = np.hstack((cls_boxes,
                          cls_scores[:, np.newaxis])).astype(np.float32)
        keep = nms(dets, NMS_THRESH)
        dets = dets[keep, :]
        #vis_detections(im, cls, dets, thresh=CONF_THRESH)
        inds=np.where(dets[:,-1]>=CONF_THRESH)[0]
        for i in inds:
            tmp_str=image_name.split('/')[-1]
            for j in range(5):
                tmp=' '+str(dets[i,j])
                tmp_str+=tmp
            fw_tmp.write(tmp_str+'\n')
 

def parse_args():
    """Parse input arguments."""
    parser = argparse.ArgumentParser(description='Faster R-CNN demo')
    parser.add_argument('--gpu', dest='gpu_id', help='GPU device id to use [0]',
                        default=0, type=int)
    parser.add_argument('--cpu', dest='cpu_mode',
                        help='Use CPU mode (overrides --gpu)',
                        action='store_true')
    parser.add_argument('--net', dest='demo_net', help='Network to use [vgg16]',
                        choices=NETS.keys(), default='vgg16')

    args = parser.parse_args()

    return args

if __name__ == '__main__':
    cfg.TEST.HAS_RPN = True  # Use RPN for proposals
    
    args = parse_args()
    
    prototxt = '/scratch/xbw/traffic_sign2/py-R-FCN/models/pascal_voc/ResNet-50/rfcn_end2end/test_agnostic.prototxt'
    caffemodel = '/scratch/xbw/traffic_sign2/py-R-FCN/output/rfcn_end2end_ohem/voc_0712_trainval/resnet50_rfcn_ohem_iter_100000.caffemodel'
    
    if not os.path.isfile(caffemodel):
        raise IOError(('{:s} not found.\nDid you run ./data/script/'
                    'fetch_faster_rcnn_models.sh?').format(caffemodel))
    
    if args.cpu_mode:
        caffe.set_mode_cpu()
    else:
        caffe.set_mode_gpu()
        caffe.set_device(args.gpu_id)
        cfg.GPU_ID = args.gpu_id
    net = caffe.Net(prototxt, caffemodel, caffe.TEST)
    print '\n\nLoaded network {:s}'.format(caffemodel)
    
    fw_tmp=open('/scratch/xbw/resnet50_finetune_test.txt','w')
    fp_tmp=open('/n/traffic_sign2/metadata/cropped_test_list.txt','r')
    lines=fp_tmp.readlines()
    im_names=[]
    for line in lines:
        if len(line)>3:
            all_str=line.strip()
            im_names.append(all_str)
    for im_name in im_names:
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print 'Demo for data/demo/{}'.format(im_name)
        print im_name
        demo(net, im_name)
    fw_tmp.close()
    fp_tmp.close()
    