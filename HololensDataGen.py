

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

    
   
    @group Settings: PACKETS_PER_SET, MIN_AIRSPEED, MAX_AIRSPEED, NEXT_VALUE_RANGE_AIRSPEED, MIN_FAN, MAX_FAN, NEXT_VALUE_RANGE_FAN, MIN_TEMP, MAX_TEMP, NEXT_VALUE_RANGE_TEMP, MIN_HEADING, MAX_HEADING, NEXT_VALUE_RANGE_HEADING, MIN_ALTITUDE, MAX_ALTITUDE, NEXT_VALUE_RANGE_ALTITUDE, MIN_BATTERY, MAX_BATTERY, NEXT_VALUE_RANGE_BATTERY  
    @cvar : Settings and Variables 
    @cvar MIN_AIRSPEED: The minimum possible airspeed value for the generator to use
    @cvar MAX_AIRSPEED: The maximum possible airspeed value for the generator to use
    @cvar NEXT_VALUE_RANGE_AIRSPEED: For all values after the first one the next airspeed value will be within +- NEXT_VALUE_RANGE_AIRSPEED of the previous value
    @cvar PACKETS_PER_SET: The number of packets generated before the generator starts fresh
    @cvar MIN_FAN: The minimum possible fan rpm, value for the generator to use
    @cvar MAX_FAN: The maximum possible fan rpm value for the generator to use
    @cvar NEXT_VALUE_RANGE_FAN: For all values after the first one the next value will be within +- NEXT_VALUE_RANGE_FAN of the previous value
    @cvar MIN_TEMP: The minimum possible temp, value for the generator to use
    @cvar MAX_TEMP: The maximum possible temp value for the generator to use
    @cvar NEXT_VALUE_RANGE_TEMP all values after the first one the next value will be within +- NEXT_VALUE_RANGE_TEMP of the previous value
    @cvar MIN_HEADING: The minimum possible heading, value for the generator to use
    @cvar MAX_HEADING: The maximum possible heading value for the generator to use
    @cvar NEXT_VALUE_RANGE_HEADING all values after the first one the next value will be within +- NEXT_VALUE_RANGE_HEADING of the previous value
    @cvar MIN_ALTITUDE: The minimum possible altitude, value for the generator to use
    @cvar MAX_ALTITUDE: The maximum possible altitude value for the generator to use
    @cvar NEXT_VALUE_RANGE_ALTITUDE all values after the first one the next value will be within +- NEXT_VALUE_RANGE_ALTITUDE of the previous value
    @cvar MIN_BATTERY: The minimum possible battery, value for the generator to use
    @cvar MAX_BATTERY: The maximum possible battery value for the generator to use
    @cvar NEXT_VALUE_RANGE_BATTERY all values after the first one the next value will be within +- NEXT_VALUE_RANGE_BATTERY of the previous value



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
    
    #Constants (set these)
    PACKETS_PER_SET = 500

    MIN_AIRSPEED = 0  
    MAX_AIRSPEED = 30
    NEXT_VALUE_RANGE_AIRSPEED = 2
    
    MIN_FAN = 0  
    MAX_FAN = 30
    NEXT_VALUE_RANGE_FAN = 2
    
    MIN_TEMP = 0  
    MAX_TEMP = 30
    NEXT_VALUE_RANGE_TEMP = 2

    MIN_HEADING = 0  
    MAX_HEADING = 30
    NEXT_VALUE_RANGE_HEADING = 2

    MIN_ALTITUDE = 0  
    MAX_ALTITUDE = 30
    NEXT_VALUE_RANGE_ALTITUDE = 2

    MIN_BATTERY = 0  
    MAX_BATTERY = 30
    NEXT_VALUE_RANGE_BATTERY = 2

    

    #Variables/Storage (leave these alone)
    setCount = 0
    packetNumber = 0
    batteryLevel = []
    altitudeLevel = []
    headingDirection = ""
    airspeedLevel = []
    temperatureLevel = []
    fanRPM = []

    
    

    def batteryDataGeneration(self):
        '''
        Returns a a set of random set of battery data, using previous values to generate next ones
        '''

        batteryData = []  # Set to be returned
        firstVal = random.uniform(self.MIN_BATTERY, self.MAX_BATTERY)
        batteryData.append(firstVal)
        lowerVal = firstVal - self.NEXT_VALUE_RANGE_BATTERY
        upperVal = firstVal + self.NEXT_VALUE_RANGE_BATTERY
        
        while len(batteryData) < self.PACKETS_PER_SET:
            val = random.uniform(lowerVal, upperVal)
            batteryData.append(val)

            upperVal = val + self.NEXT_VALUE_RANGE_BATTERY
            lowerVal = val - self.NEXT_VALUE_RANGE_BATTERY
            if upperVal > self.MAX_BATTERY:
                upperVal = self.MAX_BATTERY
            if lowerVal < self.MIN_BATTERY:
                lowerVal = self.MIN_BATTERY

        return batteryData

    def altitudeDataGeneration(self):
        '''
        Returns a a set of random altitudes, using previous values to generate next ones
        '''
        
        altitudeData = []  # Set to be returned
        firstVal = random.uniform(self.MIN_ALTITUDE, self.MAX_ALTITUDE)
        altitudeData.append(firstVal)
        lowerVal = firstVal - self.NEXT_VALUE_RANGE_ALTITUDE
        upperVal = firstVal + self.NEXT_VALUE_RANGE_ALTITUDE
        
        while len(altitudeData) < self.PACKETS_PER_SET:
            val = random.uniform(lowerVal, upperVal)
            altitudeData.append(val)

            upperVal = val + self.NEXT_VALUE_RANGE_ALTITUDE
            lowerVal = val - self.NEXT_VALUE_RANGE_ALTITUDE
            if upperVal > self.MAX_ALTITUDE:
                upperVal = self.MAX_ALTITUDE
            if lowerVal < self.MIN_ALTITUDE:
                lowerVal = self.MIN_ALTITUDE

        return altitudeData

    def headingDataGeneration(self):
        '''
        Returns a a set of random headings in degree's, using previous values to generate next ones
        '''

        headingData = []  # Set to be returned
        firstVal = random.uniform(self.MIN_HEADING, self.MAX_HEADING)
        headingData.append(firstVal)
        lowerVal = firstVal - self.NEXT_VALUE_RANGE_HEADING
        upperVal = firstVal + self.NEXT_VALUE_RANGE_HEADING
        
        while len(headingData) < self.PACKETS_PER_SET:
            val = random.uniform(lowerVal, upperVal)
            headingData.append(val)

            upperVal = val + self.NEXT_VALUE_RANGE_HEADING
            lowerVal = val - self.NEXT_VALUE_RANGE_HEADING
            if upperVal > self.MAX_HEADING:
                upperVal = self.MAX_HEADING
            if lowerVal < self.MIN_HEADING:
                lowerVal = self.MIN_HEADING

        return headingData


    def temperatureDataGeneration(self):
        '''
        Returns a a set of temperature, using previous values to generate next ones
        '''
        
        tempData = []  # Set to be returned
        firstVal = random.uniform(self.MIN_TEMP, self.MAX_TEMP)
        tempData.append(firstVal)
        lowerVal = firstVal - self.NEXT_VALUE_RANGE_TEMP
        upperVal = firstVal + self.NEXT_VALUE_RANGE_TEMP
        
        while len(tempData) < self.PACKETS_PER_SET:
            val = random.uniform(lowerVal, upperVal)
            tempData.append(val)

            upperVal = val + self.NEXT_VALUE_RANGE_TEMP
            lowerVal = val - self.NEXT_VALUE_RANGE_TEMP
            if upperVal > self.MAX_TEMP:
                upperVal = self.MAX_TEMP
            if lowerVal < self.MIN_TEMP:
                lowerVal = self.MIN_TEMP

        return tempData


    def fanRPMDataGeneration(self):
        '''
        Returns a a set of fan, using previous values to generate next ones
        '''
        
        fanData = []  # Set to be returned
        firstVal = random.uniform(self.MIN_FAN, self.MAX_FAN)
        fanData.append(firstVal)
        lowerVal = firstVal - self.NEXT_VALUE_RANGE_FAN
        upperVal = firstVal + self.NEXT_VALUE_RANGE_FAN
        
        while len(fanData) < self.PACKETS_PER_SET:
            val = random.uniform(lowerVal, upperVal)
            fanData.append(val)

            upperVal = val + self.NEXT_VALUE_RANGE_FAN
            lowerVal = val - self.NEXT_VALUE_RANGE_FAN
            if upperVal > self.MAX_FAN:
                upperVal = self.MAX_FAN
            if lowerVal < self.MIN_FAN:
                lowerVal = self.MIN_FAN

        return fanData


                
    def airspeedDataGeneration(self):
        '''
        Returns a a set of random airspeed data, using previous values to generate next ones
        '''
        
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

    def testNextValRangeANDSetSize(self):

        # #########
        # Setup Variables
        # #########

        generator = PAVDataGenerator()  # Specify the data type/function to be tested, dont invoke with () just reference
        setsToTest = 100

        ###############END OF SETUP#############
    
        for x in range(setsToTest):
            testSet = generator.airspeedDataGeneration() # SELECT TYPE
            for index in range(1, len(testSet)):
                self.assertGreaterEqual(testSet[index], testSet[index- 1]- generator.NEXT_VALUE_RANGE_AIRSPEED) # modify to fit type
                self.assertLessEqual(testSet[index], testSet[index - 1] + generator.NEXT_VALUE_RANGE_AIRSPEED)
                self.assertEqual(len(testSet), generator.PACKETS_PER_SET)

            testSet = generator.altitudeDataGeneration() # SELECT TYPE
            for index in range(1, len(testSet)):
                self.assertGreaterEqual(testSet[index], testSet[index- 1]- generator.NEXT_VALUE_RANGE_ALTITUDE) # modify to fit type
                self.assertLessEqual(testSet[index], testSet[index - 1] + generator.NEXT_VALUE_RANGE_ALTITUDE)
                self.assertEqual(len(testSet), generator.PACKETS_PER_SET)

            testSet = generator.fanRPMDataGeneration() # SELECT TYPE
            for index in range(1, len(testSet)):
                self.assertGreaterEqual(testSet[index], testSet[index- 1]- generator.NEXT_VALUE_RANGE_FAN) # modify to fit type
                self.assertLessEqual(testSet[index], testSet[index - 1] + generator.NEXT_VALUE_RANGE_FAN)
                self.assertEqual(len(testSet), generator.PACKETS_PER_SET)

            testSet = generator.temperatureDataGeneration() # SELECT TYPE
            for index in range(1, len(testSet)):
                self.assertGreaterEqual(testSet[index], testSet[index- 1]- generator.NEXT_VALUE_RANGE_TEMP) # modify to fit type
                self.assertLessEqual(testSet[index], testSet[index - 1] + generator.NEXT_VALUE_RANGE_TEMP)
                self.assertEqual(len(testSet), generator.PACKETS_PER_SET)
                
            testSet = generator.headingDataGeneration() # SELECT TYPE
            for index in range(1, len(testSet)):
                self.assertGreaterEqual(testSet[index], testSet[index- 1]- generator.NEXT_VALUE_RANGE_HEADING) # modify to fit type
                self.assertLessEqual(testSet[index], testSet[index - 1] + generator.NEXT_VALUE_RANGE_HEADING)
                self.assertEqual(len(testSet), generator.PACKETS_PER_SET)

            testSet = generator.batteryDataGeneration() # SELECT TYPE
            for index in range(1, len(testSet)):
                self.assertGreaterEqual(testSet[index], testSet[index- 1]- generator.NEXT_VALUE_RANGE_BATTERY) # modify to fit type
                self.assertLessEqual(testSet[index], testSet[index - 1] + generator.NEXT_VALUE_RANGE_BATTERY)
                self.assertEqual(len(testSet), generator.PACKETS_PER_SET)


    

   
            
if __name__ == '__main__':
    unittest.main()
    


			
