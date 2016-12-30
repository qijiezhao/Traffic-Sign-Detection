文件目录说明：
（所有脚本均面向过程编写，运行时需要修改一下路径）
tools:使用过的工具
|-- compare_valset.py: 对比在验证集上的测试结果和真实标记的效果图。
|-- compute_map.py：计算map，用于在验证集上验证算法的效果
|-- compute_simi.py：计算训练集图像的相似性，以此对图像进行近一步分析
|-- ensemble_last.py：最后一步的后融合，用于将recall（召回率）比较高的次模型的测试结果补至主模型的后面
|-- fuse+rerank.py：将交通标志的检测结果和车辆行人自行车的检测结果做一个融合和重排序，主要是把车辆行人自行车覆盖的交通标志的排序往后放
|-- fusion.py：将切开的图合在一起（主要是合结果文件的坐标，和处理重合区域的车标）
|-- fusion_4parts.py： 如上，将切成4块的合在一起
|-- generate_datalist.py：对训练集和测试集的图像遍历并产生list，同时做好voc的数据接口文件的Sets部分
|-- images_similarity.py：提取所有图像的深度特征，以用于计算图像的相似性
|-- modify_gt.py：根据切图方案，修改ground truth文件
|-- visualize_images.py：对图像的标记进行可视化，在图中将检测到的交通标志（用不同颜色）圈出。

py-frcnn: python版接口的faster-rcnn
|-- caffe-fast-rcnn：dependency中的caffe部分，需要下载，链接为：（百度网盘）http://pan.baidu.com/s/1pLrVMaf，手动解压到此目录
|-- code
	|-- compute_map.py: 计算map，用于在验证集上验证算法的效果
	|-- compute_fuseMAP.py：同上，为了方便分开计算，修改为切图后的和合图后的分别测试mAP
	|-- generate_newtestfile.txt：生成测试列表
|-- data: py-frcnn原有
	|-- *：基本和源代码不变，在训练前需要把训练数据转化成VOC的数据格式并放在此目录下
|-- experiments：实验的训练执行脚本，日志和修改配置文件等都会放在下面
	|-- *：基本和源代码不变
|-- lib：frcnn的data, rpn，roi等layer的库文件
	|-- fast_rcnn：为框架中的fast_rcnn部分，我们修改过config.py里的一些信息，包括SCALES,MAX_SIZE,RPN_NMS,RPN_MIN_SIZE
	|-- rpn：主要修改了rpn的anchors的设置，包括size和ratio分别增大为7和5。
	|-- *：其他部分除开debug基本未修改
|-- tools: 执行一些命令的脚本
	|--demo*.py 实验中的测试环节都用这个脚本进行，所以对其进行过一些输入输出的修改

models: 训练过程中需要的模型文件和最后生成的结果文件，因大小限制，需要下载，内附链接
|-- download_url.txt 内附下载链接和相应模型的简单介绍

ultimate：初赛最后提交的结果文件
|-- ensemble_last3.txt：txt接口的结果文件
|-- PKU_MI19.csv：csv接口的结果文件，格式和最后的提交格式一致

