import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

def compute_lda(eeg_data, labels):
    t = eeg_data.shape[1]
    reshaped_data = eeg_data.T
    lda = LinearDiscriminantAnalysis()
    lda_transformed = lda.fit_transform(reshaped_data, labels)
    return lda_transformed, lda
ds1=np.load("yes1.npy")
ds2=np.load("yes2.npy")
ds3=np.load("yes3.npy")
# ds4=np.load("yes4.npy")
ds5=np.load("no1.npy")
ds6=np.load("no2.npy")
ds7=np.load("no3.npy")
# ds8=np.load("no4.npy")
# by mistake no4 was overwritten so removed it and to prevent imbalance, also removed yes4
a=(ds1,ds2,ds3,ds5,ds6,ds7)

dataset=np.hstack(a)
for i in range(len(dataset)-1):
    mean=np.mean(dataset[i])
    std=np.std(dataset[i])
    dataset[i]-=mean
    dataset[i]/=std
import matplotlib.pyplot as plt
t=[i for i in range(len(dataset[0]))]
# plt.plot(t,dataset[0])
# plt.show()
# train1,test1,test2,train2=np.hsplit(dataset,4)
# train=np.hstack((train1,train2))
# test=np.hstack((test1,test2))
lda_transformed,lda=compute_lda(dataset[:6],dataset[6])
testyes=np.load("YES(testnoise).npy")
testno=np.load("NO(testnoise).npy")
testingyes=lda.predict((testyes[:6].T))
testingno=lda.predict((testno[:6].T))
ans1=0
ans2=0
for i in range(len(testingno)):
    if(testingno[i]==testno[6][i]):
        ans1+=1
    if(testingyes[i]==testyes[6][i]):
        ans2+=1
print(100*ans1/len(testingno))
print(100*ans2/len(testingyes))

