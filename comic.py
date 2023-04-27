#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# @Author: Xiaotuan

import os
import sys
sys.path.append(os.path.join(os.path.abspath('.'), 'AnimeGANv2'))
from AnimeGANv2 import test

test.test(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])