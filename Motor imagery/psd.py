import numpy as np
from scipy.signal import welch
import matplotlib.pyplot as plt
mea=[0]*6
for i in range(1,51):
    bb=np.load(f"Motor imagery\\Improved dataset\\b_{i}.npy")
    for w in range(6):
        for xx in bb[w]:
            mea[w]+=xx
        mea[w]/=len(bb[w])
for i in range(1,51):
    r=np.load(f"Motor imagery\\Improved dataset\\r_{i}.npy")
    l=np.load(f"Motor imagery\\Improved dataset\\l_{i}.npy")
    b=np.load(f"Motor imagery\\Improved dataset\\b_{i}.npy")
    for j in range(6):
        for w in range(len(r[j])):
            r[j][w]-=mea[j]
            l[j][w]-=mea[j]
    t=[w for w in range(r[0].shape[0])]
    # fig,axs=plt.subplots(1,6)
    fig,axs=plt.subplots(2,3)
    for j in range(6):
        fr,psdr=welch(r[j],500,nperseg=256)
        fl,psdl=welch(l[j],500,nperseg=256)
        fb,psdb=welch(b[j],500,nperseg=256)
        axs[j%2][j//2].plot(fr,psdr,color='red',label='right')
        axs[j%2][j//2].plot(fl,psdl,color='blue',label='left')
        axs[j%2][j//2].plot(fb,psdb,color='green',label='base')
        axs[j%2][j//2].set_ylim(0,100)
        axs[j%2][j//2].legend()
    plt.show()

    