import numpy as np
import scipy
import os
import sys
import xml.etree.ElementTree as ET


def parse_rec(filename):
    """ Parse a PASCAL VOC xml file """
    tree = ET.parse(filename)
    objects = []
    for obj in tree.findall('object'):
        obj_struct = {}
        obj_struct['name'] = obj.find('name').text
        obj_struct['pose'] = obj.find('pose').text
        obj_struct['truncated'] = int(obj.find('truncated').text)
        obj_struct['difficult'] = int(obj.find('difficult').text)
        bbox = obj.find('bndbox')
        obj_struct['bbox'] = [int(bbox.find('xmin').text),
                              int(bbox.find('ymin').text),
                              int(bbox.find('xmax').text),
                              int(bbox.find('ymax').text)]
        objects.append(obj_struct)

    return objects

def voc_ap(rec, prec):
    mrec = np.concatenate(([0.], rec, [1.]))
    mpre = np.concatenate(([0.], prec, [0.]))

    # compute the precision envelope
    for i in range(mpre.size - 1, 0, -1):
        mpre[i - 1] = np.maximum(mpre[i - 1], mpre[i])

    # to calculate area under PR curve, look for points
    # where X axis (recall) changes value
    i = np.where(mrec[1:] != mrec[:-1])[0]

    # and sum (\Delta recall) * prec
    ap = np.sum((mrec[i + 1] - mrec[i]) * mpre[i + 1])
    return ap

def voc_eval(detpath,annopath,imagesetfile,classname,ovthresh=0.5):
    with open(imagesetfile,'r') as f:
        lines=f.readlines()
    imagenames=[x.strip() for x in lines]

    class_recs={}
    npos=0

    recs={}
    for i,imagename in enumerate(imagenames):
        recs[imagename]=parse_rec(annopath.format(imagename))
        if i%100==0:
            print 'reading annotation for {:d}/{:d}'.format(
                i+1,len(imagenames)
            )

    for imagename in imagenames:
        R=[obj for obj in recs[imagename] if obj['name']==classname]
        bbox=np.array([x['bbox'] for x in R])
        difficult=np.array([x['difficult'] for x in R]).astype(np.bool)
        det=[False]*len(R)
        npos=npos+sum(~difficult)
        class_recs[imagename]={'bbox':bbox,'difficult':difficult,'det':det}

    detfile=detpath.format(classname)
    with open(detfile,'r') as f:
        lines=f.readlines()

    splitlines=[x.strip().split(' ') for x in lines]
    image_ids=[x[0].split('.')[0] for x in splitlines]
    confidence=np.array([float(x[5]) for x in splitlines])
    BB=np.array([[float(z) for z in x[1:5]] for x in splitlines])

    sorted_ind=np.argsort(-confidence)
    sorted_scores=np.sort(-confidence)
    BB=BB[sorted_ind,:]
    image_ids=[image_ids[x] for x in sorted_ind]

    nd=len(image_ids)
    tp=np.zeros(nd)
    fp=np.zeros(nd)
    for d in range(nd):
        R=class_recs[image_ids[d]]
        bb=BB[d,:].astype(float)
        ovmax=-np.inf
        BBGT=R['bbox'].astype(float)

        if BBGT.size>0:
            ixmin=np.maximum(BBGT[:,0],bb[0])
            iymin=np.maximum(BBGT[:,1],bb[1])
            ixmax=np.minimum(BBGT[:,2],bb[2])
            iymax=np.minimum(BBGT[:,3],bb[3])
            iw=np.maximum(ixmax - ixmin + 1., 0.)
            ih = np.maximum(iymax - iymin + 1., 0.)
            inters = iw * ih

            # union
            uni = ((bb[2] - bb[0] + 1.) * (bb[3] - bb[1] + 1.) +
                   (BBGT[:, 2] - BBGT[:, 0] + 1.) *
                   (BBGT[:, 3] - BBGT[:, 1] + 1.) - inters)

            overlaps = inters / uni
            ovmax = np.max(overlaps)
            jmax = np.argmax(overlaps)

        if ovmax > ovthresh:
            if not R['difficult'][jmax]:
                if not R['det'][jmax]:
                    tp[d] = 1.
                    R['det'][jmax] = 1
                else:
                    fp[d] = 1.
        else:
            fp[d] = 1.

    # compute precision recall
    fp = np.cumsum(fp)
    tp = np.cumsum(tp)
    rec = tp / float(npos)
    # avoid divide by zero in case the first detection matches a difficult
    # ground truth
    prec = tp / np.maximum(tp + fp, np.finfo(np.float64).eps)
    ap = voc_ap(rec, prec)

    return rec, prec, ap


if __name__=='__main__':

    cls='sign'

    annopath=os.path.join('/n/traffic_sign2/py-faster-rcnn/data/VOCdevkit2007/VOC2007_crop2/','Annotations','{:s}.xml')#annotation paths
    imagesetfile=os.path.join('/n/traffic_sign2/py-faster-rcnn/data/VOCdevkit2007/VOC2007_crop2/ImageSets/Main','test.txt')#including the all detection files
    filename='/n/traffic_sign2/py-faster-rcnn/output/valset/val_crop2_dot01_nms45_rawimage_9w.txt' #the detection results file
    rec,prec,ap=voc_eval(filename,annopath,imagesetfile,cls,ovthresh=0.35)

    print 'mAP is : '+str(ap)
    print prec[-1]
    print rec[-1]
    print filename