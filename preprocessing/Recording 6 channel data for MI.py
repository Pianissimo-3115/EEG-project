"""
Simple Python RDA client for the RDA tcpip interface of the BrainVision Recorder
It reads all the information from the recorded EEG,
prints EEG and marker information to the console and calculates and
prints the average power every second

Brain Products GmbH
Gilching/Freiburg, Germany
www.brainproducts.com
"""

# needs socket and struct library
from socket import *
from struct import *
import numpy as np
import time
import keyboard
zero=[]
one=[]
two=[]
three=[]
four=[]
five=[]
# Marker class for storing marker information
class Marker:
    def __init__(self):
        self.position = 0
        self.points = 0
        self.channel = -1
        self.type = ""
        self.description = ""

# Helper function for receiving whole message
def RecvData(socket, requestedSize):
    returnStream = b''
    while len(returnStream) < requestedSize:
        databytes = socket.recv(requestedSize - len(returnStream))
        if databytes == b'':
            raise RuntimeError("connection broken")
        returnStream += databytes
 
    return returnStream   

    
# Helper function for splitting a raw array of
# zero terminated strings (C) into an array of python strings
def SplitString(raw):
    stringlist = []
    s = b""
    for i in range(len(raw)):
        if raw[i] != 0:
            s += bytes([raw[i]])
        else:
            stringlist.append(s.decode())
            s = b""

    return stringlist
    

# Helper function for extracting eeg properties from a raw data array
# read from tcpip socket
def GetProperties(rawdata):

    # Extract numerical data
    (channelCount, samplingInterval) = unpack('<Ld', rawdata[:12])

    # Extract resolutions
    resolutions = []
    for c in range(channelCount):
        index = 12 + c * 8
        restuple = unpack('<d', rawdata[index:index+8])
        resolutions.append(restuple[0])

    # Extract channel names
    channelNames = SplitString(rawdata[12 + 8 * channelCount:])

    return (channelCount, samplingInterval, resolutions, channelNames)

# Helper function for extracting eeg and marker data from a raw data array
# read from tcpip socket       
def GetData(rawdata, channelCount):

    # Extract numerical data
    (block, points, markerCount) = unpack('<LLL', rawdata[:12])

    # Extract eeg data as array of floats
    data = []
    for i in range(points * channelCount):
        index = 12 + 4 * i
        value = unpack('<f', rawdata[index:index+4])
        data.append(value[0])

    # Extract markers
    markers = []
    index = 12 + 4 * points * channelCount
    for m in range(markerCount):
        markersize = unpack('<L', rawdata[index:index+4])[0]

        ma = Marker()
        (ma.position, ma.points, ma.channel) = unpack('<LLl', rawdata[index+4:index+16])
        typedesc = SplitString(rawdata[index+16:index+markersize])
        ma.type = typedesc[0]
        ma.description = typedesc[1]

        markers.append(ma)
        index = index + markersize

    return (block, points, markerCount, data, markers)


##############################################################################################
#
# Main RDA routine
#
##############################################################################################

# Create a tcpip socket
con = socket(AF_INET, SOCK_STREAM)
# Connect to recorder host via 32Bit RDA-port
# adapt to your host, if recorder is not running on local machine
# change port to 51234 to connect to 16Bit RDA-port
con.connect(("localhost", 51244))

# Flag for main loop
finish = False

# data buffer for calculation, empty in beginning
data1s = []

# block counter to check overflows of tcpip buffer
lastBlock = -1

#### Main Loop ####
a=time.perf_counter()
b=a
started=False
while not finish:
    # print(finish)
    # Get message header as raw array of chars
    rawhdr = RecvData(con, 24)

    # Split array into useful information id1 to id4 are constants
    (id1, id2, id3, id4, msgsize, msgtype) = unpack('<llllLL', rawhdr)

    # Get data part of message, which is of variable size
    rawdata = RecvData(con, msgsize - 24)
    # print("msgtype:",msgtype)
    # Perform action dependent on the message type
    if msgtype == 1:
        # Start message, extract eeg properties and display them
        (channelCount, samplingInterval, resolutions, channelNames) = GetProperties(rawdata)
        # reset block counter
        lastBlock = -1

        print("Start")
        print("Number of channels: " + str(channelCount))
        print("Sampling interval: " + str(samplingInterval))
        print("Resolutions: " + str(resolutions))
        print("Channel Names: " + str(channelNames))


    elif b-a>=4:
        print("this")
        print(msgtype,b-a)
        # Stop message, terminate program
        print("Stop")
        print(msgtype)
        print(b-a)
        finish=True
    elif msgtype==4:
        # Data message, extract data and markers
        (block, points, markerCount, data, markers) = GetData(rawdata, channelCount)
        # Check for overflow
        if lastBlock != -1 and block > lastBlock + 1:
            print("*** Overflow with " + str(block - lastBlock) + " datablocks ***")
        lastBlock = block
        

        # Print markers, if there are some in actual block
        if markerCount > 0:
            for m in range(markerCount):
                print("Marker " + markers[m].description + " of type " + markers[m].type)

        # Put data at the end of actual buffer
        data1s.extend(data)
        # If more than 1s of data is collected, calculate average power, print it and reset data buffer
        if len(data1s) > channelCount * 1000000 / samplingInterval:
            index = int(len(data1s) - channelCount * 1000000 / samplingInterval)
            data1s = data1s[index:]

            # print(len(store),channelCount)
            # print(store[0])
            # Do not forget to respect the resolution !!!
            zero.extend(data1s[0::6])
            one.extend(data1s[1::6])            
            two.extend(data1s[2::6])            
            three.extend(data1s[3::6])            
            four.extend(data1s[4::6])            
            five.extend(data1s[5::6]) 
            data1s=[]
            
        b=time.perf_counter()
    elif msgtype == 3:
        print("that")
        print(msgtype,b-a)
        # Stop message, terminate program
        print("Stop")
        print(msgtype)
        print(b-a)
        finish = True
b=a
store=[zero,one,two,three,four,five]
np.save("Right dominant wrist movement(binary classification)\\testing\\transition.npy",np.array(store))
# Close tcpip connection
con.close()
