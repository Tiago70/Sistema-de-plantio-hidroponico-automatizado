#ifndef __UTILS_
#define __UTILS_

#include <Arduino.h>

const uint8_t BUFFER_SIZE = 10;
typedef struct {
  bool status_code;
  char message [30];
} response;

extern const char ERR_INVALID_OPT[];

void read_buffer(char* buffer, uint8_t length);
void write_buffer(response data);

#endif