#ifndef __BOMB_
#define __BOMB_

#include "utils.h"

class Bomb{
private:
  uint8_t pin;

public:
  Bomb(uint8_t pin);

  void begin();
  response controller(int action_code);
};

#endif