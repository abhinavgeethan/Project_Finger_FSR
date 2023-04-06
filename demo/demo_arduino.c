const int numSensors = 6; // number of FSR sensors
const int sensorPins[numSensors] = {A0, A1, A2, A3, A4, A5}; // FSR sensor pin numbers
int samplingRate = 311; // sampling rate in microseconds

void setup() {
  Serial.begin(9600); // initialize serial communication
}

void loop() {
  int sensorData[numSensors]; // array to store sensor data
  
  // read data from each sensor
  for (int i = 0; i < numSensors; i++) {
    sensorData[i] = analogRead(sensorPins[i]);
  }

  // send sensor data to Python program via serial
  Serial.print(sensorData[0]); // first sensor data
  for (int i = 1; i < numSensors; i++) {
    Serial.print(",");
    Serial.print(sensorData[i]);
  }
  Serial.println(); // end of data line

  delayMicroseconds(samplingRate); // delay to achieve desired sampling rate
}
