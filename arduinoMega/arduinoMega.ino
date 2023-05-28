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
const int x_backward_pin = 15;
const int y_up_pin =10;
const int y_down_pin =12;


// command from pc
bool execute_cmd = false;
String cmd_string = "";

int loadcell_interval_time = 20;
unsigned long loadcell_timer = 0;

//
bool run_machine = false;
bool set_zero = false;
bool set_zero_x_success = false;
bool set_zero_y_success = false;
int exp_number = 0;
int zero_x_state = 0;
int zero_y_state = 0;
// experiment 1
int fixed_vertical_force = 0;
int fixed_horizontal_force = 0;
bool exp1_state_x_flage = false;
bool exp1_start_state_x = false;
bool exp1_start_test = false;
int exp1_x_state = 0;
int exp1_y_state = 0;
bool exp1_test_success = false;

bool exp2_start_state_x_flage = false;
bool exp2_start_state = false;
int exp2_count_cyclic = 0;
int cyclic = 0;
int cyclic_time = 0;
int start_force = 0;
int stop_force = 0;
int exp2_x_state = 0;
int exp2_y_state = 0;
bool exp2_start_test = false;
bool exp2_test_success = false;
unsigned int over_time = 0;


int update_pwm = 0;
int counter_cyclic = 0;
int start_counter = 0;
int A_cyclic = 0;

const int loadcell_guard_band = 2; 

void setup()
{
    Serial.begin(115200);
    //============ setup motor pin ================
    pinMode(x_motor_dir1,OUTPUT);
    pinMode(x_motor_dir2,OUTPUT);
    pinMode(x_motor_speed_pin,OUTPUT);
    pinMode(x_loadcell_pin,INPUT);

    pinMode(y_motor_dir1,OUTPUT);
    pinMode(y_motor_dir2,OUTPUT);
    pinMode(y_motor_speed_pin,OUTPUT);
    pinMode(y_loadcell_pin,INPUT);

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
}

void loop()
{
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
            case 'f':
            {
                int vertical_force = analogRead(y_loadcell_pin);
                Serial.print(vertical_force-20,DEC);       // return vertical force Y
                Serial.print(",");
                int horizontal_force = analogRead(x_loadcell_pin);
                Serial.println(horizontal_force,DEC);     // return horizontal force X
              break;
            }
            case 'N':   // Y distans
            {
                fixed_vertical_force = cmd_string.substring(1,cmd_len).toInt();
                Serial.println(fixed_vertical_force,DEC);
                break;
            }
            // case 'T':   // X distans
            // {
            //     fixed_horizontal_force = cmd_string.substring(1,cmd_len).toInt();
            //     Serial.println(fixed_horizontal_force,DEC);
            //     break;
            // }
            case 'X': // cyclic
            {
                cyclic  = cmd_string.substring(1,cmd_len).toInt();
                Serial.println(cyclic,DEC);
                break;                
            }
            case 'Y': // start force
            {
                start_force = cmd_string.substring(1,cmd_len).toInt();
                Serial.println(start_force,DEC);
                break;

            }
            case 'S': // stop force
            {
                stop_force = cmd_string.substring(1,cmd_len).toInt();
                Serial.println(stop_force,DEC);
                break;
            }
            case 'I':
            {
                cyclic_time = cmd_string.substring(1,cmd_len).toInt();
                Serial.println(cyclic_time);
                break;
            }
            case 'U': // update pwm for exe 2
            {
                update_pwm = cmd_string.substring(1,cmd_len).toInt();
                Serial.println(update_pwm,DEC);
                break;
            }
            case 'B':
            {
                Serial.println(counter_cyclic);
                break;
            }
            case 'Z':
            {
                set_zero = true;
                zero_x_state = 0;
                zero_y_state = 0;
                break;
            }
            case 'C':
            {
                switch (cmd_string[1])
                {
                    case '1':
                    {
                        if(exp1_test_success == true)
                        {
                            Serial.println("EXP1 SUCCESS");
                        }
                        else
                        {
                            Serial.println("NOT");
                        }
                        break;
                    }

                    case '2':
                    {
                        if(exp2_test_success == true)
                        {
                           Serial.println("EXP2 SUCCESS"); 
                        }
                        else
                        {
                            Serial.println("NOT");
                        }
                        break;
                    }
                    
                    default:
                    {
                        break;
                    }
                }
                break;
            }
            // =============== run and terminate flag ====================
            case 'r':       // run state machine
            {
                switch(cmd_string[1])
                {
                    case '1':           // run experiment 1
                    {   
                        // Serial.println("exp1");
                        run_machine = true;
                        exp1_start_test = true;
                        exp1_start_state_x = true;
                        exp1_test_success = false;
                        exp_number = 1;
                        exp1_x_state = 0;
                        exp1_y_state = 0;
                        break;
                    }
                    case '2':           // run experiment 2
                    {
                        run_machine = true;
                        exp2_start_state_x_flage = true;
                        exp2_start_test = true;
                        exp_number = 2;
                        exp2_x_state = 0;
                        exp2_y_state = 0;
                        exp2_count_cyclic = 0;
                        over_time = 0;
                        break;
                    }
                    case '3':           // run experiment 3
                    {
                        exp_number = 3;
                        break;
                    }
                    case '4':           // run experiment 4
                    {
                        exp_number = 4;
                        break;
                    }
                    default:
                    {
                        break;
                    }
                }
                break;
            }
            case 't':       // terminate state machine
            {
                run_machine = false;
                break;
            }
            // =========== check command =================
            case 'c': // check param for exp1
            {
                Serial.print(fixed_vertical_force);
                Serial.print(",");
                Serial.print(update_pwm);
                Serial.println("");
                break;
            }
            case 'd': // check param for exp2
            {
                Serial.print(start_force);
                Serial.print(",");
                Serial.print(stop_force);
                Serial.println("");
                break;
            }
            case 'L': // check limit
            {
                Serial.print(digitalRead(x_limit_front));
                Serial.print(",");
                Serial.print(digitalRead(x_limit_back));
                Serial.print(",");
                Serial.print(digitalRead(y_limit_top));
                Serial.print(",");
                Serial.print(digitalRead(y_limit_bottom));
                Serial.println("");
                break;
            }
            case 's': // check limit
            {
                switch(cmd_string[1])
                {
                    case '1':
                    {  
                        Serial.print(exp1_x_state);
                        Serial.print(",");
                        Serial.println(exp1_y_state);
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
                    default:
                    {
                        break;
                    }
                }
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
        // ============= exp1 state machine =====================
        switch(exp_number)
        {
            case 1:
            {
                run_exp1(); 
                // Serial.println("EXP1");    
                break;
            }
            case 2:
            {
                // run_exp2();
                // Serial.println("EXP2");
                break;
            }
            case 3:
            {
                // run_exp3()
                break;
            }
            case 4:
            {
                // run_exp4()
                break;
            }
            default:
            {
                break;
            }
        }
    }
    else
    {
        // ======= switch control xaxis=========
        if((digitalRead(x_forward_pin)==0)&&(digitalRead(x_limit_front)==0))
        {
            digitalWrite(x_motor_dir1,HIGH);
            digitalWrite(x_motor_dir2,LOW);
            analogWrite(x_motor_speed_pin,50);
        }
        else if ((digitalRead(x_backward_pin)==0)&&(digitalRead(x_limit_back)==0))
        {
            digitalWrite(x_motor_dir1,LOW);
            digitalWrite(x_motor_dir2,HIGH);
            analogWrite(x_motor_speed_pin,50);
        }
        else
        {
            digitalWrite(x_motor_dir1,LOW);
            digitalWrite(x_motor_dir2,LOW);
            analogWrite(x_motor_speed_pin,0);
        }
        // ======= switch control yaxis =============
        if((digitalRead(y_up_pin)==0)&&(digitalRead(y_limit_top)==0))
        {
            digitalWrite(y_motor_dir1,HIGH);
            digitalWrite(y_motor_dir2,LOW);
            analogWrite(y_motor_speed_pin,150);
        }
        else if ((digitalRead(y_down_pin)==0)&&(digitalRead(y_limit_bottom)==0))
        {
            digitalWrite(y_motor_dir1,LOW);
            digitalWrite(y_motor_dir2,HIGH);
            analogWrite(y_motor_speed_pin,150);
        }
        else
        {
            digitalWrite(y_motor_dir1,LOW);
            digitalWrite(y_motor_dir2,LOW);
            analogWrite(y_motor_speed_pin,0);
        }
        
    }
    
    if(set_zero)
    {
        int limitx_zero = digitalRead(x_limit_back);
        int limity_zero = digitalRead(y_limit_top);
        int set_zero_speed = 255; // set speed motor X , Y ZERO
            // if(limitx_zero==1)
            // {
            //     digitalWrite(x_motor_dir1,LOW);
            //     digitalWrite(x_motor_dir2,LOW);
            //     analogWrite(x_motor_speed_pin,0);
            //     set_zero_x_success = true;
            // }
            // if(limity_zero == 1)
            // {
            //     digitalWrite(y_motor_dir1,LOW);
            //     digitalWrite(y_motor_dir2,LOW);
            //     analogWrite(y_motor_speed_pin,0); 
            //     set_zero_y_success = true;
            // }

            if(set_zero_x_success==true && set_zero_y_success == true)
            {
                Serial.println("ZERO SUCCESS");
                set_zero_x_success = false;
                set_zero_y_success = false;
                set_zero = false;
            }
            switch(zero_x_state)
            {
                case 0:
                {
                    if(limitx_zero == 1)
                    {
                        digitalWrite(x_motor_dir1,LOW);
                        digitalWrite(x_motor_dir2,LOW);
                        analogWrite(x_motor_speed_pin,0);
                        zero_x_state = 3;
                    }
                    else
                    {
                        zero_x_state = 1;
                    }
                }
                case 1:
                { 
                    digitalWrite(x_motor_dir1,LOW);
                    digitalWrite(x_motor_dir2,HIGH);
                    analogWrite(x_motor_speed_pin,set_zero_speed);
                    if(limitx_zero == 1)
                    {
                        zero_x_state = 2; 
                    }
                    break;
                }
                case 2:
                {
                    digitalWrite(x_motor_dir1,LOW);
                    digitalWrite(x_motor_dir2,LOW);
                    analogWrite(x_motor_speed_pin,0);
                    zero_x_state = 3;
                    break;
                }
                case 3:
                {
                    set_zero_x_success=true;
                    break;
                }
                default:
                {
                    set_zero = false;
                }
            }
            switch (zero_y_state)
            {
                case 0:
                {
                    if(limity_zero == 1)
                    {
                        digitalWrite(y_motor_dir1,LOW);
                        digitalWrite(y_motor_dir2,LOW);
                        analogWrite(y_motor_speed_pin,0);
                        zero_y_state = 3;
                    }
                    else
                    {
                        zero_y_state = 1;
                    }
                    break;
                }

                case 1:
                {
                    if(limity_zero == 1)
                    {
                        digitalWrite(y_motor_dir1,LOW);
                        digitalWrite(y_motor_dir2,LOW);
                        analogWrite(y_motor_speed_pin,0);
                        zero_y_state = 3;
                    }
                    else
                    {
                        digitalWrite(y_motor_dir1,LOW);
                        digitalWrite(y_motor_dir2,HIGH);
                        analogWrite(y_motor_speed_pin,set_zero_speed); 
                        if(limity_zero == 1)
                        {
                            zero_y_state = 2;
                        }              
                    }
                    break;
                } 
                case 2:
                {
                    digitalWrite(y_motor_dir1,LOW);
                    digitalWrite(y_motor_dir2,LOW);
                    analogWrite(y_motor_speed_pin,0);
                    zero_y_state = 3;
                    break;
                }

                case 3:
                {
                    set_zero_y_success = true;
                    break;
                }
                
                default:
                {
                    break;
                }
                
            }
        
    }
}

void run_exp1()
{
    if(exp1_start_test == true)
    {
        // Serial.println(exp1_y_state);
        int x_present_force = analogRead(x_loadcell_pin);
        int y_present_force = analogRead(y_loadcell_pin);
        int y_speed_motor_stabilizer = 35;
        switch (exp1_x_state) // X state
        {
            case 0:
            {
                if(exp1_state_x_flage == true)
                {
                    exp1_state_x_flage = false;
                    exp1_x_state = 1;
                }
                break;
            }
            case 1:     // move machine to force >= 1
            {
                digitalWrite(x_motor_dir1,HIGH);
                digitalWrite(x_motor_dir2,LOW);
                analogWrite(x_motor_speed_pin,update_pwm);
                exp1_x_state = 2;
                break;
            }
            case 2:
            {
                if(digitalRead(x_limit_front)==1)
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
                Serial.flush();
                exp1_start_test = false;
                exp1_test_success = true;
                break;
            }
            default:
            {
                exp1_start_test = false;
                break;
            }
        }
        //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        switch (exp1_y_state) // Y state
        {
            case 0:
            {
                exp1_y_state = 1;
                break;
            }
            case 1:
            {
                exp1_y_state = 2;
                break;
            }
            case 2:     // move machine down pwm 200
            {
                digitalWrite(y_motor_dir1,HIGH);
                digitalWrite(y_motor_dir2,LOW);
                analogWrite(y_motor_speed_pin,255);
                if(y_present_force >=50)
                {
                    digitalWrite(y_motor_dir1,LOW);
                    digitalWrite(y_motor_dir2,LOW);
                    analogWrite(y_motor_speed_pin,0);
                    exp1_y_state = 3;
                }
                
                break;
            }
            case 3: // force >1 stop Motor Y
            {
                delay(300);
                exp1_y_state = 4;
                break;
            }
            case 4: // start Motor Y Pwm 20 and move down
            {

                digitalWrite(y_motor_dir1,HIGH);
                digitalWrite(y_motor_dir2,LOW);
                analogWrite(y_motor_speed_pin,y_speed_motor_stabilizer);
                exp1_y_state = 5;
                break;
            }
            case 5: // get limit or preforce > fixvertical
            {
                int limit_logic = digitalRead(y_limit_bottom);
                Serial.println(limit_logic);
                limit_logic = digitalRead(y_limit_bottom);
                Serial.println(limit_logic);
                limit_logic = digitalRead(y_limit_bottom);
                Serial.println(limit_logic);
                if(limit_logic==1)
                    {
                        exp1_y_state = 8;
                        digitalWrite(y_motor_dir1,LOW);
                        digitalWrite(y_motor_dir2,LOW);
                        analogWrite(y_motor_speed_pin,0);

                    }
                else if (y_present_force >= fixed_vertical_force-loadcell_guard_band)
                    {
                        exp1_y_state = 7;
                        digitalWrite(y_motor_dir1,LOW);
                        digitalWrite(y_motor_dir2,LOW);
                        analogWrite(y_motor_speed_pin,0);

                    }
                break;  
            }
            case 6: // move up
            {   
                digitalWrite(y_motor_dir1,LOW);
                digitalWrite(y_motor_dir2,HIGH);
                analogWrite(y_motor_speed_pin,y_speed_motor_stabilizer);
                exp1_y_state = 5;
                break;
            }
            case 7: // stabilizer Y force
            {
                if(y_present_force < fixed_vertical_force-loadcell_guard_band)
                {
                    exp1_y_state = 4;
                }
                else if(y_present_force >= fixed_vertical_force+loadcell_guard_band)
                {
                    exp1_y_state = 6;
                }
                else if(exp1_start_state_x == true)
                {
                    exp1_state_x_flage = true;  
                    exp1_start_state_x = false;
                    exp1_y_state = 7;
                }
                break;
            }
            case 8:
            {
                break;
            }
            default:
            {
                break;
            }
        }
        //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    }
}

void run_exp2()
{
    int x_present_force = analogRead(x_loadcell_pin);
    int y_present_force = analogRead(y_loadcell_pin);  
    int y_speed_motor_stabilizer = 35;
    if(exp2_start_test == true)
    {
        switch (exp2_x_state)
        {
        case 0:
            {
                if(exp2_start_state == true)
                {
                    exp2_start_state = false;
                    exp2_x_state = 1;
                }
                break;
            }
        
        case 1:
            {
                digitalWrite(x_motor_dir1,HIGH);
                digitalWrite(x_motor_dir2,LOW);
                analogWrite(x_motor_speed_pin,200);
                exp2_x_state = 2;
                break;
            }
        
        case 2:
            {
                if(x_present_force>=start_force)
                {
                    delay(300);
                    exp2_x_state = 3;
                }
                break;
            }
        case 3:
            {
                digitalWrite(x_motor_dir1,HIGH);
                digitalWrite(x_motor_dir2,LOW);
                analogWrite(x_motor_speed_pin,update_pwm);
                exp2_x_state = 4;
                over_time = millis();
                break;
            }
        case 4:
            {
                if(x_present_force>=stop_force)
                {
                    exp2_x_state = 5;
                }
                if((millis()-over_time)>=cyclic_time)
                {
                    exp2_x_state = 5;
                }
                break;
            }
        case 5:
            {
                digitalWrite(x_motor_dir1,LOW);
                digitalWrite(x_motor_dir2,HIGH);
                analogWrite(x_motor_speed_pin,update_pwm);
                exp2_x_state = 6;
                over_time = millis();
                break;
            }
        case 6:
            {
                if(x_present_force <= start_force)
                {
                    exp2_count_cyclic++;
                    exp2_x_state = 3;
                }
                if((millis()-over_time)>=cyclic_time)
                {
                    exp2_count_cyclic++;
                    exp2_x_state = 3;  
                }
                if(cyclic == exp2_count_cyclic)
                {
                    exp2_x_state = 7;
                }
                break;
            }
        case 7:
            {
                exp2_start_test = false;
                exp2_test_success = true;
            }
        default:
            {
                exp2_start_test = false;
                break;
            }
            break;
        }
        /////////////////////////////////////////////////   EXP2 Y STATE   /////////////////////////////////////////////////////////////////
        switch (exp2_y_state)
        {
            case 0:
                {
                    exp2_y_state = 1;
                    break;
                }
            case 1:     // move machine down pwm 255
                {
                    digitalWrite(y_motor_dir1,HIGH);
                    digitalWrite(y_motor_dir2,LOW);
                    analogWrite(y_motor_speed_pin,255);
                    if(y_present_force >=70)
                    {
                        digitalWrite(y_motor_dir1,LOW);
                        digitalWrite(y_motor_dir2,LOW);
                        analogWrite(y_motor_speed_pin,0);
                        exp2_y_state = 2;
                    }
                    break;
                }
            case 2: // delay 300 ms
                {
                    delay(300);
                    exp2_y_state = 3;
                    break;
                }
            case 3: // start Motor Y Pwm 20 and move down
                {
                    digitalWrite(y_motor_dir1,HIGH);
                    digitalWrite(y_motor_dir2,LOW);
                    analogWrite(y_motor_speed_pin,y_speed_motor_stabilizer);
                    exp2_y_state = 4;
                    break;
                }
            case 4: // get limit or preforce > fixvertical
                {
                    if(digitalRead(y_limit_bottom)==1)
                    {
                        exp2_y_state = 7;
                        digitalWrite(y_motor_dir1,LOW);
                        digitalWrite(y_motor_dir2,LOW);
                        analogWrite(y_motor_speed_pin,0);

                    }
                    else if (y_present_force >= fixed_vertical_force-loadcell_guard_band)
                    {
                        exp2_y_state = 6;
                        digitalWrite(y_motor_dir1,LOW);
                        digitalWrite(y_motor_dir2,LOW);
                        analogWrite(y_motor_speed_pin,0);

                    }
                break;  
                }
            case 5: // move up
                {   
                    digitalWrite(y_motor_dir1,LOW);
                    digitalWrite(y_motor_dir2,HIGH);
                    analogWrite(y_motor_speed_pin,y_speed_motor_stabilizer);
                    exp2_y_state = 4;
                    break;
                }
            case 6: // stabilizer Y force
                {
                    if(y_present_force < fixed_vertical_force-loadcell_guard_band)
                    {
                        exp2_y_state = 3;
                    }
                    else if(y_present_force >= fixed_vertical_force+loadcell_guard_band)
                    {
                        exp2_y_state = 5;
                    }
                    else if(exp2_start_state_x_flage == true)
                    {
                        exp2_start_state_x_flage = false;
                        exp2_start_state = true;
                        exp2_y_state = 6;
                    }
                    break;
                }      
            default:
                {
                    exp2_start_test = false;
                    break;
                }
        
            break;
        }

    }
}
