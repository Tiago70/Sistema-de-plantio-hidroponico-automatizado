#include "temperature.h"
#include <Arduino.h>

Temperature::Temperature(uint8_t pin) {
  this->pin = pin;
}

void Temperature::begin() {
  pinMode(this->pin, INPUT);
  this->oneWire = OneWire(this->pin);
  this->sensor = DallasTemperature(&(this->oneWire));
  this->sensor.begin();
}

float Temperature::get_temp(){
  this->sensor.requestTemperatures();
  float temperature = this->sensor.getTempCByIndex(0);
  return temperature;
}

response Temperature::controller(int action_code){
  response response_data;
  response_data.status_code = 1;
  strcpy(response_data.message, "");

  switch(action_code){
    case -1:
      dtostrf(this->get_temp(), 4, 2, response_data.message);
      return response_data;
    default:
      response_data.status_code = 0;
      strcpy(response_data.message, ERR_INVALID_OPT);
      return response_data;
  }
}
