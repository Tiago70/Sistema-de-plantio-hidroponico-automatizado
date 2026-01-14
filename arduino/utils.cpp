#include "utils.h"

const char ERR_INVALID_OPT[] = "Invalid option";

void read_buffer(char* buffer, uint8_t length){
  int characters = Serial.readBytesUntil('\n', buffer, length - 1);
  buffer[characters] = '\0';
}

void write_buffer(response data){
  Serial.print(data.status_code);

  if (data.message != ""){
    Serial.print(" ");
    Serial.print(data.message);
  }
  Serial.println();
}
