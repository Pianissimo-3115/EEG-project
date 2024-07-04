import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
def apply_pca_to_5_dimensions(data):
    x = np.array(data)
    x = x.T
    x = StandardScaler().fit_transform(x)
    pca = PCA(n_components=6)
    principalComponents = pca.fit_transform(x)
    explained_variance_ratio = pca.explained_variance_ratio_
    return principalComponents, explained_variance_ratio
da=np.load("store.npy")
t=[i for i in range(2500)]
# plt.plot(t,da[0])
# plt.show()
for i in range(da.shape[0]):
    mean=np.average(da[i])
    sd=np.std(da[i])
    for j in range(da[i].shape[0]):
        da[i][j]-=mean
        da[i][j]/=sd
# plt.plot(t,da[0])
# plt.show()
pcadata,evr=apply_pca_to_5_dimensions(da)
print((pcadata.shape))
fig, axes = plt.subplots(nrows=1, ncols=5, figsize=(20, 4))
for i,ax in enumerate(axes):
    ax.scatter(da[0],da[i+1])
plt.tight_layout()
# plt.show()
for i in range(1):
    a=[]
    for j in range(2500):
        a.append(pcadata[j][i])

pcadata=pcadata.T
# print(pcadata[:][0],"\n\n\n\n\n", pcadata[:][1])
fig, axs = plt.subplots(nrows=2, ncols=3, figsize=(10,10))
arrays=[pcadata[1],pcadata[2],pcadata[3],pcadata[4]]
for i, a in enumerate(arrays):
    row = i // 2
    col = i % 2
    axs[row, col].scatter(pcadata[0], a)
    axs[row, col].set_title(f'Scatter a1 vs a{i+2}')
    axs[row, col].set_xlabel('a1')
    axs[row, col].set_xlim(-8, 8)
    axs[row, col].set_ylim(-8, 8)
    axs[row, col].set_ylabel(f'a{i+2}')
plt.tight_layout()
plt.show()