//////////////////////////////
// Programmer: Kenneth Sinder
// Date: April 25, 2014
// Filename: ultrasonic_distance_meter.ino
// Description: Program that controls and displays text
//              for an ultrasonic distance meter
//////////////////////////////

// LCD Button definitions --------------------------------------------------------
#define RIGHT 0
#define UP 1
#define DOWN 2
#define LEFT 3
#define SELECT 4
#define NONE 5

// Variables and pin names --------------------------------------------------------
#include <LiquidCrystal.h>            // include LCD library code
LiquidCrystal lcd(8, 9, 4, 5, 6, 7);  // select LCD panel pins
const int TrigPin = 39;               // ultrasound Trig pin
const int EchoPin = 37;               // Echo pin
const int GroundPin = 35;             // ultrasound ground pin
const int PositivePin = 41;           // ultrasound Vcc pin
long echoDuration = 0;                // duration of echo pulse
long durations[] = {0, 0, 0};         // multiple trials to determine duration
int adcValue = 0;                     // ADC value from the shield         
int mode = 0;                         // current meter mode
int output;                           // screen output
int savedValues[] = {0, 0, 0, 0, 0};  // saved measurements (REVIEW mode)
short storedIndex = 0;                // current index to place saved measurement (REVIEW)
short viewingIndex = 0;               // current measurement being viewed (REVIEW)
short lcdButton = 5;                  // pressed button on LCD shield
String unit = "cm";                   // current unit of measurement
String modes[] = {"MEASURING", "HOLD     ", "REVIEW     "};

// Setup function --------------------------------------------------------
void setup()
{
  pinMode(TrigPin, OUTPUT);
  pinMode(GroundPin, OUTPUT);
  pinMode(PositivePin, OUTPUT);
  pinMode(EchoPin, INPUT);
  digitalWrite(GroundPin, LOW);       // set ultrasound ground LOW
  digitalWrite(PositivePin, HIGH);    // set ultrasound Vcc HIGH
  lcd.begin(16, 2);                   // start the LCD with 2 rows and 16 columns
  lcd.setCursor(0,0);                 // position the cursor in the top left corner
}

// Helper functions --------------------------------------------------------
long durationToCentimeters(long microseconds)
{ 
  return microseconds/58;
}
long durationToInches(long microseconds) 
{
  return microseconds / 148;
}
long getDuration() 
{
  long result;
  // get multiple duration values in order to get an accurate measurement
  for (short i = 0; i < 3; i++) {
    digitalWrite(TrigPin, LOW);         // output short LOW pulse beforehand to ensure a clean HIGH pulse
    delay(3);
    digitalWrite(TrigPin, HIGH);        // the PING))) is triggered by a HIGH pulse of 10 microseconds
    delay(10);
    digitalWrite(TrigPin, LOW);
    durations[i] = pulseIn(EchoPin, HIGH);    // The EchoPin reads the HIGH pulse signal from the PING)))
    if (i > 1 && durations[i] != durations [i - 1]) {
      return echoDuration;              // if any two measurements differ, return the previous value unchanged
    }
  }
  return durations[0];                  // otherwise, reutrn the new measurement
}
int readLCDButtons() 
{
  int reading = analogRead(0);              // get the ADC value from the shield
  if (adcValue > 1000 and reading < 1000) { // if a button is pressed, and none was pressed before
    adcValue = reading;  
    if (adcValue < 90)   return RIGHT;        // RIGHT
    else if (adcValue < 200)  return UP;      // UP
    else if (adcValue < 360)  return DOWN;    // DOWN
    else if (adcValue < 450)  return LEFT;    // LEFT
    else if (adcValue < 800)  return SELECT;  // SELECT
    else return NONE;                         // when all others checks fail, consider that no key is pressed 
  }
  adcValue = reading;
  return NONE;  
}

// Main Program --------------------------------------------------------
void loop()
{
  if (mode == 0) {
    echoDuration = getDuration();        // get the ultrasound pulse duration in MEASURING mode
  }
  
  lcdButton = readLCDButtons();        // determine which button is pressed and act accordingly
  if (lcdButton == SELECT && unit == "cm") {
    unit = "in";
  }
  else if (lcdButton == SELECT && unit == "in") {
    unit = "cm";
  }  
  else if (lcdButton == UP) {
    mode++;
    mode %= 3;
  }
  else if (lcdButton == DOWN && (mode == 0 || mode == 1)) {
    // Pressing DOWN in MEASURING or HOLD mode saves the value
    savedValues[storedIndex % 5] = echoDuration;
    storedIndex++;  
    delay(50);
  }
  else if (lcdButton == LEFT) {
    viewingIndex--;
  }
  else if (lcdButton == RIGHT) {
    viewingIndex++;
  }
  if (viewingIndex < 0) {        // ensure that the viewing measurement is between 0-4
    viewingIndex += 5;
  }
  else if (viewingIndex > 4) {
    viewingIndex -= 5;
  }
  
  if (unit == "cm" && mode != 2)
    output = durationToCentimeters(echoDuration);  
  else if (mode != 2)              
    output = durationToInches(echoDuration);
  else if (unit == "cm" && mode == 2)
    output = durationToCentimeters(savedValues[viewingIndex]);
  else if (mode == 2)
    output = durationToInches(savedValues[viewingIndex]);
    
  // print the measuring mode on the first row
  lcd.setCursor(0, 0);
  lcd.print(modes[mode]);
  
  // print the correct distance value on the second row
  lcd.setCursor(0, 1);
  lcd.print((String)output + " " + unit);
  if (output < 10) {
    lcd.print("   ");
  }
  else if (output < 100) {
    lcd.print("  ");
  }
  else if (output < 1000) {
    lcd.print(" ");
  }
  
  // in REVIEW mode, print the currently viewing measurement
  lcd.setCursor(11, 0);
  if (mode == 2) {  
    lcd.print((String)(viewingIndex + 1) + "/5");
  }
  else {
    lcd.print("   ");
  } 
}

