#include <LiquidCrystal.h>
#include <SoftwareSerial.h>

//pin number

LiquidCrystal lcd(7,8,9,10,11,12);
int machine = A2;
int coin_500 = 6;
int coin_100 = 5;

//variable to use
String blank;
String blank_1;
unsigned int bill;
int money = 0;
int before_time;
int time_gap;
int coin;

void setup(){

  // pin declare
  
  pinMode(machine,INPUT_PULLUP);
  pinMode(coin_500,INPUT);
  pinMode(coin_100,INPUT);
  lcd.begin(16,2);
  
  // Serial start
  Serial.begin(9600);
}

void loop(){
  
   while(Serial.available()){
    blank_1 = Serial.readString();
    if(blank_1=="NULL"){
      break;
    }
    money = blank_1.toInt();
    lcd.clear();
    lcd.setCursor(4,0);
    lcd.print(blank_1);
    lcd.setCursor(9,0);
    lcd.write("won");
    while(money>0){
       coin = digitalRead(coin_100);
       bill = pulseIn(machine,LOW,50000);
       if(bill>0){
        money -= 1000;
        if(money>=1000){
          blank = String(돈);
          lcd.setCursor(4,0);
          lcd.print(blank);
          lcd.setCursor(9,0);
          lcd.write("won");
          delay(1000);
        }
        else{
          blank = String(돈);
          lcd.clear();
          lcd.setCursor(5,0);
          lcd.print(blank);
          lcd.setCursor(9,0);
          lcd.write("won");
          delay(1000);
        }
       }
       else if(coin==0){
        before_time = millis();
        while(true){
          time_gap = millis() - before_time ;
          if(digitalRead(coin_500) == 0){
            money -= 500;
            if(money>=1000){
              blank = String(돈);
              lcd.setCursor(4,0);
              lcd.print(blank);
              lcd.setCursor(9,0);
              lcd.write("won");
              break;
            }
            else{
              blank = String(돈);
              lcd.clear();
              lcd.setCursor(5,0);
              lcd.print(blank);
              lcd.setCursor(9,0);
              lcd.write("won");
              break;
            }
            
          }
          if(time_gap>500){
            money -= 100;
            if(money>=1000){
              blank = String(돈);
              lcd.setCursor(4,0);
              lcd.print(blank);
              lcd.setCursor(9,0);
              lcd.write("won");
              break;
            }
            else{
              blank = String(돈);
              lcd.clear();
              lcd.setCursor(5,0);
              lcd.print(blank);
              lcd.setCursor(9,0);
              lcd.write("won");
              break;
            }
          }
        }
      }
    }
    lcd.clear();
    lcd.setCursor(2,0);
    lcd.write("you paid all");
    Serial.println("That's enough");
    blank_1 = "NULL";
   }
}
