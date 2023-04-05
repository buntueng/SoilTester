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

int exp_number = 0;
// experiment 1
int fixed_vertical_force = 0;
int max_horizontal_force = 0;
int exp1_state = 0;

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

    // Serial.print(digitalRead(y_limit_top));
    // Serial.print(",");
    // Serial.println(digitalRead(y_limit_bottom));
    // delay(100);

    if(execute_cmd)
    {
        int cmd_len = cmd_string.length();
        switch(cmd_string[0])
        {
            case 'N':
            {
                fixed_vertical_force = cmd_string.substring(1,cmd_len).toInt();
                break;
            }
            case 'T':
            {
                max_horizontal_force = cmd_string.substring(1,cmd_len).toInt();
                break;
            }
            
            // =============== run and terminate flag ====================
            case 'r':       // run state machine
            {
                switch(cmd_string[1])
                {
                    case '1':           // run experiment 1
                    {
                        break;
                    }
                    case '2':           // run experiment 2
                    {
                        break;
                    }
                    case '3':           // run experiment 3
                    {
                        break;
                    }
                    case '4':           // run experiment 4
                    {
                        break;
                    }
                    default:
                    {

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
            case 'c':
            {
                Serial.print(fixed_vertical_force);
                Serial.print(",");
                Serial.print(max_horizontal_force);
                // Serial.print(",");
                // Serial.print(x_min_displacement);
                // Serial.print(",");
                // Serial.print(x_max_displacement);
                // Serial.print(",");
                // Serial.print(x_distance);
                Serial.println("");
                break;
            }
            default:
            {

            }
        }
        execute_cmd = false;
        cmd_string = "";
    }


    // ============== run machine here ==========================
    if(run_machine)
    {
        unsigned long present_time = millis();
        // send loadcell every 10 milliseconds
        if(present_time-loadcell_timer >= loadcell_interval_time)
        {
            int x_loadcell_value = analogRead(x_loadcell_pin);
            Serial.print("x");
            Serial.println(x_loadcell_value,DEC);
            int y_loadcell_value = analogRead(y_loadcell_pin);
            Serial.print("Y");
            Serial.print("y");
            Serial.println(y_loadcell_value,DEC);
            loadcell_timer = present_time;

        }
        // ============= exp1 state machine =====================
        switch(exp_number)
        {
            case 1:
            {
                run_exp1();
                break;
            }
            case 2:
            {
                // run_exp2()
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
    
}



void run_exp1()
{
    int y_present_force = analogRead(y_loadcell_pin);
    switch (exp1_state)
    {
        case 0:
        {
            exp1_state = 1;
            break;
        }
        case 1:     // move machine down
        {
            digitalWrite(y_motor_dir1,HIGH);
            digitalWrite(y_motor_dir2,LOW);
            analogWrite(y_motor_speed_pin,50);
            exp1_state = 2;
            break;
        }
        case 2:
        {
            if(digitalRead(y_limit_bottom)==1)
            {
                
            }
            else if (y_present_force > fixed_vertical_force)
            {
                
            }
            else if (y_present_force < fixed_vertical_force)
            {

            }
            else if(y_present_force == fixed_vertical_force)
            {
                
            }
        break;
    }
    default:
        break;
    }

}

        // switch (x_axis_state_machine)
        // {
        // case 0:
        // {
        //     x_axis_state_machine = 1;
        //     // Serial.println("case 0");
        //     break;
        // }
        // case 1:
        // {
        //     digitalWrite(x_motor_dir1,HIGH);
        //     digitalWrite(x_motor_dir2,LOW);
        //     analogWrite(x_motor_speed_pin,pwm_xaxis);
        //     x_axis_state_machine = 2;
        //     // Serial.println("case1");
        //     break;
        // }
        // case 2:
        // {
        //     // if((digitalRead(x_limit_front)==1) || (x_distance <= x_max_displacement))
        //     if((digitalRead(x_limit_front)==1))
        //     {
        //         digitalWrite(x_motor_dir1,LOW);
        //         digitalWrite(x_motor_dir2,LOW);
        //         analogWrite(x_motor_speed_pin,0);
        //         x_axis_state_machine = 3;
        //         // Serial.println("case2");
        //     }
        //     break;
        // }
        // case 3:
        // {
        //     digitalWrite(x_motor_dir1,LOW);
        //     digitalWrite(x_motor_dir2,HIGH);
        //     analogWrite(x_motor_speed_pin,pwm_xaxis);
        //     x_axis_state_machine = 4;
        //     break;
        // }
        // case 4:
        // {
        //     // if((digitalRead(x_limit_back)==1) || (x_distance >= x_min_displacement))
        //     if((digitalRead(x_limit_back)==1) )
        //     {
        //         digitalWrite(x_motor_dir1,LOW);
        //         digitalWrite(x_motor_dir2,LOW);
        //         analogWrite(x_motor_speed_pin,0);
        //         x_axis_state_machine = 1;
        //     }
        //     break;
        // }
        // default:
        //     break;
        // }
        // // ============= y axis state machine =====================
        // switch(y_axis_state_machine)
        // {
        //     case 0:
        //     {
        //         break;
        //     }
        //     case 1:     // move up
        //     {
        //         digitalWrite(y_motor_dir1,HIGH);
        //         digitalWrite(y_motor_dir2,LOW);
        //         analogWrite(y_motor_speed_pin,pwm_xaxis);
        //         break;
        //     }
        //     case 2:     // move down
        //     {
        //         digitalWrite(y_motor_dir1,HIGH);
        //         digitalWrite(y_motor_dir2,LOW);
        //         analogWrite(y_motor_speed_pin,pwm_yaxis);
        //         break;
        //     }
        //     case 3:
        //     {
        //         digitalWrite(y_motor_dir1,HIGH);
        //         digitalWrite(y_motor_dir2,LOW);
        //         analogWrite(y_motor_speed_pin,0);
        //         break;
        //     }
        //     default:
        //     {

        //     }
        // }