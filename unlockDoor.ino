// CheapStepper - Version: Latest 
#include <CheapStepper.h>
#include <dht.h>

/* ==========================================================
Project : checkMyPlant with Google Assistant Voice integration
Author: Kevin Zhang
Created: Jan 11th 2012
==============================================================
*/

#define led 2
#define photoPin 1
#define moisturePin 0
#define tempHumidPin 7

char cmd = 'Z';

int minLight; //used to calibrate the readings
int maxLight;
int lightLevel;
int normalizedLightLevel;

int minMoisture; //used to calibrate the readings
int maxMoisture;
int moistureLevel;
int normalizedMoistureLevel;

dht DHT;

CheapStepper stepper (8,9,10,11); 
boolean moveClockwise = true;

void setup() {
 Serial.begin(9600);
 
 pinMode(led, OUTPUT);

 // Setup the starting light level limits
 lightLevel = analogRead(photoPin);
 minLight = lightLevel-20;
 maxLight = lightLevel;

 
 // Setup the starting moisture level limits
 moistureLevel = analogRead(moisturePin);
 minMoisture = moistureLevel-20;
 maxMoisture= moistureLevel;
}

void loop() { 
  cmd = 'Z';
  
  if (Serial.available() > 0){
    cmd = Serial.read();
  }
  
  if (cmd == 'O') { 
    digitalWrite(led, HIGH);
  }
  else if(cmd == 'X') {
    digitalWrite(led, LOW);
  } 
  else if(cmd == 'A') {
    /*Start of soil moisture sensor code*/
    moistureLevel = analogRead(moisturePin);
    
    if(minMoisture >  moistureLevel){
      minMoisture =  moistureLevel;
    }
    if(maxMoisture < lightLevel){
      maxMoisture = lightLevel;
    }
    
    //Adjust the light level for a normalized result b/w 0 and 100.
    normalizedMoistureLevel = map(moistureLevel, minMoisture, maxMoisture, 100, 0);
    
    /*Start of photocell code*/
    //auto-adjust the minimum and maximum limits in real time
    lightLevel = analogRead(photoPin);
    
    if(minLight > lightLevel){
      minLight = lightLevel;
    }
    if(maxLight < lightLevel){
      maxLight = lightLevel;
    }

    //Adjust the light level for a normalized result b/w 0 and 100.
    normalizedLightLevel = map(lightLevel, minLight, maxLight, 100, 0);

    /*Start of temp and humidity sensor code*/
    int chk = DHT.read11(tempHumidPin);
    
    /*Printing results to serial*/
    Serial.println(normalizedMoistureLevel);
    Serial.println(normalizedLightLevel);
    Serial.println(DHT.temperature);
    Serial.println(DHT.humidity);
  }
  else if(cmd == 'T') {
    /*Start of temp and humidity sensor code*/
    int chk = DHT.read11(tempHumidPin);
    Serial.println(DHT.temperature);  
  }
  else if(cmd == 'H') {
    /*Start of temp and humidity sensor code*/
    int chk = DHT.read11(tempHumidPin);
    Serial.println(DHT.humidity);  
  }
  else if(cmd == 'o') {
    stepper.setRpm(15); 
    Serial.println("opening");
    stepper.move (!moveClockwise, 7750);
  }
  else if(cmd == 'c') {
    stepper.setRpm(15); 
    Serial.println("closing");
    stepper.move (moveClockwise, 7750);
  }
  
  delay(50);
}
