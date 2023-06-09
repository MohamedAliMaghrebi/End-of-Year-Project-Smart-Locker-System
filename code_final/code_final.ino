#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <ESP8266WiFi.h>
#include <SPI.h>
#include <MFRC522.h>

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels

// Declaration for an SSD1306 display connected to I2C (SDA, SCL pins)
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);



const char* ssid = "......";
const char* password = ".........";





const char* host = "192.168.43.54";
const uint16_t port = 17;

constexpr uint8_t RST_PIN = D3;
constexpr uint8_t SS_PIN = D4;

const uint8_t RED_LED_PIN = D0;
const uint8_t GREEN_LED_PIN = D8;


MFRC522 rfid(SS_PIN, RST_PIN);
MFRC522::MIFARE_Key key;

void displayWelcomeMessage() {
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(WHITE);
  display.setCursor(0, 20);
  // Display static text
  display.println("BIENVENUE!");
  display.display();
  delay(100);
}

void scrollWelcomeMessage() {
  // Scroll in various directions, pausing in-between:
  display.startscrollright(0x00, 0x0F);
  delay(2000);
  display.stopscroll();
  delay(1000);
  display.startscrollleft(0x00, 0x0F);
  delay(2000);
  display.stopscroll();
  delay(1000);
  display.startscrolldiagright(0x00, 0x07);
  delay(2000);
  display.startscrolldiagleft(0x00, 0x07);
  delay(2000);
  display.stopscroll();
  delay(1000);
}
String tag1 ; 
void setup() {
  Serial.begin(9600);
  SPI.begin();
  rfid.PCD_Init();

  pinMode(RED_LED_PIN, OUTPUT); // Définir la broche rouge comme une sortie
  pinMode(GREEN_LED_PIN, OUTPUT); // Définir la broche verte comme une sortie
  
  digitalWrite(RED_LED_PIN, HIGH); // Allumer la LED rouge par défaut
  
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi!");
  

  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) { // Address 0x3D for 128x64
    Serial.println(F("SSD1306 allocation failed"));
    for(;;);
  }
  delay(2000);
  displayWelcomeMessage();
}


void loop() {
  static unsigned long tagReadTime = 0; // variable to store the tag read time
  static bool tagValid = false; // variable to store if the tag is valid or not
  String tag = ""; // declare the tag variable here
  if (!rfid.PICC_IsNewCardPresent()) {
    return;
  }

  if (rfid.PICC_ReadCardSerial()) {
    String tag = "";

    for (byte i = 0; i < 4; i++) {
      tag += rfid.uid.uidByte[i];
    }
    Serial.println(tag);
    rfid.PICC_HaltA();
    rfid.PCD_StopCrypto1();

    // OLED display message
    display.clearDisplay();
    display.setTextSize(1);
    display.setTextColor(WHITE);
    display.setCursor(0, 10);
    display.println("RFID TAG:");
    display.setCursor(0, 30);
    display.println(tag);
    display.display();

    // Send data to server
 WiFiClient client;
  if (client.connect(host, port)) {
    client.print(tag);
    client.print(",");
    client.print("hello world");
    client.print(",");
    client.print(123);
    client.flush();
    Serial.println("Sent data to server!");
    // wait for response from server
    
    while (client.connected() && !client.available());
    if (client.available()) {
      String response = client.readStringUntil('\n');
      Serial.println("Response from server: " + response);
      tag1 = response; // first variable
      String tag2 = tag; // second variable
      Serial.println("tag1: " + tag1);
      Serial.println("tag2: " + tag2);
      
      // Split the response string based on delimiter ','
    }
    client.stop();
  } else {
    Serial.println("Failed to connect to server.");
  }


    tagReadTime = millis(); // store the tag read time
    
    // turn on appropriate LED based on tag value
    
                            
     if (tag1 =="Green" )
          {digitalWrite(RED_LED_PIN, LOW);
          digitalWrite(GREEN_LED_PIN, HIGH);
          delay(1000); // Attendre une seconde
          digitalWrite(GREEN_LED_PIN, LOW); // Éteindre la LED verte
          for (int i = 0; i < 3; i++) { // Faire clignoter la LED verte 3 fois
            digitalWrite(GREEN_LED_PIN, HIGH);
            delay(200);
            digitalWrite(GREEN_LED_PIN, LOW);
            delay(200);
                                    }
                tagValid = true;
                digitalWrite(RED_LED_PIN, HIGH);
          }

                   
       else {
      digitalWrite(GREEN_LED_PIN, LOW);
      digitalWrite(RED_LED_PIN, HIGH);
      delay(1000); // Attendre une seconde
      digitalWrite(RED_LED_PIN, LOW); // Éteindre la LED verte
      for (int i = 0; i < 3; i++) { // Faire clignoter la LED verte 3 fois
        digitalWrite(RED_LED_PIN, HIGH);
        delay(200);
        digitalWrite(RED_LED_PIN, LOW);
        delay(200);
      }
      tagValid = false;
      digitalWrite(RED_LED_PIN, HIGH);
    }

    if (tagValid) {
    display.clearDisplay();
    display.setTextSize(1);
    display.setTextColor(WHITE);
     if (tag == "384148168") {
      Serial.println("Tag Valid Owner Ali: " + tag);
      display.setCursor(0, 10);
      display.println("Tag Valid Owner ");
      display.setCursor(0, 20);              
      display.println("Ali :");      
      display.setCursor(0, 30);
      display.println(tag);
      display.display();   
      delay(3000); }
       else if (tag == "1791937176") {
          Serial.println("Tag Valid Owner Melek: " + tag);
          display.setCursor(0, 10);
          display.println("Tag Valid Owner ");
          display.setCursor(0, 20);              
          display.println("Melek :");
          display.setCursor(0, 30);
          display.println(tag);
          display.display();
          delay(4000);    }
           else if (tag == "323821322") {
              Serial.println("Tag Valid Owner Mr Mourad: " + tag);
              display.setCursor(0, 10);              
              display.println("Tag Valid Owner ");
              display.setCursor(0, 20);              
              display.println("Mr Mourad :");
              display.setCursor(0, 30);
              display.println(tag);
              display.display();
              delay(4000);    }}
    else {
    display.clearDisplay();
    display.setTextSize(1);
    display.setTextColor(WHITE);
    if (tag == "18650145128"){
                    Serial.println("Tag invalide : " + tag);
                    display.setCursor(0, 10);
                    display.println("Unknown Person :");
                    display.setCursor(0, 30);
                    display.println(tag);
                    display.display(); 
                    delay(4000);   }}
    } else          {
                    Serial.println("Tag invalide : " + tag);
                    display.setCursor(0, 10);
                    display.println("Unknown Person :");
                    display.setCursor(0, 30);
                    display.println(tag);
                    display.display(); 
                    delay(4000);   }
  
// check if it's time to display "BIENVENUE!" message again
  if (tagReadTime != 0 && millis() - tagReadTime < 10000) {
    display.clearDisplay();
    display.setTextSize(1);
    display.setTextColor(WHITE);
    if (tagValid) {
      display.setCursor(0, 10);
      display.println("TAG VALIDE");
      display.setCursor(0, 30);
      display.println("BIENVENUE!");
      display.display();
    } else {
      display.setCursor(0, 10);
      display.println("TAG NON VALIDE");
      display.setCursor(0, 30);
      display.println("VERIFIER LE TAG!");
      display.display();
    }
    display.display();
    scrollWelcomeMessage();
  } 
}