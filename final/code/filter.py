detection_file = (r"submit.csv",)
filter_mask = r"detection_others.txt"
output_file = (r"submit2.txt",)

threshold = 0.8


def calculate_iou(box1, box2):
    W = min(box1[2], box2[2]) - max(box1[0], box2[0])
    H = min(box1[3], box2[3]) - max(box1[1], box2[1])
    if W <= 0 or H <= 0:
        return 0
    else:
        SB = (box2[3] - box2[1]) * (box2[2] - box2[0])
        cross = W * H
        return cross / SB


filter = {}
with open(filter_mask, "r") as file:
    lines = file.readlines()
    for line in lines:
        fields = line.strip().split(" ")
        if fields[1] in ["bus", "car"]:
            key = fields[0][:6]
            if key not in filter:
                filter[key] = []
            box = [float(i) for i in fields[2:6]]
            box[1] = box[3] - (box[3] - box[1]) * 2 / 3
            filter[key].append(box)

for i, input_file in enumerate(detection_file):
    with open(input_file, "r") as in_file:
        with open(output_file[i], "w") as out_file:
            lines = in_file.readlines()
            for line in lines:
                fields = line.strip().split(",")
                key = fields[0][:6]
                test_box = [float(i) for i in fields[1:5]]
                flag = True
                if key in filter:
                    for box in filter[key]:
                        if calculate_iou(box, test_box) > threshold:
                            flag = False
                            break
                confidence = float(fields[5]) if flag else float(fields[5]) * 0.5
                out_file.write("%s %s %s %s %s %f\n" % (fields[0], fields[1], fields[2], fields[3], fields[4], confidence))
