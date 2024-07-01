from socket import *
from struct import *
import time
import numpy as np
store=[]
class Marker:
    def _init_(self):
        self.position = 0
        self.points = 0
        self.channel = -1
        self.type = ""
        self.description = ""

def RecvData(socket, requestedSize):
    returnStream = b''
    while len(returnStream) < requestedSize:
        databytes = socket.recv(requestedSize - len(returnStream))
        if databytes == b'':
            raise RuntimeError("connection broken")
        returnStream += databytes
    return returnStream

def SplitString(raw):
    stringlist = []
    s = b""
    for i in range(len(raw)):
        if raw[i] != 0:
            s += bytes([raw[i]])
        else:
            stringlist.append(s.decode('utf-8'))
            s = b""
    return stringlist

def GetProperties(rawdata):
    (channelCount, samplingInterval) = unpack('<Ld', rawdata[:12])
    resolutions = []
    for c in range(channelCount):
        index = 12 + c * 8
        restuple = unpack('<d', rawdata[index:index+8])
        resolutions.append(restuple[0])
    channelNames = SplitString(rawdata[12 + 8 * channelCount:])
    return (channelCount, samplingInterval, resolutions, channelNames)

def GetData(rawdata, channelCount):
    (block, points, markerCount) = unpack('<LLL', rawdata[:12])
    data = []
    for i in range(points * channelCount):
        index = 12 + 4 * i
        value = unpack('<f', rawdata[index:index+4])
        data.append(value[0])
    markers = []
    index = 12 + 4 * points * channelCount
    for m in range(markerCount):
        markersize = unpack('<L', rawdata[index:index+4])
        ma = Marker()
        (ma.position, ma.points, ma.channel) = unpack('<LLl', rawdata[index+4:index+16])
        typedesc = SplitString(rawdata[index+16:index+markersize[0]])
        ma.type = typedesc[0]
        ma.description = typedesc[1]
        markers.append(ma)
        index = index + markersize[0]
    return (block, points, markerCount, data, markers)

con = socket(AF_INET, SOCK_STREAM)
con.connect(("localhost", 51244))

finish = False
data1s = []
lastBlock = -1
a=time.perf_counter()
b=a
while not finish:
    rawhdr = RecvData(con, 24)
    (id1, id2, id3, id4, msgsize, msgtype) = unpack('<llllLL', rawhdr)
    rawdata = RecvData(con, msgsize - 24)

    if msgtype == 1:
        (channelCount, samplingInterval, resolutions, channelNames) = GetProperties(rawdata)
        lastBlock = -1
        print("Start")
        print("Number of channels: " + str(channelCount))
        print("Sampling interval: " + str(samplingInterval))
        print("Resolutions: " + str(resolutions))
        print("Channel Names: " + str(channelNames))

    elif msgtype == 4:
        (block, points, markerCount, data, markers) = GetData(rawdata, channelCount)
        if lastBlock != -1 and block > lastBlock + 1:
            print("*** Overflow with " + str(block - lastBlock) + " datablocks ***")
        lastBlock = block

        if markerCount > 0:
            for m in range(markerCount):
                print("Marker " + markers[m].description + " of type " + markers[m].type)

        data1s.extend(data)
        if len(data1s) > channelCount * 400000 / samplingInterval:
            index = int(len(data1s) - channelCount * 400000 / samplingInterval)
            data1s = data1s[index:]
            for i in range(len(data1s)):
                store.append(data1s[i])
            leng=len(data1s)
            data1s = []
        b=time.perf_counter()
    elif msgtype == 3 or b-a>=5:
        print("Stop")
        finish = True

print(len(store))
import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt

# Sample rate and desired cutoff frequency
fs = 500.0  # Sample rate, Hz
cutoff = 30.0  # Desired cutoff frequency of the filter, Hz

# Normalize the frequency
nyq = 0.5 * fs
normal_cutoff = cutoff / nyq

# Design the filter
order = 4  # Filter order
b, a = signal.butter(order, normal_cutoff, btype='low', analog=False)

# Function to apply the filter
def low_pass_filter(data, b, a):
    y = signal.filtfilt(b, a, data)
    return y

# Generate a sample signal
# Apply the filter to the sample signal
q=0
while(q+500<len(store)):
    x=store[q:q+500]
    t=[w for w in range(500)]
    y = low_pass_filter(x, b, a)

    # Plot the original and filtered signals
    plt.figure()
    plt.subplot(2, 1, 1)
    plt.plot(t, x)
    plt.title('Original Signal')
    plt.subplot(2, 1, 2)
    plt.plot(t, y)
    plt.title('Filtered Signal (Low-pass)')
    plt.xlabel('Time [seconds]')
    plt.tight_layout()
    plt.show()
    q+=500
con.close()