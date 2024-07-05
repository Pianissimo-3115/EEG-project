import numpy as np
a=np.load("testno.npy")
b=np.load("testyes.npy")
c=np.load("no1.npy")
d=np.load("yes1.npy")
total=np.hstack((a,b))
for i in range(len(total)-1):
    mmean=np.mean(total[i])
    sstd=np.std(total[i])
    a[i]-=mmean
    a[i]/=sstd
    b[i]-=mmean
    b[i]/=sstd
total=np.hstack((c,d))
for i in range(len(total)-1):
    mmean=np.mean(total[i])
    sstd=np.std(total[i])
    c[i]-=mmean
    c[i]/=sstd
    d[i]-=mmean
    d[i]/=sstd
import matplotlib.pyplot as plt
t=[i for i in range(len(a[0]))]
for i in range(len(a)):
    plt.plot(t,a[i],color="blue")
    plt.plot(t,b[i],color="red")
    plt.title(f"test_channel{i}")
    # plt.show()
    plt.plot(t,c[i],color="purple")
    plt.plot(t,d[i],color="black")
    plt.title(f"train_channel{i}")
    plt.show()