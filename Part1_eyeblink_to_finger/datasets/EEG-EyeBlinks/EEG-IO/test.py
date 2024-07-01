import matplotlib.pyplot as plt
import pandas as pd
labels=["Time (s)","FP1","FP2","Channel 3","Channel 4","Channel 5","Channel 6","Channel 7","Channel 8","Channel 9","Channel 10","Channel 11","Sampling Rate"]
df=pd.read_csv("D:\Study-Work\Study\EEG BCI project\EEG-EyeBlinks-public\EEG-EyeBlinks\EEG-IO\S00_data.csv", names=labels)
liss=df['FP1']
time=[i for i in range(len(liss))]
plt.plot(time,liss)
plt.show()
