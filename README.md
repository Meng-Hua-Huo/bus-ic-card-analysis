# 吴巨-25311061-第三次人工智能编程作业
任务要求生成的图片存放在 figures ，而不是 images ！
## 1. 任务拆解与 AI 协作策略

在编写代码之前，我将这个项目分解成 7 个步骤

step 1: 数据预处理

step 2: 时间分布分析

step 3: 线路站点分析

step 4: 高峰小时系数(PHF)计算

step 5: 文件批量导出

step 6: 服务绩效热力图

step 7: README编写

### step 0: 创建第三次作业仓库与基础环境配置

首先我把终端直接定位到该项目的根目录
![](images/img1.png)
然后在该目录下执行作业的初始化命令
![](images/img2.png)
接下来创建四个目录，分别用于存放
数据文件、代码文件、三张图像输出、线路驾驶员信息
![](images/img03.png)
将任务要求使用的四个第三方库下载
![](images/img4.png)

question: 如何在 pycharm 中配置 gitignore

answer: 
![](images/img6.png)
![](images/img7.png)
最后将代码推送到 GitHub 
![](images/img5.png)

### step 1-6

question:
在每一步我会分别给出 prompt ，让 AI 生成大致代码
然后根据运行结果进行人工审查以及修改

（具体迭代和 debug 步骤详见后面部分）

step 1
![](images/img8.png)
![](images/img9.png)
![](images/img10.png)

step 2
![](images/img11.png)
![](images/img12.png)

把生成的 png 放入 figures 中（后面步骤同理）

![](images/img13.png)

step 3
![](images/img14.png)
![](images/img15.png)
![](images/img16.png)

step 4
![](images/img17.png)
![](images/img18.png)

step 5
![](images/img19.png)
![](images/img20.png)

把生成的 20个 txt 文件放入 output 中

step 6
![](images/img21.png)
![](images/img22.png)

最后我根据生成的热力图，通过观察该热力图的大致特征，
得出线路与上车点维度不均而司机与车辆维度分布均匀的结论

全部步骤完成之后，将 main.py 封装到 scr 中

## 2. 核心 prompt 迭代记录

在 step 5 中，虽然生成了目录，但是里面没有包含 txt 文件

question: 生成的代码运行后生成相应的 txt 文件不符合规范，
要求按照给出的格式重新生成相应代码
![](images/img23.png)
answer: （给出正确代码）

运行后格式如图
![](images/img24.png)

## 3. Debug 记录

在 step 0 中，把终端直接定位到该项目的根目录时出现报错
![](images/img25.png)
question: 如图的报错时什么原因，如何修改

answer: 
![](images/img26.png)
于是我按照 AI 的提示进行修改并成功运行
![](images/img27.png)
推送 step 0 时由于终端所在目录不是 Git 仓库的根目录，
git 找不到 .git 隐藏文件夹而报错
![](images/img28.png)
question: 为什么会出现如图的报错时，给出修改方案

answer: （给出以下解决步骤）
![](images/img29.png)
在 step 1 将代码推送到 GitHub 时，出现报错
![](images/img30.png)
![](images/img31.png)
question: 为什么会出现如图的报错时，给出修改方案

answer:![](images/img32.png)
通过上述 AI 回答以及询问同学的帮助，我尝试通过虚拟环境隔离原理，
创建虚拟环境并在其中安装numpy

question: 如何通过将numpy放置在虚拟环境中使得与python不冲突

answer: ![](images/img33.png)
![](images/img34.png)
![](images/img35.png)

配置之后依旧出现报错
![](images/img36.png)
question: 之前用将numpy置于虚拟环境中为什么还会这样报错

answer:![](images/img37.png)
于是我退出虚拟环境，检查解释器配置，发现忘记选择 anaconda ，
重新配置之后成功解决报错

然后我试图重新推送 step 1 ，又出现了新的报错
![](images/img38.png)
![](images/img39.png)
由最后一行可以看出路径问题，于是我不询问 AI 而直接进行修改
![](images/img40.png)
运行之后又出现了新的报错
![](images/img41.png)
![](images/img42.png)
可以看出是数据格式与代码不一致，于是我依旧不询问 AI 而直接修改分隔符
![](images/img43.png)

在 step 2 进行推送时，依旧发生路径错误
![](images/img44.png)
于是我依旧不询问 AI 而直接修改
![](images/img45.png)

后续均无发现 bug ，于是 debug 成功

### 4. 人工代码审查

以下为 PHF 计算的核心代码（含人工审查注释部分）
![](images/img46.png)