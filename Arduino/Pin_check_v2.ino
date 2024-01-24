// Jan 2024 - Dario Aguiar [OUTPUT Group: Monitoring]
// Der Code liest die Pins 2 - 14 von Arduino ab und rechnet diese Werte für
// die Kurvenerstellung bzw. Monitoring um. (Pin 6 frei)
//
// Quelle:  Code aus dem Übergabeprotokoll 2023 (emonKT.ino) und BA von Cansin Anil Cari.

// To Do:
// Z.70 - Beschreibung in emonKT sagt nur Cg was bedeutet das genau? Netzteilstrom?
// Z.122 und 129 - Die Pins müssen überorüft werden. Laut PinB: Ta: Außentemp und Tb: Batterietemp. Aber auf der BA steht andersum.

float Cpv;
float Cwt;
float Cc;
float Cg;
float Cbp;
float Cbn;
float Sw;
float Dw;
float Vb;
float Is;
float Ta;
float Tb;
int takt = 5000;

void setup() {
pinMode (2, INPUT);
pinMode (3, INPUT);
pinMode (4, INPUT);
pinMode (5, INPUT);
pinMode (7, INPUT);
pinMode (8, INPUT);
pinMode (9, INPUT);
pinMode (10, INPUT);
pinMode (11, INPUT);
pinMode (12, INPUT);
pinMode (13, INPUT);
pinMode (14, INPUT);
  Serial.print(F(" [INSELFITNESS] Messdaten Pins 2-14"));
      Serial.println();

Serial.begin (9600);
}

void loop() {
  
    static unsigned long sensortStamp = 0; // static unsigned long : cumsum (static) Variable ohne vorzeichen (nur positive Werte) mit langen Format 
    
    if(millis() - sensortStamp > takt){    // millis läuft solange wie Arduino eingeschaltet ist. Wird in diesem Fall verwendet um den Takt über die Zeit zu halten ohne delay
    sensortStamp = millis();

    //-------------PVA-Strom---------------
      int reading0 = analogRead(2);
      Serial.print(F("<"));
      Cpv = (((analogRead(2)-105)/(15.8))*(100.00/3))/1000;
      Serial.print(Cpv);
      Serial.print(F(","));

    //-------------WKA-Strom---------------
      int reading1 = analogRead(3);
      Cwt = (((analogRead(3)-119)/(15.8))*(200.00/3))/1000;
      Serial.print(Cwt);
      Serial.print(F(","));

    //-------------Wechselrichter-Strom---------------
      int reading2 = analogRead(4);
      Cc = (((analogRead(4)-120)/(15.8))*(100.00/3))/1000;
      Serial.print(Cc);
      Serial.print(F(","));

    //-------------Cg laut Code EmonKT / Netzteil-Strom (Cnt) laut BA von Cansin (bitte überprüfen)---------------
      int reading3 = analogRead(5);
    // -126 as it is the channels offset (OPAmp nonlinearity); devide by (15.8) as it is the amplifying factor of the OPAmp circuit; *(10/300) as 300mV=10A 
      Cg = (((analogRead(5)-103.0)/(15.8))*(100.00/3))/1000;
      Serial.print(Cg);
      Serial.print(F(","));

    //-------------Cbp Baterie positiv [A]---------------
      int reading4 = analogRead(7);
    // -92.5 as it is the channels offset (OPAmp nonlinearity); devide by (15.8) as it is the amplifying factor of the OPAmp circuit; *0.995 as amplifying correction; *(25/300) as 300mV=25A 
      Cbp = (((analogRead(7)-124)/(15.8))*(250.00/3))/1000;
      Serial.print(Cbp);
      Serial.print(F(","));

    //-------------Cbn Baterie negativ [A]---------------
      int reading5 = analogRead(8);
    // -96 as it is the channels offset (OPAmp nonlinearity); devide by (15.8) as it is the amplifying factor of the OPAmp circuit; *(25/300) as 300mV=25A 
      Cbn = (((analogRead(8)-122)/(15.8))*(250.00/3))/1000; 
      Serial.print(Cbn);
      Serial.print(F(","));

    //-------------Windgeschwindigkeit---------------
      int reading6 = analogRead(9);
    // Im=(Um/Rs); 
    // float Im = ((a+3.85)/240);
    // Im lowest reference is 4mA, for calculations this is substracted, so that 0m/s = 0mA
    //float Ih = (Im-4);
      float Sw= 11.456*analogRead(9)/1000-10.516;
      Serial.print(Sw);
      Serial.print(F(","));

    //-------------Dw - Windrichtung---------------
      int reading7 = analogRead(10);
      float Im = 94.117*analogRead(10)/1000-89.889;  
      Im=Im*(16/360);
    if (Im>17){
        
        Im = 1;
        
      }
        int Ia = (int) Im;
      Dw= (float) Ia; 
      Serial.print(Dw);
      Serial.print(F(","));

    //-------------Is - Sonneneinstrahlung---------------
      int reading8 = analogRead(11);
    // *5 as 1mV=5W/m²
      float Is = 5.501*(analogRead(11));
      Serial.print(Is);
      Serial.print(F(","));

    //-------------Ta (Außentemp) laut BA von Cansin / Laut .txt-Datei Pinbelegung ist Tb (bitte überprüfen)---------------
      int reading9 = analogRead(12);
    // devide by 10 as 10mV=1°C; -55 as the sensors starts at -55°C
      float Ta = (analogRead(12)*109.305/1000)-56.3;
      Serial.print(Ta);
      Serial.print(F(","));

    //-------------Tb (Batterietemp) Laut BA von Cansin / Laut .txt-Datei Pinbelegung ist Ta (bitte überprüfen)---------------
      int reading10 = analogRead(13);
    // devide by 10 as 10mV=1°C; -55 as the sensors starts at -55°C
      float Tb = (analogRead(13)*103.534/1000)-53.108;
      Serial.print(Tb);
      Serial.print(F(","));

    //-------------Vb - Spannung Batterie ---------------
      int reading11 = analogRead(14);
    // Vb=Um*((R2+R3)/R3), devide by 1000 for V
      Vb = (analogRead(14)*(118.2/18.2))/1000+0.001;
      Serial.print(Vb);
      Serial.print(F(">"));
      Serial.println();
  }
}
  //delay (10000);
