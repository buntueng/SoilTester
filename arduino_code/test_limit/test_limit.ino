void scan_input_switches();
void scan_limit_switches();
void set_zero();
void manual_control();
void exp1();
void exp2();

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

// ==================== SET PARAM ======================
int update_pwm = 0;
int start_force = 0;
int stop_force = 0;
int cyclic = 0;
int fixed_vertical_force = 0;
const int loadcell_guard_band = 2; 
unsigned long start_timer = 0;
unsigned long timemer_send_data = 0;
unsigned int timmer_trig = 50;
//====================== EXP 1 PARAM ========================
int exp1_x_state = 0;
int exp1_y_state = 0;
int exp1_send_force_state = 0;
bool exp1_y_set = false;
bool exp1_x_state_start = false; 
bool exp1_test_success =false;
bool exp1_start_y = false;
int y_stabilizer_pwm = 35;
//======================= EXP 2 PARAM =====================
int exp2_x_state = 0;
int exp2_y_state = 0;
int exp2_send_force_state = 0;
int counter_cyclic = 0;
bool exp2_y_set = false;
bool exp2_x_start_state = false;
bool exp2_stop_y = false;
bool exp2_test_success = false;
bool exp2_limit_swicth_is_pressed = false;
//=========================================================



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
      int cmd_len = cmd_string.length();
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
                select_exp = 1;
                exp1_y_state = 0;
                exp1_x_state = 0;
                exp1_send_force_state = 0;
                exp1_y_set = true;
                exp1_start_y = true;
                exp1_x_state_start = false; 
                exp1_test_success = false;
                break;
              }
              case '2':
              {
                run_machine = true;
                select_exp = 2;  
                exp2_x_state = 0; 
                exp2_y_state = 0;
                counter_cyclic = 0;
                exp2_stop_y = false;
                exp2_x_start_state = false;
                exp2_y_set = true;       
                exp2_test_success = false; 
                exp2_limit_swicth_is_pressed = false; 
                break;
              }
              case '3':
              {
                run_machine = true;
                select_exp = 3;            
                break;
              }
              case '4':
              {
                run_machine = true;
                select_exp = 4;            
                break;
              }
            }
                break;
          }
        case 't':
          {
            run_machine = false;
            select_exp = 0;
            break;
          }
        case 'U': // update pwm
          {
            update_pwm = cmd_string.substring(1,cmd_len).toInt();
            Serial.println(update_pwm,DEC);
            break;
          }
        case 'N': // set param F (Y)
          {
            fixed_vertical_force = cmd_string.substring(1,cmd_len).toInt();
            Serial.println(fixed_vertical_force,DEC);
            break;
          }
        case 'S': // start force
          {
            start_force = cmd_string.substring(1,cmd_len).toInt();
            Serial.println(start_force,DEC);
            break;
          }
        case 'Y': // stop force
          {
            stop_force = cmd_string.substring(1,cmd_len).toInt();
            Serial.println(stop_force,DEC);        
            break;
          }
        case 'C': // cyclic 
          {
            cyclic = cmd_string.substring(1,cmd_len).toInt();
            Serial.println(cyclic,DEC);
            break;
          }
        case 'a': // read param update pwm && F(Y)
          {
            Serial.print(update_pwm);
            Serial.print(",");
            Serial.println(fixed_vertical_force);
            break;
          }
        case 'b': // read param start force(x min) && stop force(x mmax)
          {
            Serial.print(start_force);
            Serial.print(",");
            Serial.println(stop_force);
            break;
          }
        case 'f':
          {
            int vertical_force = analogRead(y_loadcell_pin);
            int horizontal_force = analogRead(x_loadcell_pin);
            Serial.print(vertical_force,DEC);       // return vertical force Y
            Serial.print(",");
            Serial.println(horizontal_force,DEC);     // return horizontal force X
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
          // Serial.println("R1");
          exp1();
          break;
        }
        case 2:
        {
          exp2();
          // Serial.println("R2");
          break;
        }
        case 3:
        {
          Serial.println("R3");
          break;
        }
        case 4:
        {
          Serial.println("R4");
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
              analogWrite(x_motor_speed_pin,255);      
      }
      else if (((x_backward_logic)==1) && ((x_limit_back_logic)==0)) 
      {
              // Serial.println("X_backward");
              digitalWrite(x_motor_dir1,LOW);
              digitalWrite(x_motor_dir2,HIGH);
              analogWrite(x_motor_speed_pin,255);
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
              analogWrite(y_motor_speed_pin,255);    
      }
      else if(((y_down_logic)==1)&&((y_limit_bottom_logic)==0))
      {
              // Serial.println("Y_down");
              digitalWrite(y_motor_dir1,LOW);
              digitalWrite(y_motor_dir2,HIGH);
              analogWrite(y_motor_speed_pin,255);
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
          Serial.println("ZERO COMPLETE");
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
    int x_present_force = analogRead(x_loadcell_pin);
    int y_present_force = analogRead(y_loadcell_pin);
    switch (exp1_x_state)
      {
        case 0:
          {
            if((exp1_x_state_start)==true)
            {
              // Serial.println("EXP1 X");
              exp1_x_state_start = false;
              exp1_x_state = 1;
            }
            break;
          }
        case 1:
          {
            digitalWrite(x_motor_dir1,HIGH);
            digitalWrite(x_motor_dir2,LOW);
            analogWrite(x_motor_speed_pin,update_pwm);
            exp1_x_state = 2;
            break;
          }
        case 2:
          {
            if((x_limit_front_logic)==1)
            {
                digitalWrite(x_motor_dir1,LOW);
                digitalWrite(x_motor_dir2,LOW);
                analogWrite(x_motor_speed_pin,0);
                exp1_x_state = 3;
            }
            break;
          }
        case 3:
          {
            exp1_test_success = true;
            exp1_start_y = false;
            break;
          }
        default:
          {
            break;
          }
      }
    switch (exp1_y_state)
      {
          case 0:
            {
              digitalWrite(y_motor_dir1,LOW);
              digitalWrite(y_motor_dir2,LOW);
              analogWrite(y_motor_speed_pin,0);
              exp1_y_state = 1;
              break;
            }
          case 1:     // move machine down pwm 200
            {
                digitalWrite(y_motor_dir1,LOW);
                digitalWrite(y_motor_dir2,HIGH);
                analogWrite(y_motor_speed_pin,200);
                if(y_present_force >=100)
                {
                    digitalWrite(y_motor_dir1,LOW);
                    digitalWrite(y_motor_dir2,LOW);
                    analogWrite(y_motor_speed_pin,0);
                    delay(300);
                    exp1_y_state = 2;
                }
                
                break;
            }
          case 2:
            {
              digitalWrite(y_motor_dir1,LOW);
              digitalWrite(y_motor_dir2,HIGH);
              analogWrite(y_motor_speed_pin,y_stabilizer_pwm);
              exp1_y_state = 3;
              break;
            }
          case 3:
            {
              if(exp1_start_y == false)
              {
                      exp1_y_state = 7;
                      digitalWrite(y_motor_dir1,LOW);
                      digitalWrite(y_motor_dir2,LOW);
                      analogWrite(y_motor_speed_pin,0);
              }
              if(y_limit_bottom_logic == 1)
                  {
                      exp1_y_state = 7;
                      digitalWrite(y_motor_dir1,LOW);
                      digitalWrite(y_motor_dir2,LOW);
                      analogWrite(y_motor_speed_pin,0);

                  }
              else if (y_present_force >= fixed_vertical_force-loadcell_guard_band)
                  {
                      // Serial.println("OOK");
                      exp1_y_state = 5;
                      digitalWrite(y_motor_dir1,LOW);
                      digitalWrite(y_motor_dir2,LOW);
                      analogWrite(y_motor_speed_pin,0);
                  }
              break;
            }
          case 4:
            {
              digitalWrite(y_motor_dir1,HIGH);
              digitalWrite(y_motor_dir2,LOW);
              analogWrite(y_motor_speed_pin,y_stabilizer_pwm);
              exp1_y_state = 3;
              if((y_limit_top_logic)==1)
                {
                  exp1_start_y = false;
                }
              break;
            }
          case 5:
            {
              if(y_present_force < fixed_vertical_force-loadcell_guard_band)
              {
                  exp1_y_state = 2;
              }
              else if(y_present_force >= fixed_vertical_force+loadcell_guard_band)
              {
                  exp1_y_state = 4;
              }
              if(exp1_y_set == true)
              {
                exp1_x_state_start = true;
                exp1_y_set = false;
                exp1_y_state = 5;
              }
              break;
            }
          case 7:
            {
              // Serial.println("DDDDDD");
              break;
            }
          default:
            {
              break;
            }
          break;
      }
    switch (exp1_send_force_state)
      {
        case 0:
          {
            timemer_send_data = millis();
            exp1_send_force_state = 1;
            break;
          }
        case 1:
          {
            if((millis()-timemer_send_data)>=timmer_trig)
            {
              Serial.print(exp1_test_success);
              Serial.print(",");
              Serial.print(x_present_force);
              Serial.print(",");
              Serial.println(y_present_force);
              exp1_send_force_state = 0;
            }
            // if((millis()-exp1_send_force_state)>=10000)
            // {
            //   exp1_test_success = true;
            // }
            break;
          }
        default:
        {
          break;
        }
      }
  }

void exp2()
  {
    int x_present_force = analogRead(x_loadcell_pin);
    int y_present_force = analogRead(y_loadcell_pin);
    switch (exp2_x_state)
      {
        case 0: // state start x
          {
            if((exp2_x_start_state)== true)
            {
              exp2_x_start_state = false;
              exp2_x_state = 1;
            }
            break;
          }
        case 1: // set x to start force is pwm = 200
          {
            digitalWrite(x_motor_dir1,HIGH);
            digitalWrite(x_motor_dir2,LOW);
            analogWrite(x_motor_speed_pin,200);
            if((x_present_force)>=start_force)
              {
                start_timer = millis();
                exp2_x_state = 2;
              }
            else if((x_limit_front_logic)==1)
              {
                exp2_x_state = 8;
              }
            break;
          }
        case 2: // form start force
          {
            digitalWrite(x_motor_dir1,LOW);
            digitalWrite(x_motor_dir2,LOW);
            analogWrite(x_motor_speed_pin,0);
            if((millis()-start_timer)>=300)
              {
                exp2_x_state = 3;
              }
            break;
          }
        case 3: // x to stop force
          {
            digitalWrite(x_motor_dir1,HIGH);
            digitalWrite(x_motor_dir2,LOW);
            analogWrite(x_motor_speed_pin,update_pwm);
            if ((x_present_force)>=stop_force-loadcell_guard_band)
              {
                exp2_x_state = 4;
              }
            if ((x_limit_front_logic) == 1)
              {
                exp2_x_state = 8;
              }            
            break;
          }
        case 4: // x form stop force 
          {
            digitalWrite(x_motor_dir1,LOW);
            digitalWrite(x_motor_dir2,LOW);
            analogWrite(x_motor_speed_pin,0);
            exp2_x_state = 5;
            break;
          }
        case 5: // x to start force
          {
            digitalWrite(x_motor_dir1,LOW);
            digitalWrite(x_motor_dir2,HIGH);
            analogWrite(x_motor_speed_pin,update_pwm-loadcell_guard_band);
            if((x_present_force)<=start_force)
              {
                exp2_x_state = 6;
              }
            if ((x_limit_back_logic)==1)
              {
                exp2_x_state = 8;
              }
            break;
          }
        case 6: // x form start force and counter cyclic 
          {
            digitalWrite(x_motor_dir1,LOW);
            digitalWrite(x_motor_dir2,LOW);
            analogWrite(x_motor_speed_pin,0);
            counter_cyclic++;
            exp2_x_state = 3;
            if((counter_cyclic)==cyclic)
              {
                exp2_x_state = 7;
              }
            break;
          }
        case 7: // counter cyclic = cyclic form pc
          {
            digitalWrite(x_motor_dir1,LOW);
            digitalWrite(x_motor_dir2,LOW);
            analogWrite(x_motor_speed_pin,0);
            exp2_stop_y = true;
            exp2_test_success = true;
            break; 
          }
        case 8:
          {
            digitalWrite(x_motor_dir1,LOW);
            digitalWrite(x_motor_dir2,LOW);
            analogWrite(x_motor_speed_pin,0);
            exp2_stop_y = true;
            exp2_limit_swicth_is_pressed = true;
            break;
          }
        default:
          {
            break;
          }
      }

    switch (exp2_y_state)
      {
          case 0:// state 0 y == stop
            {
              digitalWrite(y_motor_dir1,LOW);
              digitalWrite(y_motor_dir2,LOW);
              analogWrite(y_motor_speed_pin,0);
              exp2_y_state = 1;
              break;
            }
          case 1:     // move machine down pwm 200
            {
                digitalWrite(y_motor_dir1,LOW);
                digitalWrite(y_motor_dir2,HIGH);
                analogWrite(y_motor_speed_pin,200);
                if(y_present_force >= 100)
                {
                    digitalWrite(y_motor_dir1,LOW);
                    digitalWrite(y_motor_dir2,LOW);
                    analogWrite(y_motor_speed_pin,0);
                    delay(300);
                    exp2_y_state = 2;
                }
                
                break;
            }
          case 2: // move y fig force
            {
              digitalWrite(y_motor_dir1,LOW);
              digitalWrite(y_motor_dir2,HIGH);
              analogWrite(y_motor_speed_pin,y_stabilizer_pwm);
              exp2_y_state = 3;
              break;
            }
          case 3: // selec condition
            {
              if(exp2_stop_y == true)
              {
                      exp2_y_state = 7;
                      digitalWrite(y_motor_dir1,LOW);
                      digitalWrite(y_motor_dir2,LOW);
                      analogWrite(y_motor_speed_pin,0);
              }
              if(y_limit_bottom_logic == 1)
                  {
                      exp2_y_state = 7;
                      digitalWrite(y_motor_dir1,LOW);
                      digitalWrite(y_motor_dir2,LOW);
                      analogWrite(y_motor_speed_pin,0);

                  }
              else if (y_present_force >= fixed_vertical_force-loadcell_guard_band)
                  {
                      exp2_y_state = 5;
                      digitalWrite(y_motor_dir1,LOW);
                      digitalWrite(y_motor_dir2,LOW);
                      analogWrite(y_motor_speed_pin,0);
                  }
              break;
            }
          case 4:
            {
              digitalWrite(y_motor_dir1,HIGH);
              digitalWrite(y_motor_dir2,LOW);
              analogWrite(y_motor_speed_pin,y_stabilizer_pwm);
              exp2_y_state = 3;
              if((y_limit_top_logic)==1)
                {
                  exp2_stop_y = true;
                }
              break;
            }
          case 5:
            {
              if(y_present_force < fixed_vertical_force-loadcell_guard_band)
              {
                  exp2_y_state = 2;
              }
              else if(y_present_force >= fixed_vertical_force+loadcell_guard_band)
              {
                  exp2_y_state = 4;
              }
              if(exp2_y_set == true)
              {
                exp2_x_start_state = true;
                exp2_y_set = false;
                exp2_y_state = 5;
              }
              break;
            }
          case 7:
            {
              break;
            }
          default:
            {
              break;
            }
          break;
      }
    switch (exp2_send_force_state)
      {
        case 0:
          {
            timemer_send_data = millis();
            exp2_send_force_state = 1;
            break;
          }
        case 1:
          {
            if((millis()-timemer_send_data)>=timmer_trig)
              {
                Serial.print(exp2_test_success);
                Serial.print(",");
                Serial.print(x_present_force);
                Serial.print(",");
                Serial.print(y_present_force);
                Serial.print(",");
                Serial.print(counter_cyclic);
                Serial.print(",");
                Serial.println(exp2_limit_swicth_is_pressed);
                exp2_send_force_state = 0;
              }
            break;
          }
        default:
          {
            break;
          }
      }
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
    else if(y_limit_top_state == 0x00)
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