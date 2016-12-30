main_file = "submit.csv"
other_file = "resnet50-min16-AB-scale1400.csv"

threshold = 0.8


def calculate_iou(box1, box2):
    W = min(box1[2], box2[2]) - max(box1[0], box2[0])
    H = min(box1[3], box2[3]) - max(box1[1], box2[1])
    if W <= 0 or H <= 0:
        return 0
    else:
        SB = (box2[3] - box2[1]) * (box2[2] - box2[0])
        SA = (box1[3] - box1[1]) * (box1[2] - box1[0])
        cross = W * H
        return cross / (SA + SB - cross)

boxes = {}
with open(main_file, "r") as f:
    lines = f.readlines()
    for line in lines:
        fields = line.strip().split(",")
        key = fields[0]
        if key not in boxes:
            boxes[key] = []
        box = [float(i) for i in fields[1:5]]
        boxes[key].append(box)

with open(other_file, "r") as f_other:
    with open(main_file, "a") as f_main:
        lines = f_other.readlines()
        for line in lines:
            fields = line.strip().split(",")
            key = fields[0]
            assert(key in boxes)
            flag = True
            for box in boxes[key]:
                if calculate_iou(box, [float(i) for i in fields[1:5]]) >= 0.8:
                    flag = False
                    break
            if flag:
                f_main.write("%s,%s,%s,%s,%s,%f\n" % (fields[0], fields[1], fields[2], fields[3], fields[4], float(fields[5]) / 100 - 1))

