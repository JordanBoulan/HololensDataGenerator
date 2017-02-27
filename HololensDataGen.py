

'''
Data Generatior code for PAV graphics and animation
Contributers: Allen Black, Jordan Boulanger
Creation Date: 10/26/2016
Last Modified Date: 02/26/17
Description: There are 6 sets of data that are generated randomly, but form a general pattern by using previous values to generate future values.
These sets of data are then parsed through and one-by-one, each data point in the set
is converted to JSON and then sent as a message via UDP
'''

import unittest
import random
import string
import time
import json
import socket




class PAVDataGenerator:

    """
    SET ALL CONSTANTS HERE BEFORE RUNNING OTHERWISE DEFAULT VALUES WILL BE USED
    Previously generated values are used to create a more realistic next value.
    Adjust how many packets are created per generation.
    When the system sends all packets in the set it starts fresh and generates a new set of packets

    
   
    @group Settings: PACKETS_PER_SET, MIN_AIRSPEED, MAX_AIRSPEED, NEXT_VALUE_RANGE_AIRSPEED
    @cvar : Settings and Variables 
    @cvar MIN_AIRSPEED: The minimum possible airspeed value for the generator to use
    @cvar MAX_AIRSPEED: The maximum possible airspeed value for the generator to use
    @cvar NEXT_VALUE_RANGE_AIRSPEED: For all values after the first one the next airspeed value will be within +- NEXT_VALUE_RANGE_AIRSPEED of the previous value
    @cvar PACKETS_PER_SET: The number of packets generated before the generator starts fresh

    @group Storage: setCount, packetNumber, batteryLevel, altitudeLevel, headingDirection, airspeedLevel, temperatureLevel, fanRPM
    @cvar setCount: The current packet to be sent in the generated set
    @cvar packetNumber: The number of packets sent in total (accross all generated sets)
    @cvar batteryLevel: The current set of battery data
    @cvar altitudeLevel: The current set of altitude data
    @cvar headingDirection: The curret set of heading data
    @cvar airspeedLevel: The current set of airspeed data
    @cvar temperatureLevel: The current set of temprature data
    @cvar fanRPM: The current set of fan data

    @sort: Settings, Storage
    

    """
    
    #Constants
    PACKETS_PER_SET = 5
    MIN_AIRSPEED = 0  
    MAX_AIRSPEED = 30
    NEXT_VALUE_RANGE_AIRSPEED = 2  

    
    
    #Variables
    setCount = 0
    packetNumber = 0
    batteryLevel = []
    altitudeLevel = []
    headingDirection = ""
    airspeedLevel = []
    temperatureLevel = []
    fanRPM = []

    
    

    def batteryDataGeneration(self):

        batteryData = []
        valPrev = 100
        while len(batteryData) < 100:
            val = random.randrange(0, 100, 2)
            if valPrev > 98:
                upperVal = 100
            else:
                upperVal = valPrev + 2
            if valPrev < 2:
                lowerVal = 0
            else:
                lowerVal = valPrev - 2
            if val >= lowerVal and val <= upperVal and val <= valPrev:
                batteryData.append(val)
                valPrev = val
        return batteryData

    def altitudeDataGeneration(self):
        altitudeData = []
        valPrev = 0
        while len(altitudeData) < 100:
            val = random.randrange(0, 11, 1)
            if valPrev == 10:
                upperVal = 11
            else:
                upperVal = valPrev + 1
            if valPrev == 1:
                lowerVal = 0
            else:
                lowerVal = valPrev - 1
            if val >= lowerVal and val <= upperVal:
                altitudeData.append(val)
                valPrev = val
        return altitudeData

    def headingDataGeneration(self):
        '''
        Returns a random heading (does not use previous values)
        '''

        headingVal = 'N'
        val = random.randint(0, 7)
        if val == 0:
            headingVal = 'N'
        elif val == 1:
            headingVal = 'NE'
        elif val == 2:
            headingVal = 'E'
        elif val == 3:
            headingVal = 'SE'
        elif val == 4:
            headingVal = 'S'
        elif val == 5:
            headingVal = 'SW'
        elif val == 6:
            headingVal = 'W'
        elif val == 7:
            headingVal == 'NW'
        return headingVal

    def temperatureDataGeneration(self):
        temperatureData = []
        valPrev = 150
        while len(temperatureData) < 100:
            val = random.randrange(0, 150, 5)
            if valPrev > 145:
                upperVal = 150
            else:
                upperVal = valPrev + 5
            if valPrev < 5:
                lowerVal = 0
            else:
                lowerVal = valPrev - 5
            if val >= lowerVal and val <= upperVal and val <= valPrev:
                temperatureData.append(val)
                valPrev = val
        return temperatureData

    def fanRPMDataGeneration(self):
        fanRPMData = []
        valPrev = 0
        while len(fanRPMData) < 100:
            val = random.randrange(0, 25000, 5000)
            if valPrev >= 20000:
                upperVal = 25000
            else:
                upperVal = valPrev + 5000
            if valPrev <= 5000:
                lowerVal = 0
            else:
                lowerVal = valPrev - 5000
            if val >= lowerVal and val <= upperVal:
                fanRPMData.append(val)
                valPrev = val
        return fanRPMData

    def airspeedDataGeneration(self):
        speedData = []  # Set to be returned
        firstVal = random.uniform(self.MIN_AIRSPEED, self.MAX_AIRSPEED)
        speedData.append(firstVal)
        lowerVal = firstVal - self.NEXT_VALUE_RANGE_AIRSPEED
        upperVal = firstVal + self.NEXT_VALUE_RANGE_AIRSPEED
        
        while len(speedData) < self.PACKETS_PER_SET:
            val = random.uniform(lowerVal, upperVal)
            speedData.append(val)

            upperVal = val + self.NEXT_VALUE_RANGE_AIRSPEED
            lowerVal = val - self.NEXT_VALUE_RANGE_AIRSPEED
            if upperVal > self.MAX_AIRSPEED:
                upperVal = self.MAX_AIRSPEED
            if lowerVal < self.MIN_AIRSPEED:
                lowerVal = self.MIN_AIRSPEED

        return speedData

    

    def PAVDataCollection(self):
        """
        This function will be used to send the data generated to a json conversion function
        Collects a lists of each generated data type and sends them to the json converter
        If it runs out of packets to send (specified by PACKETS_PER_set),
        it requests a new set from the data generator.
        """
        
        
        if self.setCount >= self.PACKETS_PER_SET or setCount == 0:
            if self.setCount >=  self.PACKETS_PER_SET:
                self.setCount = 0
                
                self.batteryLevel = self.batteryDataGeneration()
                self.altitudeLevel = self.altitudeDataGeneration()
                self.headingDirection = self.headingDataGeneration()
                self.airspeedLevel = self.airspeedDataGeneration()
                self.temperatureLevel = self.temperatureDataGeneration()
                self.fanRPM = self.fanRPMDataGeneration()
                self.packetNumber = packetNumber + 1
                dataPacket = [
                    self.batteryLevel[count],
                    self.altitudeLevel[count],
                    self.headingDirection,
                    self.airspeedLevel[count],
                    self.temperatureLevel[count],
                    self.fanRPM[count],
                    self.packetNumber,
                    ]
                self.setCount = self.setCount + 1
                return dataPacket
        elif self.setCount <= self.PACKETS_PER_SET and self.setCount != 0:
            self.headingDirection = self.headingDataGeneration()
            self.packetNumber = packetNumber + 1
            dataPacket = [
                self.batteryLevel[count],
                self.altitudeLevel[count],
                self.headingDirection,
                self.airspeedLevel[count],
                self.temperatureLevel[count],
                self.fanRPM[count],
                self.packetNumber,
                ]
            self.setCount = setCount + 1
            return dataPacket


class PAVDataStructure:
    """
    This class has an antribute/field for each data type.
    It is used as a struct to store each packet and is used by json for encoding
    """
    def __init__(
        self,
        batteryData,
        altitudeData,
        headingData,
        speedData,
        tempData,
        fanData,
        packetNumber,
        ):
        
        self.batteryData = batteryData
        self.altitudeData = altitudeData
        self.headingData = headingData
        self.speedData = speedData
        self.tempData = tempData
        self.fanData = fanData
        self.packetNumber = packetNumber


def jsonDefault(object):
    return object.__dict__


def jsonConversion():
    """
    Gets a packet from the data generator
    Puts each generated packet into an instance the struct tyoe.
    The struct containing the data is converted to a string using JSON
    This generated string is what is sent over UDP
    """
    
    PAVGeneratedData = PAVDataGenerator().PAVDataCollection()
    dataPacket1 = PAVDataStructure(
        PAVGeneratedData[0],
        PAVGeneratedData[1],
        PAVGeneratedData[2],
        PAVGeneratedData[3],
        PAVGeneratedData[4],
        PAVGeneratedData[5],
        PAVGeneratedData[6],
        )
    jsonPAVDataStructure = json.dumps(dataPacket1, default=jsonDefault)
    return str(jsonPAVDataStructure)


def sendUDP(udp_ip, udp_port):
    """
    Sends the JSON generated string to the hololens via UDP
    THIS IS THE FUNCTION TO CALL FROM MAIN
    GIVE IT AN UP AND PORT TO SEND DATA TO HOLOLENS

    @param udp_ip: The IP of the Hololens to send data to
    @param udp_port: The used to connect to the hololens
    """
    
    
    data = jsonConversion()

    # print ("UDP target IP:", UDP_IP)
    # print ("UDP target port:", UDP_PORT)

    #print MESSAGE

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    sock.sendto(data, (udp_ip, udp_port))

"""
def main():

    # for x in range(0,3):
       # time.sleep(.1)

    PAVDataGeneration().airspeedDataGeneration()


# main()
"""

class UnitTests(unittest.TestCase):

    # Tests if each value is within next value range for

    def testRange(self):

        # #########
        # Setup Variables
        # #########

        generator = PAVDataGenerator()  # Specify the data type/function to be tested, dont invoke with () just reference
        dataTestRange = 5  # set the range to be testing (change last part to data type name)
        generator.NEXT_VALUE_RANGE_AIRSPEED = dataTestRange  # WILL NEED MODIFICATION TO FIT DATATYPE (Change last part of generator.NEXT_VALUE_RANGE_
        setsToTest = 10

        ###############END OF SETUP#############

        for x in range(setsToTest):
            testSet = generator.airspeedDataGeneration()
            for index in range(1, len(testSet)):
                self.assertGreaterEqual(testSet[index], testSet[index- 1]- dataTestRange)
                self.assertLessEqual(testSet[index], testSet[index - 1] + dataTestRange)


if __name__ == '__main__':
    unittest.main()
    


			
