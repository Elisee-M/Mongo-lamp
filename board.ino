#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

const char* ssid = "WIFI_NAME";
const char* password = "WIFI_PASSWORD";

String server = "http://YOUR_IP:5000/get";

int ledPin = 2;

void setup() {

pinMode(ledPin, OUTPUT);

WiFi.begin(ssid,password);

while(WiFi.status()!=WL_CONNECTED){
delay(500);
}

}

void loop(){

HTTPClient http;
http.begin(server);

int httpCode = http.GET();

if(httpCode == 200){

String payload = http.getString();

StaticJsonDocument<200> doc;
deserializeJson(doc, payload);

String state = doc["state"];

if(state == "ON"){
digitalWrite(ledPin, HIGH);
}else{
digitalWrite(ledPin, LOW);
}

}

http.end();

delay(3000);

}