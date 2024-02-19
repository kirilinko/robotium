int ledPin = 13;                  // LED connectée à la broche digitale 13
unsigned long startTime;          // Pour stocker le temps au démarrage

void setup() {
  pinMode(ledPin, OUTPUT);        // Initialise la broche de la LED en sortie
  startTime = millis();           // Sauvegarde le temps au démarrage
}

void loop() {
  unsigned long currentTime = millis(); // Obtient le temps actuel

  // Vérifie si 15 secondes se sont écoulées depuis le démarrage
  if (currentTime - startTime < 15000) {
    digitalWrite(ledPin, HIGH);   // Allume la LED
    delay(1000);                  // Attends une seconde
    digitalWrite(ledPin, LOW);    // Éteint la LED
    delay(1000);                  // Attends une seconde
  } else {
    digitalWrite(ledPin, LOW);    // Garde la LED éteinte après 15 s
  }
}
