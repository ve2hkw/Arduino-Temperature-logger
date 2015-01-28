#include <OneWire.h>
#include <DallasTemperature.h>

#define CODE_VERSION "2014010906"

// Data wire is plugged into port 3 on the Arduino
#define ONE_WIRE_BUS 3
#define TEMPERATURE_PRECISION 12

// Simulate Temp sensor using array
//#define SIM_TEMP

// Setup a oneWire instance to communicate with any OneWire devices (not just Maxim/Dallas temperature ICs)
OneWire oneWire(ONE_WIRE_BUS);

// Pass our oneWire reference to Dallas Temperature. 
DallasTemperature sensors(&oneWire);

// arrays to hold device addresses
DeviceAddress insideThermometer   = { 0x28, 0x21, 0x66, 0x02, 0x04, 0x00, 0x00, 0x8B}, 
              outsideThermometer = { 0x28, 0x96, 0x82, 0x02, 0x04, 0x00, 0x00, 0xCC};
int Err=0;    // To sim errors


#ifdef SIM_TEMP
float Temp_array[] = {  22.2, -7.1, 22.2, -7.4, 22.3, -7.7, 22.4, -8.2, 22.2, -8.3, 22.3, -8.8, 22.7, -8.7, 22.5, -8.1, 
  22.3, -7.6, 22.1, -7.2, 22.0, -6.8, 22.1, -7.0 };      // Array of Temperature pairs, Inside, Outside, Inside...
int Temp_array_size=23;      // Array size-1
int Temp_array_p=0;          // Array pointer
#endif

void setup(void)
{
  // start serial port
  Serial.begin(9600);
  Serial.println("DS18B20 Temperature Sensors");

  delay(2000);
  
  // Start up the library
  sensors.begin();

  // locate devices on the bus
  Serial.print(sensors.getDeviceCount(), DEC);
  Serial.println(" devices found.");

  // report parasite power requirements
  Serial.print("Parasite power is: "); 
  if (sensors.isParasitePowerMode()) Serial.println("ON");
  else Serial.println("OFF");

  // set the resolution to 12 bit
  sensors.setResolution(insideThermometer, TEMPERATURE_PRECISION);
  sensors.setResolution(outsideThermometer, TEMPERATURE_PRECISION);

  Serial.println("Press t for temperature");
  Serial.println("READY");

}


//-------------------------------------------------------------------------------------------------------
// function to switch char to uppercase

int uppercase (int charbytein)
{
  if ((charbytein > 96) && (charbytein < 123)) {
    charbytein = charbytein - 32;
  }
  return charbytein;
}

//-------------------------------------------------------------------------------------------------------
// function to print the temperature for a device
void printTemperature(DeviceAddress deviceAddress)
{
#ifdef SIM_TEMP
  if (Temp_array_p > Temp_array_size) Temp_array_p=0;
  float tempC = Temp_array[Temp_array_p];
  Temp_array_p++;
#endif

#ifndef SIM_TEMP
  float tempC = sensors.getTempC(deviceAddress);
#endif

  if (tempC == -127.0 || Err) Serial.print("ERR");
  else Serial.print(tempC,1);
}


void loop(void)
{ 
byte serial_byte;

  while (1) {
    if (Serial.available() == 0) {  // wait for the next key
    } else { 
      serial_byte = Serial.read();
      serial_byte = uppercase(serial_byte);
    
      switch (serial_byte) {
        case 'T':  // Key 't' Temp req
#ifndef SIM_TEMP
        // call sensors.requestTemperatures() to issue a global temperature 
        // request to all devices on the bus
        sensors.requestTemperatures();
#endif

        Serial.print("In: ");
        printTemperature(insideThermometer);
        Serial.print(", Out: ");
        printTemperature(outsideThermometer);
        Serial.println();
        break;
        
        case 'E':  // Key 'e' Error req
#ifndef SIM_TEMP
        // call sensors.requestTemperatures() to issue a global temperature 
        // request to all devices on the bus
        sensors.requestTemperatures();
#endif

        Serial.print("In: ");
        printTemperature(insideThermometer);
        Serial.print(" Out: ");
        Err=1;
        printTemperature(outsideThermometer);
        Serial.println();
        Err=0;
        break;
      }
    }      
  }
}

