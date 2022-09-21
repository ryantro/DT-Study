// global variabls
String incomingStr;
const byte numChars = 32;
char receivedChars[numChars];
boolean newData = false;
boolean isMoving = false;

// inital setup
void setup() {
  pinMode(1,OUTPUT);  
  pinMode(2,OUTPUT); 
  pinMode(3,OUTPUT);  
  pinMode(4,OUTPUT); 
  pinMode(5,OUTPUT);  
  pinMode(6,OUTPUT);  
  Serial.begin(9600);
}
// main loop
void loop() {
    recvWithStartEndMarkers();
    showNewData();
}
// read serial
void recvWithStartEndMarkers() {
    static boolean recvInProgress = false;
    static byte ndx = 0;
    char startMarker = '<';
    char endMarker = '>';
    char rc;
 
    while (Serial.available() > 0 && newData == false) {
        rc = Serial.read();
        if (recvInProgress == true) {
            if (rc != endMarker) {
                receivedChars[ndx] = rc;
                ndx++;
                if (ndx >= numChars) {
                    ndx = numChars - 1;
                }
            }
            else {
                receivedChars[ndx] = '\0'; // terminate the string
                recvInProgress = false;
                ndx = 0;
                newData = true;
            }
        }
        else if (rc == startMarker) {
            recvInProgress = true;
        }
    }
}
// 
void showNewData() {
    if (newData == true) {
        parseStr(receivedChars); 
        newData = false;
    }
}
// parse the serial command
void parseStr(String command){
  int r = command.toInt();
  if(r == 0) setAllOpen();
  else setRelays(command.toInt());
}
// set a specific relay to open to power a single emitter
void setRelays(int r){
  for(int i = 1; i <= 6; i++){
    if(i == r){
      digitalWrite(i,LOW);
      Serial.println(i);
    } else {
      digitalWrite(i,HIGH);
    }
  }
}
// set all relays to open to turn on an entire hexel
void setAllOpen(){
  for(int i = 1; i <= 6; i++){
    digitalWrite(i,LOW);
  }
}
