import numpy as np
import matplotlib.pyplot as plt
mental=np.load("thinking\\YES(mental).npy")
physical=np.load("thinking\\YES(physical).npy")
no=np.load("thinking\\NO.npy")
t=[i for i in range(len(mental[0]))]
for i in range(len(mental)-1):
    plt.plot(t,mental[i],label="mental")
    plt.plot(t,physical[i],label="physical")
    plt.plot(t,no[i],label="no")
    plt.title(f"channel {i}")
    plt.legend()
    plt.show()