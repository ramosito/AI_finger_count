const int NB_LEDS = 5;
const int PINS_LEDS[NB_LEDS] = {2, 3, 4, 5, 6};
const int PIN_BUZZER = 7;
const int NOTES[NB_LEDS] = {500, 800, 1100, 1400, 1700};

void setup() {
  for (int i = 0; i < NB_LEDS; i++) {
    pinMode(PINS_LEDS[i], OUTPUT);
  }
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    int nbDoigts = Serial.parseInt();
    nbDoigts = constrain(nbDoigts, 0, NB_LEDS);

    for (int i = 0; i < NB_LEDS; i++) {
      digitalWrite(PINS_LEDS[i], i < nbDoigts ? HIGH : LOW);
    }

    if (nbDoigts > 0) {
      tone(PIN_BUZZER, NOTES[nbDoigts - 1], 200);
    } else {
      noTone(PIN_BUZZER);
    }
  }
}