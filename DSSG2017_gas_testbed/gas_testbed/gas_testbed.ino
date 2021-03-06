#include <Wire.h>
#include <Adafruit_ADS1015.h>
#include <stdio.h>

//for Gases sensor init
Adafruit_ADS1015 ads;    // Construct an ads1015 at the default address: 0x48
Adafruit_ADS1015 ads2(0x49);
Adafruit_ADS1015 ads3(0x4A);

int resetPin = 12;

void setup() {
  digitalWrite(resetPin, HIGH);
  delay(200);
  pinMode(resetPin, OUTPUT);     
  Wire.begin();       //join i2c bus
  Serial.begin(9600, SERIAL_8N1);
  ads.begin(); 
  ads2.begin();  
  ads3.begin();
  //ads.setGain(GAIN_ONE);
}

//GASES SENSORS
int16_t *get_gas_values() {
  static int16_t values[6];
  int Vx[4];
  float Ix[4];
  
  //initialising base voltage and current values for each gas
  Vx[0] = 818; //12bit
  Vx[1] = 823;
  Vx[2] = 812;
  Vx[3] = 810;
  Ix[0] = 0.00000000475;
  Ix[1] = 0.000000025;
  Ix[2] = 0.000000032;
  Ix[3] = 0.0000000040;
  
  //adjusting sensor values
  for (int i = 0; i < 6; i++) {
    values[i] = ads.readADC_SingleEnded(i);
    delay(10);
  }
  
  return values;
}

int16_t *get_gas_values2() {
  static int16_t values2[6];
  int Vx[4];
  float Ix[4];
  
  //initialising base voltage and current values for each gas
  Vx[0] = 818; //12bit
  Vx[1] = 823;
  Vx[2] = 812;
  Vx[3] = 810;
  Ix[0] = 0.00000000475;
  Ix[1] = 0.000000025;
  Ix[2] = 0.000000032;
  Ix[3] = 0.0000000040;
  
  //adjusting sensor values
  for (int i = 0; i < 6; i++) {
    values2[i] = ads2.readADC_SingleEnded(i);
    delay(10);
  }
  return values2;
}

int16_t *get_gas_values3() {
  static int16_t values3[6];
  int Vx[4];
  float Ix[4];
  
  //initialising base voltage and current values for each gas
  Vx[0] = 818; //12bit
  Vx[1] = 823;
  Vx[2] = 812;
  Vx[3] = 810;
  Ix[0] = 0.00000000475;
  Ix[1] = 0.000000025;
  Ix[2] = 0.000000032;
  Ix[3] = 0.0000000040;
  
  //adjusting sensor values
  for (int i = 0; i < 6; i++) {
    values3[i] = ads3.readADC_SingleEnded(i);
    delay(10);
  }
  return values3;
}


void print_gas() {
  String gas[6];
  gas[0] = "CO";
  gas[1] = "SO";
  gas[2] = "O3";
  gas[3] = "NO";
  gas[4] = "AA";
  gas[5] = "BB";

  int16_t *v = get_gas_values();
  int16_t *v2 = get_gas_values2();
  int16_t *v3 = get_gas_values3();
  
  
  for (int i = 0; i < 5; i++) {
    Serial.print(gas[i] + "_1 ");
    Serial.print(v[i]);
    Serial.print(" ");
  }
  for (int i = 0; i < 5; i++) {
    Serial.print(gas[i] + "_2 ");
    Serial.print(v2[i]);
    Serial.print(" ");
  }
  for (int i = 0; i < 5; i++) {
    Serial.print(gas[i] + "_3 ");
    Serial.print(v3[i]);
    Serial.print(" ");
  }
}


void loop() {
  int response = Serial.read();
  
  if (response == 102){ // "f" means fail
      digitalWrite(resetPin, LOW);
      delay(20);
      digitalWrite(resetPin, HIGH);
      delay(200);
    } else if (response == 103) { // "g" means good
      print_gas();
      Serial.println();
    } else {
      delay(200);
    }
    delay(20);
}
