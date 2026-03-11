#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

const char* ssid = "YOUR_SSID";
const char* password = "YOUR_PASS";
const char* server_url = "http://YOUR_PC_IP:8000/get"; // use your PC IP, not 127.0.0.1

int ledPin = 2; // example pin

void setup() {
  Serial.begin(115200);
  pinMode(ledPin, OUTPUT);

  WiFi.begin(ssid, password);
  while(WiFi.status() != WL_CONNECTED){
    delay(500);
    Serial.print(".");
  }
  Serial.println("WiFi connected");
}

void loop() {
  if(WiFi.status() == WL_CONNECTED){
    HTTPClient http;
    http.begin(server_url);
    int code = http.GET();
    if(code > 0){
      String payload = http.getString();
      Serial.println(payload);

      // Parse JSON
      DynamicJsonDocument doc(1024);
      deserializeJson(doc, payload);
      String state = doc["state"];
      
      if(state == "ON") digitalWrite(ledPin, HIGH);
      else digitalWrite(ledPin, LOW);
    }
    http.end();
  }
  delay(1000); // poll every 1 sec
}