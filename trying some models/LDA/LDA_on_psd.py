import numpy as np
import matplotlib.pyplot as plt
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from PSD import psd
# labels=np.load("labels.npy")
def compute_lda(psd_data, labels):
    t = psd_data.shape[1]
    reshaped_data = psd_data.T
    lda = LinearDiscriminantAnalysis()
    lda_transformed = lda.fit_transform(reshaped_data, labels)
    return lda_transformed, lda
yes=np.load("Right dominant wrist movement(binary classification)\\testing\\yes(recorded while moving).npy")
no=np.load("Right dominant wrist movement(binary classification)\\testing\\no(recorded while moving).npy")
for j in range(yes.shape[0]-1):
    f,ps=psd(yes[j])
    for i in range(f.size):
        if f[i]>5 and ps[i]>ps[i-1]:
            start=i
            break
    maxx=0
    maxxind=0
    for i in range(i,25):
        if(ps[i]>maxx):
            maxx=ps[i]
            maxxind=i
    print(maxx,f[maxxind])