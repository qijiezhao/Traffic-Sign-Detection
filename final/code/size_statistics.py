import os
import numpy as np
import matplotlib.pyplot as plt

max_box_size = 200

threshold = 0.6
ground_truth = r"data\train.csv"
filenames = (ground_truth, r"data\resnet50-min16-AB-scale1400.txt", r"data\rfcn20w_20w_test_fusion.txt", r"data\rfcn20w_finetune_test_fusion.txt")
separator = (",", ",", " ", " ")

plt.title(threshold)
for i, filename in enumerate(filenames):
    bins = [0 for j in range(max_box_size)]
    file = open(filename, "r")
    lines = file.readlines()
    for l in lines:
        fields = l.split(separator[i])
        if filename == ground_truth or float(fields[5]) >= threshold:
            w = float(fields[3]) - float(fields[1])
            h = float(fields[4]) - float(fields[2])
            size = int(np.sqrt(w * h))
            if size < max_box_size:
                bins[size] += 1
    distribution = [0.0 for j in range(max_box_size)]
    for k in range(max_box_size):
        distribution[k] = bins[k] / sum(bins) * 100
    plt.plot(distribution)
    file.close()
plt.legend(filenames)
plt.ylabel("percentage")
plt.xlabel("sqrt(w * h)")
plt.show()
