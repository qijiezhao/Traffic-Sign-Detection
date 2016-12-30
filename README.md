CCF-datafountain大数据与计算智能系列赛之UISEE-自动驾驶场景下的交通标志检测比赛

PKU_MI队

初赛a,b榜No.1

复赛a,b榜No.3,4

决赛二等奖

# 代码运行说明

除Faster R-CNN及R-FCN之外，所有代码均使用Python与C#编写，代码在运行前可能需要更改操作路径或重新编译。

## 准备数据集

1. 运行`final\code\crop_image.py`将原图切割为两个半图，运行`prelimilary\tools\modify_gt.py`转化ground truth。

2. 运行`final\code\generate_xml.py`生成Pascal VOC格式的xml文件。

3. 选择模型：`final\external`目录下的`py-faster-rcnn`，`py-faster-rcnn-VGG16`，`py-R-FCN`分别为ResNet Faster R-CNN，VGG16 Faster R-CNN和ResNet R-FCN模型的根目录。

   将对应的在ImageNet上预训练的模型放入`data\imagenet_models`下。在`data\VOCdevkit\VOC2007`（对于Faster R-CNN模型）或`data\VOCdevkit\VOC0712`下按Pascal VOC格式建立训练集。

   `\Annotations` - xml文件

   `\ImageSets\Main` - `trainval.txt`和`test.txt`分别为训练集和验证集的图像编号列表。

   `\JPEGImages` - JPG格式的图像文件

## 开始训练

设根目录为`final\external\py-faster-rcnn`，`final\external\py-faster-rcnn-VGG16`，`final\external\py-R-FCN`。

运行`experiments\scripts`下的`{faster_rcnn, rfcn}_end2end.sh`脚本，命令行选项为`<script-name> GPU-ID NET-NAME pascal_voc`，网络即开始训练。

训练日志和模型（每迭代10000次输出一次快照）分别输出在`experiments\logs`及`\output`下

## 测试

运行`tools\demo*.py`，将对指定图像文件进行测试，输出保存在txt文件中。

## 后处理与评估

`final\code\calculate_map.py` - 在训练集上计算mAP并绘制P-R曲线

`final\code\size_statistics.py` - 统计结果中box的大小分布

`final\code\filter.py` - 滤除车辆检测的结果，减少False Positive

`final\code\convert_format.py` - 将结果转化为csv格式
