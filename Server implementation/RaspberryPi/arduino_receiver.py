import csv
import serial
import time
import datetime
#import RPi.GPIO as GPIO
#from lidar_lite import Lidar_Lite
import json
import requests
import os

# This file receives sensor data from Arduino board.
# Also, collect data from GPS.
# Both of them are coming directly from serial ports.

# PIN assignments. Change if board connections change.
SWITCH_PIN = 29
ERROR_PIN = 31
STATUS_PIN = 33
NET_STATUS_PIN = 35

# Other constants
logFileName = 'proximity.log'
DELAY = 0.1 # In seconds

# Configure GPIO        
#GPIO.setmode(GPIO.BOARD);
# GPIO.setup(SWITCH_PIN, GPIO.IN)
# GPIO.setup(ERROR_PIN,GPIO.OUT)
# GPIO.setup(STATUS_PIN,GPIO.OUT)
# GPIO.output(ERROR_PIN,True)                                                     # Make it alive only if loop starts running.
# GPIO.setup(NET_STATUS_PIN,GPIO.OUT)
# GPIO.output(NET_STATUS_PIN,0)

# JSON Labels.
jsonDataLabels = ['proxTime','UltrasoundLeft','UltrasoundRight','LidarLeft','LidarRight']
jsonStatusLabels = ['usLeftStatus','usRightStatus','lidarLeftStatus','lidarRightStatus','diskWriteStatus']
statusList = [0]*5

# Self
HOST_SERVER = '127.0.0.1'

# Network settings
headers = {'Content-type': 'application/json'}
DATA_URL = 'http://' + HOST_SERVER + ':5000/proximity'
STATUS_URL = 'http://' + HOST_SERVER + ':5000/status'

# Open a file with a name appended with current time.
timeNow=datetime.datetime.now()
fileTime=timeNow.strftime('%m-%d-%Y-%H-%M-%S')

logFile =  open(logFileName,'a')
logFile.write('Starting script at '+fileTime+'\n')
logFile.close()

#Create a new log file for this trip
dataFile = open('/home/pi/data/arduino_data.json','a')
dataFile.write('Start new trip file')
dataFile.close

# status = True
try:
        ser = serial.Serial(port='/dev/ttyACM0',baudrate=4800)

        while True:
                ser.flushInput()
                ser.flush()
                serialLine=ser.readline()
                arduinoData=serialLine.split()

                timeNow=datetime.datetime.now()
                dataTime=timeNow.strftime('%m-%d-%Y-%H-%M-%S')
                if len(arduinoData) <3:
                        logFile = open(logFileName,'a')
                        logFile.write("Could not write data at time " + str(dataTime) + " Arduino data: " + ''.join(arduinoData) + "\n")
                        logFile.close()
                        continue                        # Incomplete data
                dataList = [dataTime] + arduinoData 

                jsonData = json.dumps(dict(zip(jsonDataLabels,dataList)))

                #write json data to local file first
                dataFile = open('/home/pi/data/arduino_data.json','a')
                dataFile.write(jsonData)
                dataFile.close()

                statusList = [0,(arduinoData[0] != '0'),(arduinoData[1] != '0'),(arduinoData[2] != '0'),0]
                statusList  = [str(x).lower() for x in statusList]
                jsonStatus = json.dumps(dict(zip(jsonStatusLabels,statusList)))

                #print jsonStatus
                try:
                    response = requests.post(DATA_URL, data=jsonData, headers=headers)
                    response2 = requests.post(STATUS_URL, data=jsonStatus, headers=headers)
                    print response2.text
                except requests.exceptions.RequestException:
                    print "ERROR in posting data to URLs..."
                else:
                    if (response.status_code != requests.codes.ok) or (response2.status_code != requests.codes.ok):
                            print "Data and Status posting successful."
                    else:
                            print "Data and Status posted but no response..."
                # else:
                #         statusList = [False]*5
                #         statusList  = [str(x).lower() for x in statusList]
                #         jsonStatus = json.dumps(dict(zip(jsonStatusLabels,statusList)))
                #         #print jsonStatus
                #         try:
                #             response2 = requests.post(STATUS_URL, data=jsonStatus, headers=headers)
                #             print response2.text
                #         except requests.exceptions.RequestException:
                #                 print "Error in posting data to Status URL..."
                #         else:
                #                 if (response2.status_code != requests.codes.ok):
                #                         print "Status posting successful."
                #                 else:
                #                         print "Status posted but no response..."

                #time.sleep(DELAY)
                
except KeyboardInterrupt:
        logFile = open(logFileName,'a')
        logFile.write('Script stopped manually. \n')
        logFile.close()
except Exception as e:
        logFile = open(logFileName,'a')
        logFile.write('Error: '+str(e) + ' stopping script. \n')
        logFile.close()
