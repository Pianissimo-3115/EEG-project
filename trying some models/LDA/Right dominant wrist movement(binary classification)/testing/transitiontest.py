import numpy as np
import LDA
a=np.load("Right dominant wrist movement(binary classification)\\testing\\transition.npy")
import matplotlib.pyplot as plt
t=[i for i in range(a[0].size)]
for i in range(6):
    mean=np.mean(a[i])
    std=np.std(a[i])
    a[i]-=mean
    a[i]/=std
    plt.plot(t,a[i])
    plt.show()

print(a.shape)
outputs=LDA.lda.predict(a.T)
for i in outputs:
    print(i)

