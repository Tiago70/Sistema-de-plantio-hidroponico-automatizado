#include "clock.h"

Clock::Clock(int CE, int CLK, int IO){
  this->CE_pin = CE; this->CLK_pin = CLK; this->IO_pin = IO;
}

void Clock::begin() {
  // Instância do RTC com pinos CE, CLK, IO
  this->rtc = new Ds1302(this->CE_pin, this->CLK_pin, this->IO_pin);
  this->rtc->init();

  // código de configuração do horário do rtc
  // (deve ser executado apenas uma vez)
  Ds1302::DateTime dt;

  dt.year = 25;    // Ano 2025 (últimos dois dígitos)
  dt.month = 6;    // Junho
  dt.day = 17;     // Dia 17
  dt.dow = 2;      // Dia da semana (Terça-feira) 0-6
  dt.hour = 15;    // 15h
  dt.minute = 20;  // 20 minutos
  dt.second = 0;   // Começa em 00 segundos

  this->rtc->setDateTime(&dt);  // Define a data e hora no RTC
}

// retorna as horas minutos e segundos atuais de forma formatada
void Clock::get_dtf(char buffer[]) {
  Ds1302::DateTime now;
  this->rtc->getDateTime(&now);

  sprintf(buffer, "20%02d-%02d-%02d %02d:%02d:%02d",
    now.year, now.month, now.day, now.hour, now.minute, now.second);
}

response Clock::controller(int action_code){
  response response_data;
  response_data.status_code = 1;

  switch(action_code){
    case -1:
      char buffer[20];
      this->get_dtf(buffer);

      strcpy(response_data.message, buffer);
      return response_data;
    default:
      response_data.status_code = 0;
      strcpy(response_data.message, ERR_INVALID_OPT);
      return response_data;
  }
}