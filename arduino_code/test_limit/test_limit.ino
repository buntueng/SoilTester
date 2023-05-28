const int x_loadcell_pin = A13;
const int y_loadcell_pin = A10;

const int x_motor_dir1 = 7;
const int x_motor_dir2 = 5;
const int x_motor_speed_pin = 3;

const int y_motor_dir1 = 6;
const int y_motor_dir2 = 4;
const int y_motor_speed_pin = 2;

// limit switches
const int x_limit_front = 18;
const int x_limit_back = 16;
const int y_limit_top = 26;
const int y_limit_bottom = 20;

// x move button
const int x_forward_pin = 11;
const int x_backward_pin = 40;
const int y_up_pin =10;
const int y_down_pin =12;

// command from pc
bool execute_cmd = false;
String cmd_string = "";

int loadcell_interval_time = 20;
unsigned long loadcell_timer = 0;

bool run_machine = false;

//=======================================================
bool x_backward_logic = 0;
bool x_forward_logic = 0;
bool y_down_logic = 0;
bool y_up_logic = 0;

unsigned char x_backward_state = 0xFF;
unsigned char x_forward_state = 0xFF;
unsigned char y_down_state = 0xFF;
unsigned char y_up_state = 0xFF;
//=======================================================

void setup()
{
    Serial.begin(115200);
    //============ setup motor pin ================
    pinMode(x_motor_dir1,OUTPUT);
    pinMode(x_motor_dir2,OUTPUT);
    pinMode(x_motor_speed_pin,OUTPUT);

    pinMode(y_motor_dir1,OUTPUT);
    pinMode(y_motor_dir2,OUTPUT);
    pinMode(y_motor_speed_pin,OUTPUT);

    pinMode(x_limit_front,INPUT_PULLUP);
    pinMode(x_limit_back,INPUT_PULLUP);

    pinMode(x_forward_pin,INPUT_PULLUP);
    pinMode(x_backward_pin,INPUT_PULLUP);

    pinMode(y_up_pin,INPUT_PULLUP);
    pinMode(y_down_pin,INPUT_PULLUP);
    pinMode(y_limit_top,INPUT_PULLUP);
    pinMode(y_limit_bottom,INPUT_PULLUP);

    pinMode(x_loadcell_pin,INPUT);
    pinMode(y_loadcell_pin,INPUT);

    // stop all motors
    digitalWrite(x_motor_dir1,0);
    digitalWrite(x_motor_dir2,0);
    digitalWrite(x_motor_speed_pin,0);

    digitalWrite(y_motor_dir1,0);
    digitalWrite(y_motor_dir2,0);
    digitalWrite(y_motor_speed_pin,0);
}

void loop()
{
  // read all button logic
  // Serial.print(digitalRead(x_forward_pin));
  // Serial.print((","));
  // Serial.print(digitalRead(x_backward_pin));
  // Serial.print((","));
  // Serial.print(digitalRead(y_up_pin));
  // Serial.print((","));
  // Serial.println(digitalRead(y_down_pin));

  x_backward_state = ((x_backward_state << 1) + digitalRead(x_backward_pin)) & 0xFF;
  // Serial.println(x_backward_state);
  if(x_backward_state == 0xFC)
  {
    x_backward_logic = 1;
  }
  else if(x_backward_state == 0x3F)
  {
    x_backward_logic = 0;
  }

  x_forward_state = ((x_forward_state << 1) + digitalRead(x_forward_pin)) & 0xFF;
  if(x_forward_state == 0xFC)
  {
    x_forward_logic = 1;
  }
  else if(x_forward_state == 0x3F)
  {
    x_forward_logic = 0;
  }

  y_up_state = ((y_up_state << 1) + digitalRead(y_up_pin)) & 0xFF;
  if(y_up_state == 0xFC)
  {
    y_up_logic = 1;
  }
  else if(y_up_state == 0x3F)
  {
    y_up_logic = 0;
  }

  y_down_state = ((y_down_state << 1) + digitalRead(y_down_pin)) & 0xFF;
  if(y_down_state == 0xFC)
  {
    y_down_logic = 1;
  }
  else if(y_down_state == 0x3F)
  {
    y_down_logic = 0;
  }


  if(Serial.available())
  {
    char input_char = Serial.read();
    if(input_char=='\n')
    {  
      execute_cmd = true;
    }
    else
    {
      cmd_string.concat(input_char);
    }
  }

  if(execute_cmd)
  {
    switch(cmd_string[0])
    {
      case 'r':
      {
        switch(cmd_string[1])
        {
          case '0':
          {
            run_machine = false;
            break;
          }
          case '1':
          {
            run_machine = true;
            break;
          }
              case '2':
              {
                break;
              }
              case '3':
              {
                break;
              }
              case '4':
              {
                break;
              }
            }
            break;
          }
          case 'L':
          {
            break;
          }
          default:
            {
                break;
            }
        }
        execute_cmd = false;
        cmd_string = "";
  }

  // ============== run machine here ==========================
  if(run_machine)
  {
    
  }
  else
  {
    Serial.print(x_forward_logic);
    Serial.print(",");
    Serial.print(x_backward_logic);
    Serial.print(",");
    Serial.print(y_up_logic);
    Serial.print(",");
    Serial.println(y_down_logic);

      // if((digitalRead(x_forward_pin)==0)&&(digitalRead(x_limit_front)==0))
      //   {
      //       digitalWrite(x_motor_dir1,HIGH);
      //       digitalWrite(x_motor_dir2,LOW);
      //       analogWrite(x_motor_speed_pin,50);
      //   }
      //   else if ((digitalRead(x_backward_pin)==0)&&(digitalRead(x_limit_back)==0))
      //   {
      //       digitalWrite(x_motor_dir1,LOW);
      //       digitalWrite(x_motor_dir2,HIGH);
      //       analogWrite(x_motor_speed_pin,50);
      //   }
      //   else
      //   {
      //       digitalWrite(x_motor_dir1,LOW);
      //       digitalWrite(x_motor_dir2,LOW);
      //       analogWrite(x_motor_speed_pin,0);
      //   }
      //   // ======= switch control yaxis =============
      //   if((digitalRead(y_up_pin)==0)&&(digitalRead(y_limit_top)==0))
      //   {
      //       digitalWrite(y_motor_dir1,HIGH);
      //       digitalWrite(y_motor_dir2,LOW);
      //       analogWrite(y_motor_speed_pin,150);
      //   }
      //   else if ((digitalRead(y_down_pin)==0)&&(digitalRead(y_limit_bottom)==0))
      //   {
      //       digitalWrite(y_motor_dir1,LOW);
      //       digitalWrite(y_motor_dir2,HIGH);
      //       analogWrite(y_motor_speed_pin,150);
      //   }
      //   else
      //   {
      //       digitalWrite(y_motor_dir1,LOW);
      //       digitalWrite(y_motor_dir2,LOW);
      //       analogWrite(y_motor_speed_pin,0);
      //   }
  }    
}
