# PyComic

<div align=center><img src="https://s1.ax1x.com/2023/04/27/p9QYxmj.png"></div>

## APP 介绍

基于人工智能的图片动漫化，组成：GUI 界面（PySide6 实现电脑端 APP）+ 内容主体（Python 实现 AI 功能），GUI 模板是 [PyDracula](https://github.com/Wanderson-Magalhaes/Modern_GUI_PyDracula_PySide6_or_PyQt6)，AI 模型是 [AnimeGANv2](https://github.com/TachibanaYoshino/AnimeGANv2) ，详细笔记请看[这篇博客](https://www.cnblogs.com/CourserLi/p/17156077.html)，也算是抽空学习的一个小项目，PySide6 开发相比其他桌面端 APP 开发，优势在于比较容易结合 Python 脚本文件

主要功能：

1. 选择合适模型，图片动漫化
2. 系统监控，查看电脑信息（如显卡信息、CUDA 版本等）

#### 部分软件截图

<div align=center><img src="https://s1.ax1x.com/2023/04/27/p9Qt9kq.png"></div>

<div align=center><img src="https://s1.ax1x.com/2023/04/27/p9QtFpT.png"></div>

<div align=center><img src="https://s1.ax1x.com/2023/04/27/p9Qtk1U.png"></div>

## 运行项目

1. 需要调整 `comic.bat` 中的下面几个参数

```cmd
start cmd /k "cd/d D:\conda地址&&call D:\conda地址\Scripts\activate.bat&&call conda activate 环境 &&call d:&&call cd D:\地址\PyComic&&call python D:\地址\PyComic\comic.py %1 %2 %3 %4"
```

2. 如果没有 `torch` 或者 `tensorflow` 库，需要注释 `infomation.py` 中的如下引用头

```python
# import torch
# import tensorflow as tf
```

3. **先运行 `infomation.py` 再运行 `main.py`**
