#include <stdint.h>
#ifndef __CLOCK_
#define __CLOCK_

#include <Arduino.h>
#include <Ds1302.h>
#include "utils.h"

class Clock{
private:
  Ds1302* rtc = nullptr;
  uint8_t CE_pin;
  uint8_t CLK_pin;
  uint8_t IO_pin;

public:
  Clock(int CE, int CLK, int IO);
  void begin();
  void get_dtf(char buffer[]);
  response controller(int action_code);
};

#endif