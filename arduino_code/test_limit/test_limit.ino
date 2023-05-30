void scan_input_switches();
void scan_limit_switches();
void manual_control();

const int x_loadcell_pin = A13;
const int y_loadcell_pin = A10;

const int x_motor_dir1 = 7;
const int x_motor_dir2 = 5;
const int x_motor_speed_pin = 3;

const int y_motor_dir1 = 6;
const int y_motor_dir2 = 4;
const int y_motor_speed_pin = 2;

// limit switches
const int x_limit_front_pin = 28;
const int x_limit_back_pin = 30;
const int y_limit_top_pin = 26;
const int y_limit_bottom_pin = 24;

// x move button
const int x_forward_pin = 38;
const int x_backward_pin = 32;
const int y_up_pin =34;
const int y_down_pin =36;

// command from pc
bool execute_cmd = false;
String cmd_string = "";

int loadcell_interval_time = 20;
unsigned long loadcell_timer = 0;

bool run_machine = false;

//================= switch control inputs ==================
bool x_backward_logic = 0;
bool x_forward_logic = 0;
bool y_down_logic = 0;
bool y_up_logic = 0;

unsigned char x_backward_state = 0xFF;
unsigned char x_forward_state = 0xFF;
unsigned char y_down_state = 0xFF;
unsigned char y_up_state = 0xFF;

// ================= limit switch ======================
bool x_limit_front_logic = 0;
bool x_limit_back_logic = 0;
bool y_limit_top_logic = 0;
bool y_limit_bottom_logic = 0;

unsigned char x_limit_front_state = 0xFF;
unsigned char x_limit_back_state = 0xFF;
unsigned char y_limit_top_state = 0xFF;
unsigned char y_limit_bottom_state = 0xFF;
//=================== SET ZERO ============================
int set_zero_x_state = 0;
int set_zero_y_state = 0;
bool set_zero_start = false;
bool set_zero_x_success = false;
bool set_zero_y_success = false;
//=======================================================
int select_exp = 0;

bool set_zero_flag = false;
unsigned int set_zero_state = 0;


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

    pinMode(x_limit_front_pin,INPUT_PULLUP);
    pinMode(x_limit_back_pin,INPUT_PULLUP);

    pinMode(x_forward_pin,INPUT_PULLUP);
    pinMode(x_backward_pin,INPUT_PULLUP);

    pinMode(y_up_pin,INPUT_PULLUP);
    pinMode(y_down_pin,INPUT_PULLUP);
    pinMode(y_limit_top_pin,INPUT_PULLUP);
    pinMode(y_limit_bottom_pin,INPUT_PULLUP);

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
  scan_input_switches();
  scan_limit_switches();
  //////////////////// =====================================================================================

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
        Serial.print(x_limit_front_logic);
        Serial.print(",");
        Serial.print(x_limit_back_logic);
        Serial.print(",");
        Serial.print(y_limit_top_logic);
        Serial.print(",");
        Serial.println(y_limit_bottom_logic);
        break;
      }
      case 'Z':
      {
        Serial.println("SET ZERO");
        set_zero_flag = true;
        set_zero_state = 0;
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
    switch (select_exp) 
    {
      case 1:
      {

        break;
      }
      default:
      {
        break;
      }
      break;
    }
  }
  else
  {
    if(set_zero_flag)
    {
      set_zero();
    }
    else
    {
      manual_control();
    }    
  }
}


void manual_control()
{
  if(((x_forward_logic) == 1) && ((x_limit_front_logic)==0))
    {
            // Serial.println("X_forward");
            digitalWrite(x_motor_dir1,HIGH);
            digitalWrite(x_motor_dir2,LOW);
            analogWrite(x_motor_speed_pin,150);      
    }
    else if (((x_backward_logic)==1) && ((x_limit_back_logic)==0)) 
    {
            // Serial.println("X_backward");
            digitalWrite(x_motor_dir1,LOW);
            digitalWrite(x_motor_dir2,HIGH);
            analogWrite(x_motor_speed_pin,150);
    }
    else
    {
            // Serial.println("x stop");
            digitalWrite(x_motor_dir1,LOW);
            digitalWrite(x_motor_dir2,LOW);
            analogWrite(x_motor_speed_pin,0);
    }
    if (((y_up_logic)==1)&&((y_limit_top_logic)==0))
    {
            // Serial.println("Y_up");
            digitalWrite(y_motor_dir1,HIGH);
            digitalWrite(y_motor_dir2,LOW);
            analogWrite(y_motor_speed_pin,150);    
    }
    else if(((y_down_logic)==1)&&((y_limit_bottom_logic)==0))
    {
            // Serial.println("Y_down");
            digitalWrite(y_motor_dir1,LOW);
            digitalWrite(y_motor_dir2,HIGH);
            analogWrite(y_motor_speed_pin,150);
    }
    else
    {
        // Serial.println("y stop");
        digitalWrite(y_motor_dir1,LOW);
        digitalWrite(y_motor_dir2,LOW);
        analogWrite(y_motor_speed_pin,0);
    }
}

void set_zero()
{
  switch (set_zero_state)
  {
    case 0:
    {
      digitalWrite(y_motor_dir1,LOW);
      digitalWrite(y_motor_dir2,LOW);
      analogWrite(y_motor_speed_pin,0);

      digitalWrite(x_motor_dir1,LOW);
      digitalWrite(x_motor_dir2,LOW);
      analogWrite(x_motor_speed_pin,0); 
      // x_limit_back_logic = 0;
      // y_limit_top_logic = 0;
      set_zero_state = 1;
      break;
    }
    case 1:
    {
      if(y_limit_top_logic == 1)
      {
        set_zero_state = 3;
      }
      else
      {
        set_zero_state = 2;
        digitalWrite(y_motor_dir1,HIGH);
        digitalWrite(y_motor_dir2,LOW);
        analogWrite(y_motor_speed_pin,150);
      }
      break;
    } 
    case 2:
    {
      if(y_limit_top_logic == 1)
      {
        set_zero_state = 3;
        digitalWrite(y_motor_dir1,LOW);
        digitalWrite(y_motor_dir2,LOW);
        analogWrite(y_motor_speed_pin,0);
      }
      break;
    }
    case 3:
    {   
      set_zero_state = 4;
      digitalWrite(y_motor_dir1,LOW);
      digitalWrite(y_motor_dir2,LOW);
      analogWrite(y_motor_speed_pin,0);
      break;
    }
    case 4:
    {
      if((x_limit_back_logic) == 1)
      {
        digitalWrite(x_motor_dir1,LOW);
        digitalWrite(x_motor_dir2,LOW);
        analogWrite(x_motor_speed_pin,0);
        set_zero_state = 7;
      }
      else
      {
        set_zero_state = 5;
        digitalWrite(x_motor_dir1,LOW);
        digitalWrite(x_motor_dir2,HIGH);
        analogWrite(x_motor_speed_pin,150);
      }
      break;
    }   
    case 5:
    {
      if((x_limit_back_logic) == 1)
        {
          set_zero_state = 6;
          digitalWrite(x_motor_dir1,LOW);
          digitalWrite(x_motor_dir2,LOW);
          analogWrite(x_motor_speed_pin,0);
        }
        break;
    }
    case 6:
    {
      set_zero_state = 7;
      digitalWrite(x_motor_dir1,LOW);
      digitalWrite(x_motor_dir2,LOW);
      analogWrite(x_motor_speed_pin,0);
      break;
    }
    case 7:
    {
      Serial.println("Zero complete");
      set_zero_flag = false;
      break;
    }
    default:
    {
      break;
    }
  }
}


void exp1()
{
  
}

// ====================== sub program ===============================
void scan_input_switches()
{
  x_backward_state = ((x_backward_state << 1) + digitalRead(x_backward_pin)) & 0xFF;
  if(x_backward_state == 0xFE)
  {
    x_backward_logic = 1;
  }
  else if(x_backward_state == 0x7F)
  {
    x_backward_logic = 0;
  }

  x_forward_state = ((x_forward_state << 1) + digitalRead(x_forward_pin)) & 0xFF;
  if(x_forward_state == 0xFE)
  {
    x_forward_logic = 1;
  }
  else if(x_forward_state == 0x7F)
  {
    x_forward_logic = 0;
  }

  y_up_state = ((y_up_state << 1) + digitalRead(y_up_pin)) & 0xFF;
  if(y_up_state == 0xFE)
  {
    y_up_logic = 1;
  }
  else if(y_up_state == 0x7F)
  {
    y_up_logic = 0;
  }

  y_down_state = ((y_down_state << 1) + digitalRead(y_down_pin)) & 0xFF;
  if(y_down_state == 0xFE)
  {
    y_down_logic = 1;
  }
  else if(y_down_state == 0x7F)
  {
    y_down_logic = 0;
  }
}

void scan_limit_switches()
{
  // x_limit_front_logic = digitalRead(x_limit_front_pin);
  // x_limit_back_logic = digitalRead(x_limit_back_pin);
  // y_limit_top_logic = digitalRead(y_limit_top_pin);
  // y_limit_bottom_logic = digitalRead(y_limit_bottom_pin);
  // ============================== push = 0 ========================
  x_limit_front_state = ((x_limit_front_state << 1) + digitalRead(x_limit_front_pin)) & 0x03;
  if(x_limit_front_state == 0x03)
  {
    x_limit_front_logic = 1;
  }
  else if(x_limit_front_state == 0x00)
  {
    x_limit_front_logic = 0;
  }

  x_limit_back_state = ((x_limit_back_state << 1) + digitalRead(x_limit_back_pin)) & 0x03;
  if(x_limit_back_state == 0x03)
  {
    x_limit_back_logic = 1;
  }
  else if(x_limit_back_state == 0x00)
  {
    x_limit_back_logic = 0;
  }

  y_limit_top_state = ((y_limit_top_state << 1) + digitalRead(y_limit_top_pin)) & 0x03;
  if(y_limit_top_state == 0x03)
  {
    y_limit_top_logic = 1;
  }
  else if(y_limit_top_state == 0x3F)
  {
    y_limit_top_logic = 0;
  }

  y_limit_bottom_state = ((y_limit_bottom_state << 1) + digitalRead(y_limit_bottom_pin)) & 0x03;
  if(y_limit_bottom_state == 0x03)
  {
    y_limit_bottom_logic = 1;
  }
  else if(y_limit_bottom_state == 0x00)
  {
    y_limit_bottom_logic = 0;
  }


}