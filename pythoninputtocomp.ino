/*
PIN LAYOUT

Output Pins: Ground, Ground
Input Pins: D2 (Left Button), D3 (Right Button)

Copyright EVG Store 2024. Built for Extreme Airsoft
*/
int pinD2 = 2;
int pinD3 = 3;

void setup() {
  Serial.begin(9600);
  Serial.println("Arduino Booted. Running PTIC V3.2");
  
  pinMode(pinD2, INPUT_PULLUP);
  pinMode(pinD3, INPUT_PULLUP);
}

void loop() {
  bool D2State = digitalRead(pinD2) == LOW;
  bool D3State = digitalRead(pinD3) == LOW;

  if (D2State && D3State) {
    Serial.println("buzzer");
  } else if (D2State) {
    Serial.println("leftB");
  } else if (D3State) {
    Serial.println("rightB");
  }

}
