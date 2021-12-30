#include <Arduino.h>

#define DAC1 25
#define LED 2

#include "song.h"

void setup() { 
  Serial.begin(115200);
  // initialize EEPROM with predefined size
  pinMode(LED, OUTPUT);
  pinMode(DAC1, OUTPUT);
}

void loop() {
  //digitalWrite(LED, HIGH);
  for (long i = 0; i < song_len; ++i){
    dacWrite(DAC1, song[i]);
    delayMicroseconds(song_step);
  }
}