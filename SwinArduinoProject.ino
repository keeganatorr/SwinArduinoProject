//Task 1. Turning LEDs on and off based on keystroke
void setup() 
{
  pinMode(13,OUTPUT);
  pinMode(3,OUTPUT);
  Serial.begin(9600);
}

void loop()
{
   //Check if there is serial input data available 
   if (Serial.available()>0)
   {
      //Read serial input
      int value = Serial.read();
      if (value == '1')
      {
        digitalWrite(13,HIGH);
      }
      else if (value == '2')
      {
        digitalWrite(13,LOW);
      }
       else if (value == '3')
      {
        digitalWrite(3,HIGH);
      }
       else if (value == '4')
      {
        digitalWrite(3,LOW);
      }
   }

   Serial.println("test");
   delay(1000);
}