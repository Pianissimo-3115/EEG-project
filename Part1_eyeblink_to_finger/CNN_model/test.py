import serial
import time
import keras
from socket import *
from struct import *
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image

# Initialize serial communication with robust error handling
def initialize_serial(port, baudrate, timeout):
    try:
        return serial.Serial(port=port, baudrate=baudrate, timeout=timeout)
    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")
        exit(1)

arduino = initialize_serial(port='COM8', baudrate=9600, timeout=.1)

# Load the Keras model
model = keras.models.load_model("newcnn.h5")

def plottoarr(x, y):
    plt.figure(figsize=(0.64, 0.48))
    plt.plot(x, y)
    plt.axis(False)
    plt.grid('off')
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image = Image.open(buf).convert('L')
    gray_array = np.array(image)
    buf.close()
    plt.close()
    return gray_array

class Marker:
    def __init__(self):
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
        index += markersize[0]
    return (block, points, markerCount, data, markers)

# Create a tcpip socket
con = socket(AF_INET, SOCK_STREAM)
con.connect(("localhost", 51244))

finish = False
data1s = []
lastBlock = -1

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
                data1s[i] = -abs(data1s[i])
            t = [i for i in range(len(data1s))]
            a = np.reshape(np.array(plottoarr(t, data1s)), (1, 48, 64, 1))
            if model.predict(a):
                print("Blink detected")
                arduino.write(bytes("MOVE", 'utf-8'))
                # Read response from Arduino
                while arduino.in_waiting == 0:
                    pass
                response = arduino.readline().decode('utf-8').strip()
                print(response)
                # if response == "servo":
                #     print("Arduino confirmed move")
                time.sleep(1)
            data1s = []

    elif msgtype == 3:
        print("Stop")
        finish = True

con.close()
