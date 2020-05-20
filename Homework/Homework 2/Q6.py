# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 22:12:09 2020

@author: qinzhen
"""

from Q4 import *
from Q5 import *

#### Q6
File1 = "cfg_vert.counts"
Count_x = Count(File1)
f1 = "parse_train_vert.dat"
o1 = "parse_train_vert_proc.dat"
Replace(f1, o1, Count_x)

#python count_cfg_freq.py parse_train_vert_proc.dat > cfg_vert_proc.counts

File2 = "cfg_vert_proc.counts"
f2 = "parse_dev.dat"
o2 = "parse_dev_vert_result.dat"
Count_xyy, Count_xy, Count_x, Count_y = Generate_count(File2)
q_xyy, q_xy = Generate_mle(Count_xyy, Count_xy, Count_x, Count_y)
Generate(f2, o2, Count_xyy, Count_xy, Count_x, Count_y, q_xyy, q_xy)