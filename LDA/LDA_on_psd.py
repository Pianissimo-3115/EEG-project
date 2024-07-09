import numpy as np
import matplotlib.pyplot as plt
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
f,psd=np.load("f.npy"),np.load("psd.npy")
labels=np.load("labels.npy")
def compute_lda(eeg_data, labels):
    t = eeg_data.shape[1]
    reshaped_data = eeg_data.T
    lda = LinearDiscriminantAnalysis()
    lda_transformed = lda.fit_transform(reshaped_data, labels)
    return lda_transformed, lda
lda_transformed,lda=compute_lda(f,labels)