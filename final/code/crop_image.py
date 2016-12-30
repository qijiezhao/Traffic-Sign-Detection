import os
from PIL import Image

inputDir = r"D:\ccf_traffic_sign_2\test_images"
outputDir = r"E:\xbw\traffic_sign2\cropped_test_images"

region_l = [0, 0, 780, 530]
region_r = [500, 0, 1280, 530]

for f in os.listdir(inputDir):
    path = os.path.join(inputDir, f)
    image = Image.open(path)
    cropped_image_l = image.crop(region_l)
    cropped_image_l.save(os.path.join(outputDir, f[0: -4] + "a.jpg"), quality=100)
    cropped_image_r = image.crop(region_r)
    cropped_image_r.save(os.path.join(outputDir, f[0: -4] + "b.jpg"), quality=100)
