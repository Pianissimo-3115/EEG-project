import numpy as np
from scipy.signal import welch
import matplotlib.pyplot as plt
for i in range(26,51):
    r=np.load(f"Motor imagery\\Dataset(L,R,baseline)\\r_{i}.npy")
    l=np.load(f"Motor imagery\\Dataset(L,R,baseline)\\l_{i}.npy")
    b=np.load(f"Motor imagery\\Dataset(L,R,baseline)\\b_{int(np.ceil(i/2))}.npy")
    t=[w for w in range(r[0].shape[0])]
    fig,axs=plt.subplots(1,6)
    for j in range(6):
        fr,psdr=welch(r[j],500,nperseg=256)
        axs[j].plot(fr,psdr)
    plt.tight_layout()
    # plt.show()
    fig,axs=plt.subplots(1,6)
    for j in range(6):
        fl,psdl=welch(l[j],500,nperseg=256)
        axs[j].plot(fl,psdl)
    plt.tight_layout()
    # plt.show()
    fig,axs=plt.subplots(1,6)
    for j in range(6):
        fb,psdb=welch(b[j],500,nperseg=256)
        axs[j].plot(fb,psdb)
    plt.tight_layout()
    plt.show()

    