'''
Data Generation code for PAV graphics and animation
Created by Allen Black
Creation Date: 10/26/2016
Last Modified by: Allen Black
Last Modified Date: 11/30/16
Description: There are 6 sets of data that are generated randomly, but form a general pattern.
        These sets of data are then parsed through and one-by-one, each data point in the set
        is converted to JSON and then sent as a message via UDP
'''
#https://gist.github.com/sloria/7001839
import unittest
import random
import string
import time
import json
import socket

'''
global variables for moving through generated lists of data
'''
global count
global packetNumber
count = 0
packetNumber = 0

'''
class PAVDataGeneration() is used for generating all the sets of data for the
    battery, altitude, airspeed, temperature, heading, and the fan RPM. 
'''
class PAVDataGeneration():
    '''
    Calling batteryDataGeneration returns a list of length 100 of battery values starting at 100,
    and heads to 0.
    '''
    def batteryDataGeneration(self):
        batteryData = []
        valPrev = 100
        while (len(batteryData) < 100):
            val = random.randrange(0, 100, 2)
            if valPrev > 98:
                upperVal = 100
            else:
                upperVal = valPrev + 2
            if valPrev < 2:
                lowerVal = 0
            else:
                lowerVal = valPrev - 2
            if(val >= lowerVal and val <= upperVal and val <= valPrev):
                batteryData.append(val)
                valPrev = val
        return batteryData

    '''    
    Calling altitudeDataGeneration() returns a list that is 100 values long and starts at 0, and
    increases to 10 as a max.
    '''
    def altitudeDataGeneration(self):
        altitudeData = []
        valPrev = 0
        while (len(altitudeData) < 100):
            val = random.randrange(0, 11, 1)
            if valPrev == 10:
                upperVal = 11
            else:
                upperVal = valPrev + 1
            if valPrev == 1:
                lowerVal = 0
            else:
                lowerVal = valPrev - 1
            if(val >= lowerVal and val <= upperVal):
                altitudeData.append(val)
                valPrev = val
        return altitudeData
 
    '''
    Calling headingDataGeneration() returns a list that is 100 values long and randomly switches
    between various compass directions
    G-force data as well as turn angle/bank should all be real data from the accelerometer
    '''
    def headingDataGeneration(self):
        headingVal = "N"
        val = random.randint(0, 7)
        if val == 0:
            headingVal = "N"
        elif val == 1:
            headingVal = "NE"
        elif val == 2:
            headingVal = "E"
        elif val == 3:
            headingVal = "SE"
        elif val == 4:
            headingVal = "S"
        elif val == 5:
            headingVal = "SW"
        elif val == 6:
            headingVal = "W"
        elif val == 7:
            headingVal == "NW"
        return headingVal
    '''
    temperatureDataGeneration() creates a list of values from 1
    '''
    def temperatureDataGeneration(self):
        temperatureData = []
        valPrev = 150
        while (len(temperatureData) < 100):
            val = random.randrange(0, 150, 5)
            if valPrev > 145:
                upperVal = 150
            else:
                upperVal = valPrev + 5
            if valPrev < 5:
                lowerVal = 0
            else:
                lowerVal = valPrev - 5
            if(val >= lowerVal and val <= upperVal and val <= valPrev):
                temperatureData.append(val)
                valPrev = val
        return temperatureData

    def fanRPMDataGeneration(self):
        fanRPMData = []
        valPrev = 0
        while (len(fanRPMData) < 100):
            val = random.randrange(0, 25000, 5000)
            if valPrev >= 20000:
                upperVal = 25000
            else:
                upperVal = valPrev + 5000
            if valPrev <= 5000:
                lowerVal = 0
            else:
                lowerVal = valPrev - 5000
            if(val >= lowerVal and val <= upperVal):
                fanRPMData.append(val)
                valPrev = val
        return fanRPMData
                
    def airspeedDataGeneration(self):
        speedData = []
        valPrev = 0
        while (len(speedData) < 100):
            val = random.randrange(0, 30, 2)
            if valPrev >= 28:
                upperVal = 30
            else:
                upperVal = valPrev + 2
            if valPrev <= 2:
                lowerVal = 0
            else:
                lowerVal = valPrev - 2
            if(val >= lowerVal and val <= upperVal):
                speedData.append(val)
                valPrev = val
        return speedData
    
    #this function will be used to send the data generated to a json conversion function
    def PAVDataCollection(self):
        global count
        global packetNumber
        global batteryLevel
        global altitudeLevel
        global headingDirection
        global airspeedLevel
        global temperatureLevel
        global fanRPM
        if count >= 100 or count == 0:
            if count >= 100:
                count = count%100
            if count == 0:
                batteryLevel = self.batteryDataGeneration()
                altitudeLevel = self.altitudeDataGeneration()
                headingDirection = self.headingDataGeneration()
                airspeedLevel = self.airspeedDataGeneration()
                temperatureLevel = self.temperatureDataGeneration()
                fanRPM = self.fanRPMDataGeneration()
                packetNumber = packetNumber + 1
                dataPacket = [batteryLevel[count], altitudeLevel[count],
                             headingDirection, airspeedLevel[count],
                             temperatureLevel[count], fanRPM[count], packetNumber]
                count = count + 1
                return dataPacket
        elif (count <= 100 and count != 0):
            headingDirection = self.headingDataGeneration()
            packetNumber = packetNumber + 1
            dataPacket = [batteryLevel[count], altitudeLevel[count],
                         headingDirection, airspeedLevel[count],
                         temperatureLevel[count], fanRPM[count], packetNumber]
            count = count + 1
            return dataPacket

        
        
        
        


class PAVDataStructure(object):
    def __init__(self, batteryData, altitudeData, headingData, speedData, tempData, fanData, packetNumber):
        self.batteryData = batteryData
        self.altitudeData = altitudeData
        self.headingData = headingData
        self.speedData = speedData
        self.tempData = tempData
        self.fanData = fanData
        self.packetNumber = packetNumber
        
def jsonDefault(object):    
    return object.__dict__
    
def jsonPAVDataGenerator():
    PAVGeneratedData = PAVDataGeneration().PAVDataCollection()
    dataPacket1 = PAVDataStructure(PAVGeneratedData[0], PAVGeneratedData[1],
                                    PAVGeneratedData[2], PAVGeneratedData[3],
                                    PAVGeneratedData[4], PAVGeneratedData[5], PAVGeneratedData[6])
    jsonPAVDataStructure = json.dumps(dataPacket1, default=jsonDefault)
    return str(jsonPAVDataStructure)

def PAVUDP():
    UDP_IP = "192.168.42.17"
    UDP_PORT = 5005
    MESSAGE = jsonPAVDataGenerator()
    #print ("UDP target IP:", UDP_IP)
    #print ("UDP target port:", UDP_PORT)
    print (MESSAGE)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

def main():
    for x in range(0,180):
        time.sleep(.1)
        PAVUDP()


#main()


class UnitTests(unittest.TestCase):

    #UNIT Test 1
    def testBatteryListSize(self):
        listOfBatteryVals = PAVDataGeneration().batteryDataGeneration()
        self.assertTrue(len(listOfBatteryVals) == 100)

    #Unit Test 2
    def testAltitudeValues(self):
        listOfAltitudeVals = PAVDataGeneration().altitudeDataGeneration()
        for altitudeVal in listOfAltitudeVals:
            self.assertGreaterEqual(altitudeVal, 0)
            self.assertLessEqual(altitudeVal, 10)
        



if __name__ == '__main__':
    unittest.main();
    
self.assertGreaterEqual(altitudeVal, 0)
