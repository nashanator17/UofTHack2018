from flask import Flask 
from flask_assistant import Assistant, ask, tell
from flask_ask import Ask, question, statement
from random import randint
import serial 
from recognition_tutorial import initialization, recognize

arduinoSerial = serial.Serial("/dev/ttyACM0", 9600, timeout=1)
app = Flask(__name__) 
assist = Assistant(app, '/') 
ask = Ask(app, '/')
	
isDoorOpen = 0
initialization();
	
#start of Google Assistant handler
@assist.action("Default Welcome Intent")
def launch():	
	return ask("Welcome, this is eye lock!")

@assist.action("testLightOn") 
def testLightOn(): 
   	arduinoSerial.write(b'O') 
   	return ask("Test light turned on!") 

@assist.action("testLightOff") 
def testLightOff(): 
   	arduinoSerial.write(b'X') 
   	return ask("Test light turned off!") 

@assist.action("getOutdoorCondition") 
def getOutdoorCondition():
	arduinoSerial.write(b'A')
	soilMoisture = arduinoSerial.readline()
   	sunLight = arduinoSerial.readline()
   	temperature = arduinoSerial.readline()
   	humidity = arduinoSerial.readline()
   	
   	if (int(soilMoisture) < 15):
   		soilMoisture = "dry. "
   	elif (int(soilMoisture) < 25):
   		soilMoisture = "fairly dry. "
   	elif (int(soilMoisture) < 60):
   		soilMoisture = "damp. "
   	elif (int(soilMoisture) < 80):
   		soilMoisture = "fairly wet. "
   	else: soilMoisture = "flooded. "
   	
   	if (int(sunLight) < 10):
   		sunLight = "It is pitch black, probably night time. "	
   	elif (int(sunLight) < 25):
   		sunLight = "There seems to be moonlight, it is probably night time. " 	
   	elif (int(sunLight) < 50):
   		sunLight = "It is cloudy, overcast skies. "	
   	elif (int(sunLight) < 80):
   		sunLight = "It is a nice day, but not excessively bright. "   	
   	else: sunLight = "It is super bright. "
   	
   	returnStatement = "Here is information about the weather outside. The ground is " + soilMoisture + sunLight + "The temperature is " + str(float(temperature)) + " degrees Celsius. " + "And the relative humidity is " + str(float(humidity)) + " percent."
   	
   	return tell(returnStatement)
	

@assist.action("doorUnlock") 
def doorUnlock():
	global isDoorOpen
	if (recognize() == "s1" and isDoorOpen == 0): 
		arduinoSerial.write(b'o')
		isDoorOpen = 1
		return tell("Door has been unlocked")
	
	return ask("Sorry, your face is not recognized, would you like to try again?")


@assist.action("doorLock") 
def doorLock():
	global isDoorOpen
	if (isDoorOpen == 1):
		arduinoSerial.write(b'c')
		isDoorOpen = 0
		
	return tell("Door has been locked")

@assist.action("checkTemp")
def checkTemp():
	arduinoSerial.write(b'T')
	temperature = arduinoSerial.readline()
	returnStatement = "The temperature is " + str(float(temperature)) + " degrees Celsius. "
	return tell(returnStatement)

@assist.action("checkHumid")
def checkHumid():
	arduinoSerial.write(b'H')
	humidity = arduinoSerial.readline()
	returnStatement = "The relative humidity is " + str(float(humidity)) + " percent."
	return tell(returnStatement)

if __name__ == "__main__":
	app.run(debug=True) 


