#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  tempserial.py
#  
#  Copyright 2015 user <user@user-HP-Compaq-nc6320-EN186UT-ABA>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
import time
import serial
import requests
from datetime import datetime
import os

server = "http://tempserver.example.com" #webserver you wish to push info to
sample_time = 5 #how many seconds we want to wait before getting temp data
in_sensor_location = "In:"
out_sensor_location = "Out:"

def main():
	print('Hi there, please choose one of the following ports:') 
	print('1- /dev/ttyACM0\n2- /dev/ttyACM1\n3- /dev/ttyS0\nENTER for manual entry')
	portnumber = raw_input("$: ")
	#determins the serialport the Arduino is on
	try:
		if portnumber == '1':
			serialport = '/dev/ttyACM0'
			print('Selected /dev/ttyACM0')
		elif portnumber == '2':
			serialport = '/dev/ttyACM1'
			print('Selected /dev/ttyACM1')
		elif portnumber == '3':
			serialport = '/dev/ttyS0'
			print('Selected /dev/ttyS0')
		elif not portnumber: #If only the enter key is pressed, then we want different data than supplied by default
			serialport = str(raw_input("$: "))
			if "/dev/" not in serialport: #Needs to change a bit to support non linux operating systems
				raise NameError("Invalid serial port, exiting")
			print('Selected ' + serialport)
		else:
			print("Invalid entry")
			
	except:
		print("You likely typed something wrong")
		time.sleep(1)
	
	internetQuery = raw_input("Do you want internet logging? (Y/n) $:") #we don't want the program to exit if there is not an internet connection so we ask
	if internetQuery == "y":
		internet = 1
	elif internetQuery == "Y":
		internet = 1
	elif internetQuery == "n":
		internet = 0
	elif internetQuery == "N":
		internet = 0
	elif not internetQuery:
		internet = 1
	else:
		print("You didn't enter stuff correctly, assuming yes")
		internet = 1
	folder_setup() #check for, and make if it isn't there, a folder for the logger data
	readtemp(serialport, internet)
	
def readtemp(port, internet):
	serialport = serial.Serial(port, 9600)
	indata = ""
	while "READY" not in indata: #the arduino code needs to init the sensors, once the text "READY" we are ready to go
		 indata = serialport.readline()
		 print(indata)
		 time.sleep(0.5)
	filename = open("datalog/temperature " + datetime.utcnow().ctime() + ".log.csv", 'w')
	filename.write("Time, Indoor temp, Outdoor temp\n") #makes processing this into a graph a lot easier
	print("accepting data now")
	while True:
		serialport.write("t") # used to trigger the arduino temp sensor readings
		tempdata = serialport.readline()
		curtime = datetime.utcnow().ctime() #current time UTC
		
		#localtempdata = str(curtime) + "C, " + str(tempdata) + "C"
		
		#text formating starts here
		cutcurtime = curtime[4:19]
		splittempdata = tempdata.split(',')
		outdoortemp = splittempdata[1]
		indoortemp = splittempdata[0]
		shortindoortemp = indoortemp[4:]
		shortoutdoortemp = outdoortemp[5:]
		#text formating ends about here
		
		splitoutdoor = outdoortemp.split(":")
		outdoortemp = out_sensor_location + splitoutdoor[1]
		splitindoortemp = indoortemp.split(":")
		indoortemp = in_sensor_location + splitindoortemp[1]
		
		outdoortemp = outdoortemp.strip()
		outdoortemp = outdoortemp + "C\n"
		
		#print(outdoortemp) #debugging
		#print(indoortemp + ".")  #debugging
		
		localtempdata = curtime + ", " + indoortemp +'C, ' + outdoortemp
		tempdata = indoortemp + 'C, ' + outdoortemp
		#print(cutcurtime + " " + indoortemp + " " + outdoortemp)
		filename.write(cutcurtime + ", " + shortindoortemp + ", " + shortoutdoortemp) #writes the temp data to the log file
		
		
		
		#filename.write(localtempdata)
		
		if internet == 1: #if we turned on internet, we want to push to a server
			remotetempdata = {'time': curtime, 'temp': tempdata}
			httpsend = requests.post(server, data=remotetempdata)
#			print(httpsend.text)
		
		print(localtempdata) #prints temp data to local output
		time.sleep(sample_time)
	
def folder_setup(): #checks for the datalog folder, and if it isn't there, make it
	if not os.path.isdir('datalog/'):
		os.makedirs("datalog/")
		print("loging directory created")

def fun_stuff():
	print("Testing Git stuff, please ignore :)")
	
		
if __name__=='__main__':
	if server == "http://tempserver.example.com":
		print("You haven't edited lines 30 and 31 yet, please do so before continuing\nIf you don't want a webserver, just change the server variable to something other than what is there")
		exit()
	main()
