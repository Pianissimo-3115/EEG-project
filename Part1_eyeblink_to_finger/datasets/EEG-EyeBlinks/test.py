import keras
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import signal
labels=['Time','FP1','FP2','Channel 3','Channel 4','Channel 5','Channel 6','Channel 7','Channel 8','Channel 9','Channel 10','Channel 11','Sampling Rate']
data=pd.read_csv("D:\Study-Work\Study\EEG BCI project\EEG-EyeBlinks-public\EEG-EyeBlinks\EEG-IO\S07_data.csv",names=labels)
outputs=pd.read_csv("D:\Study-Work\Study\EEG BCI project\EEG-EyeBlinks-public\EEG-EyeBlinks\EEG-IO\S07_labels.csv")
# print(type(data['FP1'][0]))
arra=np.array(data["FP1"],dtype=float)
for i in range(len(arra)):
    arra[i] = float(arra[i])
# print(type(arra[0]))
leng=len(arra)
print(arra)
F,PSD=signal.welch(arra,64,nperseg=leng)
print(PSD.shape)
F=list(F)
PSD=list(PSD)
for i in range(len(F)):
    F[i] = float(F[i])
for i in range(len(PSD)):
    PSD[i] = float(PSD[i]) 
print(F,PSD,type(F),type(PSD))
plt.plot(F,PSD)
plt.show()