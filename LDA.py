import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

def compute_lda(eeg_data, labels):
    t = eeg_data.shape[1]
    reshaped_data = eeg_data.T
    lda = LinearDiscriminantAnalysis()
    lda_transformed = lda.fit_transform(reshaped_data, labels)
    return lda_transformed, lda
