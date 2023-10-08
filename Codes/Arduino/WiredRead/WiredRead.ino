#include "Adafruit_MLX90393.h"
#define num 14 // Total 14 MLX90393 sensors
Adafruit_MLX90393 sensor[num];

int CS[num] = {A0, A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, A11, A12, A13};
float data_array[num*3+1];

void setup()
{
  // baud rate: 921600
  Serial.begin(921600);
  /* Wait for serial on USB platforms. */
  while (!Serial)
  {
    delayMicroseconds(10);
  }
  delayMicroseconds(1000);
  for (int i = 0; i < num; ++i)
  {
    sensor[i] = Adafruit_MLX90393();
    while (!sensor[i].begin_SPI(CS[i]))
    {
      Serial.print("No sensor ");
      Serial.print(i + 1);
      Serial.println(" found ... check your wiring?");
      delayMicroseconds(500);
    }

    while (!sensor[i].setOversampling(MLX90393_OSR_0))
    {
      Serial.print("Sensor ");
      Serial.print(i + 1);
      Serial.println(" reset OSR!");
    }
    delayMicroseconds(500);
    while (!sensor[i].setFilter(MLX90393_FILTER_2))
    {
      Serial.print("Sensor ");
      Serial.print(i + 1);
      Serial.println(" reset filter!");
      // delayMicroseconds(500);
    }
  }
}

void loop()
{ 
  int start_time = micros();
  for(int i = 0; i < num; ++i)
  {
    sensor[i].startSingleMeasurement();
  }
  // time for converting data
  delayMicroseconds(mlx90393_tconv[2][0] * 1000+100);
  for(int i = 0; i < num; ++i)
  {
    sensor[i].readMeasurement(&data_array[3*i], &data_array[3*i+1], &data_array[3*i+2]);
  }
  // record time interval
  data_array[3*num] = micros() - start_time;
  // write bytes
  Serial.write((byte*)(data_array), 4*(3*num+1)); 
}
