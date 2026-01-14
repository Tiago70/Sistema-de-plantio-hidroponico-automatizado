#include "conductivity.h"

Cond::Cond(uint8_t pin, Temperature* temperature) {
  this->pin = pin;
  this->temp_sensor = temperature;
}

void Cond::begin() {
  pinMode(this->pin, INPUT);
}

float Cond::get_cond(){
  float vout = analogRead(this->pin);
  vout = (float)vout / 1023 * this->Vin;

  float resistance = this->std_resistor * (vout / (this->Vin - vout));
  float condutividade = this->std_resistor / (resistance * K);
  condutividade = condutividade * (1 / (1 + this->temp_coefficient * (this->temp_sensor->get_temp() - 25)));

  return condutividade;
}

response Cond::controller(int action_code) {
  response response_data;
  response_data.status_code = 1;
  strcpy(response_data.message, "");

  switch(action_code){
    case -1:
      dtostrf(this->get_cond(), 4, 2, response_data.message);
      return response_data;
    default:
      response_data.status_code = 0;
      strcpy(response_data.message, ERR_INVALID_OPT);
      return response_data;
  }
}