import os
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement

ground_truth = r"data\train.csv"
separator = ","
output_path = "Annotations"

width = 1280
height = 720


def write_xml(id, boxes):
    if len(boxes) != 0:
        output_filename = os.path.join(output_path, id + ".xml")
        annotation = Element("annotation")
        _folder = SubElement(annotation, "folder")
        _folder.text = "VOC2007"
        _filename = SubElement(annotation, "filename")
        _filename.text = id + ".jpg"
        _source = SubElement(annotation, "source")
        __database = SubElement(_source, "database")
        __database.text = "The VOC2007 Database"
        __annotation = SubElement(_source, "annotation")
        __annotation.text = "The Traffic Sign Database"
        __image = SubElement(_source, "image")
        __image.text = "ccf-dataset"
        __flickrid_1 = SubElement(_source, "flickrid")
        __flickrid_1.text = "null"
        _owner = SubElement(annotation, "owner")
        __flickrid_2 = SubElement(_owner, "flickrid")
        __flickrid_2.text = "null"
        __name_1 = SubElement(_owner, "name")
        __name_1.text = "traffic sign"
        _size = SubElement(annotation, "size")
        __width = SubElement(_size, "width")
        __width.text = str(width)
        __height = SubElement(_size, "height")
        __height.text = str(height)
        __height = SubElement(_size, "depth")
        __height.text = "3"
        _segmented = SubElement(annotation, "segmented")
        _segmented.text = "0"
        for box in boxes:
            _object = SubElement(annotation, "object")
            __name_2 = SubElement(_object, "name")
            __name_2.text = "sign"
            __pose = SubElement(_object, "pose")
            __pose.text = "null"
            __truncated = SubElement(_object, "truncated")
            __truncated.text = "0"
            __difficult = SubElement(_object, "difficult")
            __difficult.text = "0"
            __bndbox = SubElement(_object, "bndbox")
            ___xmin = SubElement(__bndbox, "xmin")
            ___xmin.text = box[0]
            ___ymin = SubElement(__bndbox, "ymin")
            ___ymin.text = box[1]
            ___xmax = SubElement(__bndbox, "xmax")
            ___xmax.text = box[2]
            ___ymax = SubElement(__bndbox, "ymax")
            ___ymax.text = box[3]
        tree = ElementTree.ElementTree(annotation)
        tree.write(output_filename)

id = None
boxes = []
with open(ground_truth, "r") as file:
    lines = file.readlines()
for line in lines:
    fields = line.split(separator)
    current_id = fields[0][:6]
    if current_id != id:
        if id is not None:
            write_xml(id, boxes)
            boxes = []
        id = current_id
    boxes.append([fields[i].strip() for i in range(1, 5)])
write_xml(id, boxes)