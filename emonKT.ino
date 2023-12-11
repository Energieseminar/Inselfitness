#include <SPI.h>
#include <Ethernet.h>
#include <JeeLib.h>
#include <avr/wdt.h>
#include <TimeLib.h>

#define RF69_COMPAT 0                                                       //Set to 1 if using RFM69CW or 0 is using RFM12B
#define myNodeID 15                                                         //node ID of tx (range 0-30)
#define network 210                                                         //network group (can be in the range 1-250).
#define RF_freq RF12_433MHZ                                                 //Freq of RF12B can be RF12_433MHZ, RF12_868MHZ or RF12_915MHZ. Match freq to module

// Connection Config
//------------------------------------------------------------------------------------------------------

boolean ETHERNET = true;                  
boolean RADIO = false;

// esem:      dd66850a85ba2373bc8e59f504af3110
// cloudhall: 40ef78aca78007a9517d86b13c0b30b1

char APIkey [] = "40ef78aca78007a9517d86b13c0b30b1";                        // Enter your API key found on your emoncms account here
char server[] = "emoncms.cloudhall.de";						
char subdir[] = "";                                		    // if you want to connect via IP, change this line to: byte server[] = { xx, xxx, xxx, xx };
byte mac[] = { 0x00, 0xAB, 0xBB, 0xCC, 0xDE, 0x02 };                        // OKG MAC - experiment with different MAC addresses if you have trouble connecting 
byte ip[] = {130, 149, 26, 149 };                                          // OKG static IP - only used if DHCP failes

//------------------------------------------------------------------------------------------------------

// Sampling Config
//------------------------------------------------------------------------------------------------------

char* channels5V[] = 
{"Cpv","Cwt","Cc","Cg","Trash","Cbp","Cbn","Sw","Dw","Vb"};      	// Enable additional samplingchannel by adding <,"NAME"> syntax within 										// the brackets.  
char* channels1V1[] = {"Is","Ta","Tb"};					// Enable channels with a resolution of 1.1/1023mV 				 
                                                                                                                                      
const int numReadings = 10;                                                 // amount of samples used for smoothing

//------------------------------------------------------------------------------------------------------

// Calibration/Calculation Config
//------------------------------------------------------------------------------------------------------

typedef float (*oneargfunc) (float a);                                       //  in the swifted brackets you can do your needed calculations/calibrations, a is measured value in mV

float cal0(float a){
  // -105 as it is the channels offset (OPAmp nonlinearity); devide by (15.8) as it is the amplifying factor of the OPAmp circuit; *(10/300) as 300mV=10A 
  float Cpv = (((a-105)/(15.8))*(100.00/3))/1000;
   return Cpv;
  }

float cal1(float a){

  float Cwt = (((a-119)/(15.8))*(200.00/3))/1000;
  
  return Cwt;
  
}

float cal2(float a){

  float Cc = (((a-120)/(15.8))*(100.00/3))/1000;
  
  return Cc;
  
}

float cal3(float a){

  // -126 as it is the channels offset (OPAmp nonlinearity); devide by (15.8) as it is the amplifying factor of the OPAmp circuit; *(10/300) as 300mV=10A 
  float Cg = (((a-103.0)/(15.8))*(100.00/3))/1000;
  
  return Cg;
  
}

float cal4(float a){return a;}

float cal5(float a){

  // -92.5 as it is the channels offset (OPAmp nonlinearity); devide by (15.8) as it is the amplifying factor of the OPAmp circuit; *0.995 as amplifying correction; *(25/300) as 300mV=25A 
  float Cbp = (((a-124)/(15.8))*(250.00/3))/1000;
  
  return Cbp;
  
}

float cal6(float a){

   // -96 as it is the channels offset (OPAmp nonlinearity); devide by (15.8) as it is the amplifying factor of the OPAmp circuit; *(25/300) as 300mV=25A 
  float Cbn = (((a-122)/(15.8))*(250.00/3))/1000;
  
  return Cbn;
  
}

float cal7(float a){

  // Im=(Um/Rs); 
 // float Im = ((a+3.85)/240);
  // Im lowest reference is 4mA, for calculations this is substracted, so that 0m/s = 0mA
  //float Ih = (Im-4);
  float Sw= 11.456*a/1000-10.516;
  
  return Sw;
  
}
                                            
float cal8(float a){  
/*
  // Im=Um/Rs
  float Im = (a/240);
  // preparing Ih for variabletype change so that values from (x-1).5 to x.5 equal x, starting with x=1
  float Ih = Im-3+0.6;
  // the last possible sector is the same as the first, as only 16 [N(1)-NNO(16)] are used in emonCMS
  if (Ih>17){
    
    Ih = 1;
    
  }
  // change from float to int, what cuts of the decimals
  int Ii = (int) Ih;
  //change back to float so we meet the required return-variable-type
  float Dw = (float) Ii;  
  
  return Dw;
  */

float Im = 94.117*a/1000-89.889;  
  Im=Im*(16/360);
 if (Im>17){
    
    Im = 1;
    
  }
    int Ia = (int) Im;
   float Dw= (float) Ia;
  return Dw;

}

float cal9(float a){

  // Vb=Um*((R2+R3)/R3), devide by 1000 for V
  float Vb = (a*(118.2/18.2))/1000+0.001;               
  
  return Vb;
  
}


float cal10(float a){
  
  // *5 as 1mV=5W/m²
  float Is = 5.501*(a);

  return Is;
  
}  



float cal11(float a){
  
  // devide by 10 as 10mV=1°C; -55 as the sensors starts at -55°C
  float Ta = (a*109.305/1000)-56.3;

  return Ta;
}
 
                                                  
float cal12(float a){

  
   // devide by 10 as 10mV=1°C; -55 as the sensors starts at -55°C
  float Tb = (a*103.534/1000)-53.108;

  return Tb;
  
}



float cal13(float a){return a;}

float cal14(float a){return a;}

float cal15(float a){return a;}

oneargfunc calFunctions[] = {                                          

cal0,
cal1,
cal2, 
cal3, 
cal4, 
cal5, 
cal6, 
cal7,
cal8, 
cal9, 
cal10, 
cal11, 
cal12, 
cal13,
  
};

//------------------------------------------------------------------------------------------------------

// Ethernet Config
//------------------------------------------------------------------------------------------------------

EthernetClient client;
const int WizResetPin = 7;                                                  // wired to the Wiznet reset line

//------------------------------------------------------------------------------------------------------

// Open Kontrol Gateway Config
//------------------------------------------------------------------------------------------------------

const int LEDPin = 17;                                                       // front status LED on OKG

//------------------------------------------------------------------------------------------------------

// Variables
//------------------------------------------------------------------------------------------------------

const int dataLED = 13;

const int radioLED = 6;

boolean lastConnected = false;

unsigned long previousMillis = 0, time60s;

char line_buf[50];                                                          // Used to store line of http reply header

const int numChan5V = sizeof(channels5V)/sizeof(char*);                         // calculation of the amount of channels to be sampled
const int numChan1V1 = sizeof(channels1V1)/sizeof(char*);
const int numChan = numChan5V + numChan1V1;

//------------------------------------------------------------------------------------------------------

// Defintion of the data struct
//------------------------------------------------------------------------------------------------------

  typedef struct {

     String       dec[numChan];    
     int          chan[numChan];   
     float        val[numChan];
     oneargfunc   cal[numChan];
         
  } data;
  
  data insula;                                                                // decleration of the data struct: insula

//------------------------------------------------------------------------------------------------------

// Defintion of the data struct for Radiotransmission
//------------------------------------------------------------------------------------------------------

  typedef struct {float val[numChan];} Payload;
  
  Payload emonKT;                                                                // decleration of the Payload struct: emonKT

//------------------------------------------------------------------------------------------------------


// The PacketBuffer class is used to generate the json string that is send via ethernet - JeeLabs
//------------------------------------------------------------------------------------------------------

class PacketBuffer : public Print {
public:
    PacketBuffer () : fill (0) {}
    const char* buffer() { return buf; }
    byte length() { return fill; }
    void reset()
    { 
      memset(buf,NULL,sizeof(buf));
      fill = 0; 
    }
    virtual size_t write (uint8_t ch)
        { if (fill < sizeof buf) buf[fill++] = ch; }
    byte fill;
    char buf[150];
    private:
};

PacketBuffer str;

//------------------------------------------------------------------------------------------------------

void setup() {

  Serial.begin(9600);

// Ethernet Initialisation 
//------------------------------------------------------------------------------------------------------

  if (ETHERNET){
    
    Serial.println("InselsystemKT > OKG > Wiznet > emoncms");  
     
    pinMode(LEDPin, OUTPUT);
    digitalWrite(LEDPin,HIGH);
  
    pinMode(WizResetPin, OUTPUT);                                               // Reset the Wiznet module
    digitalWrite(WizResetPin, LOW);                
    delay(5);
    digitalWrite(WizResetPin, HIGH);
    
    
    if (Ethernet.begin(mac) == 0) {
      
      Serial.println
      ("Failed to configure Ethernet using DHCP");
      Ethernet.begin(mac, ip);                                                  //configure manually 
      
    }
    
    Serial.print("Local IP address: ");                                         // print your local IP address
    
    for (byte thisByte = 0; thisByte < 4; thisByte++) {                         // print the value of each byte of the IP address
      
      Serial.print(Ethernet.localIP()[thisByte], DEC);     
      Serial.print(".");
       
    }
    
    Serial.println();

  }

//------------------------------------------------------------------------------------------------------

// RFM Module Initialisation 
//------------------------------------------------------------------------------------------------------

  if (RADIO){

    rf12_initialize(myNodeID,RF_freq,network);                                  //Initialize RFM12 with settings defined above 
        
    Serial.println("InselystemKT > RFM12B > emonBase > emoncms");

    Serial.print("Node: "); 
    Serial.print(myNodeID); 
    Serial.print(" Freq: "); 
    if (RF_freq == RF12_433MHZ) Serial.print("433Mhz");
    if (RF_freq == RF12_868MHZ) Serial.print("868Mhz");
    if (RF_freq == RF12_915MHZ) Serial.print("915Mhz"); 
    Serial.print(" Network: "); 
    Serial.println(network);
  
    pinMode(radioLED, OUTPUT);    
        
  }

  for (int i = 0; i <= numChan5V-1; i++) {
    
    insula.dec[i] = channels5V[i];
    insula.chan[i] = i+2;
    insula.val[i] = 0;
    insula.cal[i] = calFunctions[i];
    
  }

  for (int i = numChan5V; i <= numChan-1; i++) {
    
    insula.dec[i] = channels1V1[i-numChan5V];
    insula.chan[i] = i+2;
    insula.val[i] = 0;
    insula.cal[i] = calFunctions[i];
    
  }

  delay(200);
  digitalWrite(LEDPin,LOW);                                                   // turn of OKG status LED to indicate setup success 
                                                                                
  wdt_enable(WDTO_8S);                                                        // enable an 8's reset watchdog
      
}

//---------------------------------------------------------------------------------------------------

void loop() {

  if (numChan > 14){
    
    Serial.println("Too many channels enabled, reduce them to max 16 by deleting some in the Sampling Config of your sourcecode!");
    
  }

  else{
    
    unsigned long timecode = now();
    float newVal = 0;
    float sum;   
  
    digitalWrite(dataLED, HIGH);
    
    for (int i = 0; i <= numChan-1; i++){

      sum = 0; 

      if(i > numChan5V-1){
	
	      analogReference(INTERNAL1V1);

      	for (int n = 0; n <= numReadings-1; n++){            
      
       	  float trash = analogRead(A0);       
                  
          delayMicroseconds(10);
          
      	}        
      
        
        for (int n = 0; n <= numReadings-1; n++){                           
        
          newVal = analogRead(insula.chan[i]);
          sum = sum + newVal ;
                    
          delay(10);
            
        }     

        insula.val[i] = insula.cal[i]((sum/numReadings)*(1089.2 / 1024));
	      emonKT.val[i] = insula.val[i];

        Serial.print(insula.dec[i]); 
        Serial.print(" (A"); 
        Serial.print(insula.chan[i]); 
        Serial.print(" | 1V1)     =   ");        
        Serial.println(insula.val[i]);  
 

        if(i == (numChan-1)){
          
          analogReference(DEFAULT);      
    
          for (int n = 0; n <= numReadings-1; n++){            
      
            float trash = analogRead(insula.chan[A0]);       
                  
           delayMicroseconds(10);
          
          }

        }
	
      }

      else{
	
        for (int n = 0; n <= numReadings-1; n++){                  
      
          newVal = analogRead(insula.chan[i]);
          sum = sum + newVal ;
                  
          delay(1);
          
        }
        
        insula.val[i] = insula.cal[i]((sum/numReadings)*(4998.1/1024));     
        emonKT.val[i] = insula.val[i];

	      Serial.print(insula.dec[i]); 
        Serial.print(" (A"); 
        Serial.print(insula.chan[i]); 
        Serial.print(" | 5V)     =   ");        
        Serial.println(insula.val[i]);     
  
      }

    }

    Serial.println();	       
    Serial.println();
  
    digitalWrite(dataLED, LOW);
        

    if(ETHERNET){

      rf12_sleep(0);

//---------------------------------------------------------------------------------------------------
  
     if (client.available()){
      
      memset(line_buf,NULL,sizeof(line_buf));
      int pos = 0;
      
      while (client.available()) {
        
        char c = client.read();
        line_buf[pos] = c;
        pos++;
        
      }  
  
      if (strcmp(line_buf,"ok")==0){
        
        Serial.println("OK recieved");
        
      }
      
      else if(line_buf[0]=='t'){
         
        Serial.print("Time: ");
        Serial.println(line_buf);
      
        char tmp[] = {line_buf[1],line_buf[2],0};
        byte hour = atoi(tmp);
        tmp[0] = line_buf[4]; tmp[1] = line_buf[5];
        byte minute = atoi(tmp);
        tmp[0] = line_buf[7]; tmp[1] = line_buf[8];
        byte second = atoi(tmp);
        
       }
       
      }
    
      if (!client.connected() && lastConnected){
      
      Serial.println();
      Serial.println("disconnecting.");
      client.stop();
      
    }
    
// Packing the Json String
//-------------------------------------------------------------------------------------------------------

    str.reset();
    str.print("{");
  
    for (int i = 0; i <= numChan-1; i++) {      
      
      str.print(insula.dec[i]);  
      str.print(":");
      str.print(insula.val[i]);
  
      if (i<numChan-1){
  
        str.print(",");
        
      }        
          
    }    
  
// Post Data
//-----------------------------------------------------------------------------------------------------------------
    
    if (!client.connected()){
      
      if (client.connect(server, 80)){
  
        digitalWrite(LEDPin,HIGH);
        
        str.print("}\0");
                
        Serial.println();
        Serial.print("Sent: "); Serial.println(str.buf);
        
        client.print("GET "); 
        client.print("http://");
        client.print(server);
	      client.print(subdir);
        client.print("/input/post.json?apikey=");
        client.print(APIkey); 
        client.print("&json=");
        client.print(str.buf);
        client.print("&time=");
        client.print(timecode); 
        client.print("&node="); 
        client.print(myNodeID); 
        client.println();
      
        delay(300);
  
        digitalWrite(LEDPin,LOW);
	client.stop();
        
      } 
      
      else {Serial.println("Cant connect to send data"); delay(500); client.stop();}
      
    }
  
    if (!client.connected() && ((millis()-time60s)>10000)){
      
      time60s = millis();                                                       // reset lastRF timer
                                                                                
      if (client.connect(server, 80)){
        
        Serial.println();
        Serial.println("Sent time request");
        
        client.print("GET "); 
        client.print("http://");
        client.print(server);
        client.print("/time/local.json?apikey="); 
        client.print(APIkey); 
        client.println();
        
      }
      
      else {Serial.println("Cant connect to req time"); delay(500); client.stop();}
  
    }
  
    lastConnected = client.connected();
  
    wdt_reset();     
    
//----------------------------------------------------------------------------------------------------------------
    
    rf12_sleep(-1);
    
   }   

// Post Data via RFModule
//----------------------------------------------------------------------------------------------------------------
  
  if (RADIO){

    digitalWrite(radioLED, HIGH);

    rf12_sendNow(0, &emonKT, sizeof emonKT);                    
    rf12_sendWait(2);

    delay(500);

    digitalWrite(radioLED, LOW);
    
  }   

//----------------------------------------------------------------------------------------------------------------

 }
 
}


