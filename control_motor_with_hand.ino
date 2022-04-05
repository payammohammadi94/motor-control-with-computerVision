#include <cvzone.h>

SerialData serialData(1,3);

int valueEntr[1]; 

void setup() {
  // put your setup code here, to run once:
  serialData.begin(9600);
  pinMode(3,OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  serialData.Get(valueEntr);
  
  digitalWrite(3,valueEntr[0]);

}
