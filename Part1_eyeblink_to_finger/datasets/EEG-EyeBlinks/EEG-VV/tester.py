import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal
import numpy as np
labels=['a','b','c','d','e','f','g','h','i','j','k','l']
df=pd.read_csv('S00V_data.csv',names=labels)
# print(df.head())
# time=list(df['a'][])
FP1=np.array((df['b'][0:250]))
FP2=np.array(df['c'])
time=[i for i in range(0,len(FP1))]
# FP1=(FP1[:15000])
F,PSD=signal.welch(FP1,fs=250,nperseg=2048)
l=['aa','bb']
df2=pd.read_csv("S00V_labels.csv",names=l)
liss=list(df2['aa'])
FP1=list(FP1)
for i in range(len(FP1)):
    FP1[i]/=3
for i in range(len(liss)):
    liss[i]*=250
# plt.scatter(liss,[10000]*len(liss),label='actual',color='red')
plt.plot(time,FP1,label='shown',color='blue')
plt.show()
plt.plot(F,PSD)
plt.show()






