import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
labels=['a','b','c','d','e','f','g','h','i','j','k','l']
df=pd.read_csv('D:\Study-Work\Study\EEG BCI project\EEG-EyeBlinks-public\EEG-EyeBlinks\EEG-VV\S00V_data.csv',names=labels)
FP1=np.array((df['b']))
FP2=np.array(df['c'])
l=['aa','bb']
df2=pd.read_csv("D:\Study-Work\Study\EEG BCI project\EEG-EyeBlinks-public\EEG-EyeBlinks\EEG-VV\S00V_labels.csv",names=l)
df2=df2.drop(df2[df2['bb']==2].index)
df2=df2.drop(df2[df2['bb']==1].index)
liss=list(df2['aa'])
FP1=list(FP1)
for i in range(len(liss)):
    liss[i]=int(liss[i]*250)
print(df2.head())
time=np.array([i for i in range(len(FP1))])

# checker=[int(time[i] in liss) for i in range(len(time))]
print(len(liss))