import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch
def psd(x):
    f,psd=welch(x,500,nperseg=256)
    f=np.array(f)
    psd=np.array(psd)
    return f,psd
yes=np.load("Right dominant wrist movement(binary classification)\\testing\\yes(recorded while moving).npy")
no=np.load("Right dominant wrist movement(binary classification)\\testing\\no(recorded while moving).npy")
# print(yes.shape)
for w in range(yes.shape[0]-1):
    t=[i for i in range(yes[0].size)]
    # fig,axs=plt.subplots(2,1)
    # axs[0].plot(t,yes[w])
    # axs[1].plot(t,no[w])
    # plt.tight_layout()
    # plt.show()
    # plt.close()
    f1,ps1=psd(yes[w])
    f2,ps2=psd(no[w])
    for i in range(f1.size):
        if f1[i]>5 and ps1[i]>ps1[i-1]:
            start=i
            break
    maxx=0
    maxxind=0
    for x in range(i,25):
        if(ps1[x]>maxx):
            maxx=ps1[x]
            maxxind=x
    print(maxx,f1[maxxind])
    fig,axs=plt.subplots(2,1)
    axs[0].plot(f1,ps1)
    axs[0].set_xlim(left=0,right=60)
    axs[1].plot(f2,ps2)
    axs[1].set_xlim(left=0,right=60)
    plt.tight_layout()
    plt.show()