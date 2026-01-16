#include "utils.h"
#include "bomb.h"
#include "temperature.h"
#include "conductivity.h"
#include "clock.h"

Bomb bomb(5);
Temperature temp_sensor(7);
Cond cond_sensor(A2, &temp_sensor);
Clock clock(0, 1, 2);

void setup() {
  Serial.begin(9600);
  Serial.println("Serial iniciado");

  bomb.begin();
  temp_sensor.begin();
  cond_sensor.begin();
  clock.begin();
}

void loop() {
  if (Serial.available() > 0){
    char message[BUFFER_SIZE];
    read_buffer(message, BUFFER_SIZE);

    char* module = strtok(message, " ");
    char* action = strtok(NULL, " ");

    int token = -1;
    if (action != NULL) token = atoi(action);

    response data;
    switch (*module){
      case 'B':
        data = bomb.controller(token);
      break;

      case 'T':
        data = temp_sensor.controller(token);
      break;

      case 'C':
        data = cond_sensor.controller(token);
      break;

      case 'R':
        data = clock.controller(token);
      break;

      default:
        data.status_code = 0;
        strcpy(data.message, "Invalid module code");
    }
    write_buffer(data);
  }
}