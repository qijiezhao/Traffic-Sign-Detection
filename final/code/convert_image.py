import os
from PIL import Image

inputDir = r"D:\ccf_traffic_sign_2\test_images"
outputDir = r"E:\xbw\traffic_sign2\test_images_jpg"

for f in os.listdir(inputDir):
    path = os.path.join(inputDir, f)
    image = Image.open(path)
    image.save(os.path.join(outputDir, f[0: -4] + ".jpg"), quality=100)
