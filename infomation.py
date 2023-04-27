#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# @Author: Xiaotuan

from pprint import pprint
import psutil
import os
import sys
import platform
import subprocess
import re
import torch
import tensorflow as tf
import json

def runcmd(command):
    # 不显示输入内容 stdout=subprocess.PIPE, stderr=subprocess.PIPE
    # 编码方式 encoding="utf-8"
    ret = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if ret.returncode == 0:
        return ("success:", ret)
    else:
        return ("error:", ret)

# 显卡信息
result = str(runcmd(["nvdebugdump", "--list"])[1]).split(f"\\r\\n\\t")[2]
pattern = re.compile(r"Device name:\s+(.+?)(?:\s+\(\*PrimaryCard\))?$")
try:
    Card_Information = re.search(pattern, result).group(1)
except Exception as e:
    Card_Information = str(None)

# 操作系统的名称及版本号
OS_Version = platform.platform()

# CUDA 版本
result = str(runcmd(["nvcc", "-V"])[1])
pattern = r"V\d+\.\d+\.\d+"
try:
    CUDA_Version = re.search(pattern, result).group(0)
except Exception as e:
    CUDA_Version = str(None)

# Python 版本
Python_Version = platform.python_version()

# pytorch 的版本
try:
    Pytorch_Version = torch.__version__
except Exception as e:
    Pytorch_Version = str(None)

# pytorch 是否可用 CUDA
try:
    Pytorch_CUDA = str(torch.cuda.is_available())
except Exception as e:
    Pytorch_CUDA = str(None)

# tensorflow 的版本
try:
    Tensorflow_Version = tf.__version__
except Exception as e:
    Tensorflow_Version = str(None)

# tensorflow 是否可用 CUDA
try:
    Test = tf.config.list_physical_devices('GPU')
    if "device_type='GPU'" in str(Test): Tensorflow_CUDA = str(True)
    else: Tensorflow_CUDA = str(False)
except Exception as e:
    Tensorflow_CUDA = str(None)

# 计算机的处理器架构
PC_Framework = platform.machine()

# 计算机的处理器信息
PC_Information = platform.processor()

# CPU 的逻辑数量
CPU_logic = str(psutil.cpu_count())

# CPU 的物理核心数量
CPU_core = str(psutil.cpu_count(logical=False))

# CPU 使用率
CPU_List = psutil.cpu_percent(interval=0.5, percpu=True)
CPU_Use = []
for i in range(len(CPU_List)):
    tmp = "CPU_" + str(i+1) + ": " + str(CPU_List[i]) + "%    "
    CPU_Use.append(tmp)
    if i == len(CPU_List)//2-1: CPU_Use.append("\n")
CPU_Use = "".join(CPU_Use)

# 内存使用情况
Memory_List = psutil.virtual_memory()
Memory = ["总内存: %.2f G" % (Memory_List.total/1024/1024/1024)]
Memory.append("已使用内存: %.2f G" % (Memory_List.used/1024/1024/1024))
Memory.append("未使用内存: %.2f G" % (Memory_List.free/1024/1024/1024))
Memory.append("内存使用率: " + str(Memory_List.percent) + "%")
Memory = ",   ".join(Memory)

data = {
    "Card_Information": Card_Information,
    "OS_Version": OS_Version,
    "CUDA_Version": CUDA_Version,
    "Python_Version": Python_Version,
    "Pytorch_Version": Pytorch_Version,
    "Pytorch_CUDA": Pytorch_CUDA,
    "Tensorflow_Version": Tensorflow_Version,
    "Tensorflow_CUDA": Tensorflow_CUDA,
    "PC_Framework": PC_Framework,
    "PC_Information": PC_Information,
    "CPU_logic": CPU_logic,
    "CPU_logic": CPU_logic,
    "CPU_core": CPU_core,
    "CPU_Use": CPU_Use,
    "Memory": Memory
}

with open('./info.json', 'w+', encoding='utf-8') as f:
    # 写入 JSON 的缩进为 2 个空格
    talks_json = str(json.dumps(data, indent=2)).replace("'","\"")
    f.write(talks_json)

"""
PRINT = [
    Card_Information, OS_Version, CUDA_Version, Python_Version, Pytorch_Version, Pytorch_CUDA, Tensorflow_Version, Tensorflow_CUDA, PC_Framework,
    PC_Information, CPU_logic, CPU_core, CPU_Use, Memory
]

for item in PRINT:
    print(item)
"""