// running this on an mCore board
#include <MeMCore.h>

// flag
const int messLen = 15;
char m[] = "CSC{bl!nkBL1nk}";

// transmit function declared in module.S
extern "C" void transmit();

/******************* Global Declarations *******************************/

// Onboard LED port/slot definitions
const int PORT = 7;
const int SLOT = 2;

// LED Control settings
const int BOTH_LEDS = 0;
const int RIGHT_LED = 1;
const int LEFT_LED  = 2;

// The led that'll blink
const int ledPin = 13;

// Declare the MeRGLed object
MeRGBLed onboardLEDs(PORT, SLOT);

// helper function to control the RGB leds on the mCore
void updateLED(int led, int red, int green, int blue) {
  onboardLEDs.setColor(led, red, green, blue);
  onboardLEDs.show();
}

void setup() {
  // set the color of the RGB leds to black (off)
  updateLED(BOTH_LEDS, 0, 0, 0);

  // enable the internal led that'll carry the message
  pinMode(ledPin, OUTPUT); 
  digitalWrite(ledPin, LOW);
  Serial.begin(9600);   
}

void signalStartMessage() {
  updateLED(BOTH_LEDS, 150, 140, 130);
  delay(1000);
  updateLED(BOTH_LEDS, 0, 0, 0);
  delay(1000);
}

void loop() {
    Serial.println("Starting LO0P");
    
    // turn on the RGB leds once to signal the start of the message
    signalStartMessage();

    // transmit the message
    transmit();
    
    delay(1000);

    // restore the message for the loop
    strncpy(m, "CSC{bl!nkBL1nk}",  messLen);
}