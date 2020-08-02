// ----------------------------
//   SETUP
// ----------------------------

// the number of the LED pin
const int nipple0 = 14; 
const int nipple0Channel = 0;
const int nipple1 = 15; 
const int nipple1Channel = 1;

// setting PWM properties
const int freq = 5000;
const int resolution = 8;


String inputString = "";

unsigned long nextPulse;
int tick;

void setup() {
  Serial.begin(115200);
  inputString.reserve(200);

  // configure LED PWM functionalitites
  ledcSetup(nipple0Channel, freq, resolution);
  ledcSetup(nipple1Channel, freq, resolution);
  
  ledcAttachPin(nipple0, nipple0Channel);
  ledcAttachPin(nipple1, nipple1Channel);

  // Set servo pulse interval
  tick = 10;
  // Set time for first pulse
  nextPulse = millis() + tick;
}

void loop() {
  if (Serial.available() > 0) {
    char inChar = (char)Serial.read();

    if (inChar == '\n') {
      processSerialBuffer();
    } else {
      inputString += inChar;
    }
  }

  if (millis() > nextPulse) {
    unsigned long t = nextPulse;
    nextPulse = nextPulse + tick;
  }
}

void processSerialBuffer() {
  String command = getValue(inputString, ',', 0);
  if (command == "VIB") {
    String channel = getValue(inputString, ',', 1);
    String level = getValue(inputString, ',', 2);
    
    switch (channel.toInt()) {
      case 0:
        ledcWrite(nipple0Channel, level.toInt());   
        break;
      case 1:
        ledcWrite(nipple1Channel, level.toInt());   
        break;
      
    }
  }

  inputString = "";
}

String getValue(String data, char separator, int index) {
    int found = 0;
    int strIndex[] = { 0, -1 };
    int maxIndex = data.length() - 1;

    for (int i = 0; i <= maxIndex && found <= index; i++) {
        if (data.charAt(i) == separator || i == maxIndex) {
            found++;
            strIndex[0] = strIndex[1] + 1;
            strIndex[1] = (i == maxIndex) ? i+1 : i;
        }
    }
    return found > index ? data.substring(strIndex[0], strIndex[1]) : "";
}
