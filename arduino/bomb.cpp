#include "Arduino.h"
#include "bomb.h"

Bomb::Bomb(uint8_t pin){
  this->pin = pin;
}

void Bomb::begin(){
  pinMode(this->pin, OUTPUT);
}

response Bomb::controller(int action_code){
  response response_data;
  response_data.status_code = 1;
  strcpy(response_data.message, "");

  switch(action_code){
    case 1:
      digitalWrite(this->pin, HIGH);
      return response_data;

    case 0:
      digitalWrite(this->pin, LOW);
      return response_data;

    case -1:
      response_data.message[0] = digitalRead(this->pin) ? '1' : '0';
      response_data.message[1] = '\0';
      return response_data;

    default:
      response_data.status_code = 0;
      strcpy(response_data.message, ERR_INVALID_OPT);
      return response_data;
  }
}