#ifndef __TEMPERATURE_
#define __TEMPERATURE_

#include <DallasTemperature.h>
#include <OneWire.h>
#include "utils.h"

class Temperature {
private:
  DallasTemperature sensor;
  OneWire oneWire;

  uint8_t pin;

public:
  Temperature(uint8_t pin);

  void begin();
  response controller(int action_code);
  float get_temp();
};
#endif