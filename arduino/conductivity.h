#ifndef __CONDUTIVITY_
#define __CONDUTIVITY_

#include "temperature.h"
#include "utils.h"

class Cond {
private:
  // atributos para o calculo da condutividade
  uint8_t Vin = 5;                    // valor da entrada em volts (5v do arduino)
  float K = 0.996;                    // valor médio do coeficiente K
  float temp_coefficient = 0.015;     // também é um valor médio
  uint16_t std_resistor= 1000;        // valor em Ohms
  
  Temperature* temp_sensor;
  uint8_t pin;

public:
  Cond(uint8_t pin, Temperature* temperature);

  void begin();
  response controller(int action_code);
  float get_cond();
};

#endif