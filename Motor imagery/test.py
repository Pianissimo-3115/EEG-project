import numpy as np
a=np.load("Motor imagery\\Dataset(L,R,baseline)\\l_1.npy")
from scipy.signal import welch
f,psd=welch(a[0],500,nperseg=256)
import matplotlib.pyplot as plt
plt.plot(f,psd)
plt.show()
b=np.load("Motor imagery\\Dataset(L,R,baseline)\\l_12.npy")
print(b.shape)