# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 20:09:53 2023

@author: Administrator
"""

#! -*- coding: utf-8 -*-
# 测试代码可用性: 提取特征
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["KERAS_BACKEND"] = "torch"
os.environ["CUDA_VISIBLE_DEVICES"]="-1"

import numpy as np
from bert4keras3.backend import keras
#from bert4keras3.backend import ops
from bert4keras3.models import build_transformer_model
from bert4keras3.tokenizers import Tokenizer
from bert4keras3.snippets import to_array
#bert from 
base_path='models/chinese_GAU-alpha-char_L-24_H-768/'
config_path =base_path+ 'bert_config.json'
checkpoint_path = base_path+'bert_model.ckpt'
dict_path = base_path+'vocab.txt'

tokenizer = Tokenizer(dict_path, do_lower_case=True)  # 建立分词器
model = build_transformer_model(config_path, checkpoint_path,model='gau')  # 建立模型，加载权重

# 编码测试
token_ids, segment_ids = tokenizer.encode(u'语言模型')
token_ids, segment_ids = to_array([token_ids], [segment_ids])

print('\n ===== predicting =====\n')
print(model.predict([token_ids, segment_ids]))
model.predict([np.zeros([1024,32]),np.zeros([1024,32])],batch_size=8)
model.predict([np.zeros([1024,32]),np.zeros([1024,32])],batch_size=8,verbose=1)

"""
cpu is  i7-9750H CPU 
gpu is 16660ti

keras2.3.1 with tf2.2 ：
这里要乘8才和后面的等价
cpu
1024/1024 [==============================] - 36s 36ms/step
[[[ 8.43694583e-02 -1.82464731e+00 -1.73736602e-01 ...  2.17949137e-01
   -1.23585558e+00  5.60472012e-01]
  [ 1.65610969e-01  4.27814692e-01 -7.09107751e-03 ...  1.79192960e+00
   -1.47388828e+00  9.21145678e-02]
  [ 3.21300216e-02  1.16802305e-01 -3.47867310e-01 ...  2.66305923e+00
   -7.62626946e-01  1.79617792e-01]
  [ 5.30323863e-01  8.27933013e-01 -2.09565043e-01 ...  2.70129180e+00
   -1.70141995e+00 -4.62279111e-01]
  [ 1.11098802e+00  2.50530988e-01 -1.20544562e-03 ...  3.05589271e+00
   -9.48840380e-01 -1.16868329e+00]
  [ 3.26632172e-01 -1.05267394e+00  1.10736869e-01 ...  1.04140675e+00
   -1.63025188e+00  7.14173079e-01]]]
1024/1024 [==============================] - 3s 3ms/step


keras3 torch backend
cpu
 128/128 ━━━━━━━━━━━━━━━━━━━━ 30s 359ms/step
[[[ 8.43690783e-02 -1.82464767e+00 -1.73736081e-01 ...  2.17950568e-01
   -1.23585534e+00  5.60471833e-01]
  [ 1.65611252e-01  4.27814305e-01 -7.09151709e-03 ...  1.79192996e+00
   -1.47388911e+00  9.21137035e-02]
  [ 3.21297087e-02  1.16802014e-01 -3.47867429e-01 ...  2.66305876e+00
   -7.62626946e-01  1.79616228e-01]
  [ 5.30323923e-01  8.27932477e-01 -2.09564567e-01 ...  2.70129371e+00
   -1.70142019e+00 -4.62279409e-01]
  [ 1.11098838e+00  2.50531554e-01 -1.20343606e-03 ...  3.05589414e+00
   -9.48841333e-01 -1.16868329e+00]
  [ 3.26631963e-01 -1.05267489e+00  1.10735424e-01 ...  1.04140878e+00
   -1.63025296e+00  7.14173734e-01]]]

keras3 jax backend
因为在cpu上,XLA可能有副作用 0  
cpu 
128/128 ━━━━━━━━━━━━━━━━━━━━ 50s 352ms/step
[[[ 8.4370218e-02 -1.8246456e+00 -1.7373715e-01 ...  2.1795137e-01
   -1.2358553e+00  5.6047183e-01]
  [ 1.6561073e-01  4.2781356e-01 -7.0914533e-03 ...  1.7919306e+00
   -1.4738873e+00  9.2114463e-02]
  [ 3.2128207e-02  1.1680270e-01 -3.4786788e-01 ...  2.6630602e+00
   -7.6262707e-01  1.7961684e-01]
  [ 5.3032303e-01  8.2793194e-01 -2.0956475e-01 ...  2.7012937e+00
   -1.7014201e+00 -4.6227869e-01]
  [ 1.1109877e+00  2.5053164e-01 -1.2037499e-03 ...  3.0558927e+00
   -9.4884133e-01 -1.1686826e+00]
  [ 3.2663262e-01 -1.0526737e+00  1.1073510e-01 ...  1.0414089e+00
   -1.6302530e+00  7.1417361e-01]]]


keras3 tf backend
cpu
128/128 ━━━━━━━━━━━━━━━━━━━━ 27s 178ms/step
[[[ 8.4370218e-02 -1.8246456e+00 -1.7373715e-01 ...  2.1795137e-01
   -1.2358553e+00  5.6047183e-01]
  [ 1.6561073e-01  4.2781356e-01 -7.0914533e-03 ...  1.7919306e+00
   -1.4738873e+00  9.2114463e-02]
  [ 3.2128207e-02  1.1680270e-01 -3.4786788e-01 ...  2.6630602e+00
   -7.6262707e-01  1.7961684e-01]
  [ 5.3032303e-01  8.2793194e-01 -2.0956475e-01 ...  2.7012937e+00
   -1.7014201e+00 -4.6227869e-01]
  [ 1.1109877e+00  2.5053164e-01 -1.2037499e-03 ...  3.0558927e+00
   -9.4884133e-01 -1.1686826e+00]
  [ 3.2663262e-01 -1.0526737e+00  1.1073510e-01 ...  1.0414089e+00
   -1.6302530e+00  7.1417361e-01]]]
"""

