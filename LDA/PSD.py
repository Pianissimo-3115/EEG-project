import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch
store=np.load("store.npy")
print(store.shape)
print(store[-1])
f=[[]]*(store.shape[0]-1)
psd=[[]]*(store.shape[0]-1)
t=[i for i in range(store[0].size)]
for i in range(store.shape[0]-1):
    fig,axs=plt.subplots(2,1)
    axs[0].plot(t,store[i])
    f[i],psd[i]=welch(store[i],500,nperseg=256)
    axs[1].plot(f[i],psd[i])
    plt.tight_layout()
    plt.show()
f=np.array(f)
psd=np.array(psd)
np.save("f.npy",f)
np.save("psd.npy",psd)
np.save("labels.npy",store[-1])