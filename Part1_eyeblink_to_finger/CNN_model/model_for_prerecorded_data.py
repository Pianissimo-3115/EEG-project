import keras
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
from PIL import Image
# import time
check=[]
# x=time.perf_counter()
def plottoarr(x,y):
    plt.figure(figsize=(0.64, 0.48))
    plt.plot(x, y)
    plt.axis(False)
    plt.grid('off')
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image = Image.open(buf).convert('L')
    gray_array = np.array(image)
    # image.show()
    buf.close()
    plt.close()
    return gray_array
model=keras.models.load_model('cnn_model.h5')
a=list(np.load('store.npy'))
for i in range(len(a)):
    for j in range(len(a[0])):
        a[i][j]=-a[i][j]
for i in range(len(a)):
    t=[j for j in range(len(a[i]))]
    plt.plot(t,a[i])
    plt.show()
    b=plottoarr(t,a[i])
    b=np.reshape(b,(1,48,64))
    if(model.predict(b)[0][0]):
        print("Blink detected")
    # check.append(time.perf_counter()-x)
    # x=time.perf_counter()
# print(sum(check)/len(check))