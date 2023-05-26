const int x_loadcell_pin = A10;
const int y_loadcell_pin = A13;

const int x_motor_dir1 = 7;
const int x_motor_dir2 = 5;
const int x_motor_speed_pin = 3;

const int y_motor_dir1 = 6;
const int y_motor_dir2 = 4;
const int y_motor_speed_pin = 2;

// limit switches
const int x_limit_front = 18;
const int x_limit_back = 16;
const int y_limit_top = 20;
const int y_limit_bottom = 26;

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
bool set_zero_success = false;

int exp_number = 0;
int zero_state = 0;
// experiment 1
int fixed_vertical_force = 0;
int fixed_horizontal_force = 0;
bool exp1_state_x_flage = false;
bool exp1_start_state_x = false;
int exp1_x_state = 0;
int exp1_y_state = 0;
int cyclic = 0;
int start_force = 0;
int stop_force = 0;
int update_pwm = 0;
int exp2_x_state = 0;
int exp2_y_state = 0;
int counter_cyclic = 0;
int start_counter = 0;
int f_max = 0;
int f_min = 0;
int A_cyclic = 0;
unsigned int cyclic_time = 0; 

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
            case 'T':   // X distans
            {
                fixed_horizontal_force = cmd_string.substring(1,cmd_len).toInt();
                Serial.println(fixed_horizontal_force,DEC);
                break;
            }
            case 'X': // cyclic
            {
                cyclic  = cmd_string.substring(1,cmd_len).toInt();
                Serial.println(cyclic,DEC);
                break;                
            }
            case 'A': //A cyclic
            {
                A_cyclic  = cmd_string.substring(1,cmd_len).toInt();
                Serial.println(A_cyclic,DEC);
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
            case 'L':
            {
                Serial.print(f_min);
                Serial.print(",");
                Serial.print(f_max);
                Serial.println(" ");               
                break;
            }
            case 'Z':
            {
                set_zero = true;
                zero_state = 0;
                // Serial.println("ZERO");
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
                        exp1_start_state_x = true;
                        exp_number = 1;
                        exp1_x_state = 0;
                        exp1_y_state = 0;
                        break;
                    }
                    case '2':           // run experiment 2
                    {
                        run_machine = true;
                        exp_number = 2;
                        exp2_x_state = 0;
                        exp2_y_state = 0;
                        counter_cyclic = 0;
                        start_counter = 0;
                        cyclic_time = 0;
                        f_max = 0;
                        f_min = 0;
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
                Serial.print(fixed_horizontal_force);
                Serial.println("");
                break;
            }
            case 'd':
            {
                Serial.print(start_force);
                Serial.print(",");
                Serial.print(stop_force);
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
                run_exp2();
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
        int limity_zero = digitalRead(y_limit_bottom);
        switch(zero_state)
        {
            case 0:
            {
                int limitx_zero = digitalRead(x_limit_back);
                int limity_zero = digitalRead(y_limit_bottom);
                if(((limitx_zero)==1)&&((limity_zero)==1))
                {
                    digitalWrite(x_motor_dir1,LOW);
                    digitalWrite(x_motor_dir2,LOW);
                    digitalWrite(y_motor_dir1,LOW);
                    digitalWrite(y_motor_dir2,LOW);
                    analogWrite(x_motor_speed_pin,0);
                    analogWrite(y_motor_speed_pin,0);
                    zero_state = 3;
                }
                else
                {
                    zero_state = 1;
                }
            }
            case 1:
            { 
                digitalWrite(x_motor_dir1,LOW);
                digitalWrite(x_motor_dir2,HIGH);
                analogWrite(x_motor_speed_pin,255);
                if((limitx_zero)==1)
                {
                    zero_state = 2; 
                }
                break;
            }
            case 2:
            {
                digitalWrite(x_motor_dir1,LOW);
                digitalWrite(x_motor_dir2,LOW);
                analogWrite(x_motor_speed_pin,0);
                zero_state = 3;
                break;
            }
            case 3:
            {
                digitalWrite(y_motor_dir1,LOW);
                digitalWrite(y_motor_dir2,HIGH);
                analogWrite(y_motor_speed_pin,255);
                if((limity_zero)==1)
                {
                    zero_state = 4;
                }
                break;
            }
            case 4:
            {
                digitalWrite(y_motor_dir1,LOW);
                digitalWrite(y_motor_dir2,LOW);
                analogWrite(y_motor_speed_pin,0);
                zero_state = 5;
                break;
            }
            case 5:
            {
                Serial.println("ZERO");
                set_zero = false;
                set_zero_success = true;
                break;
            }
            default:
            {
            
            }
        }
    }
}

void run_exp1()
{
    int x_present_force = analogRead(x_loadcell_pin);
    int y_present_force = analogRead(y_loadcell_pin);
    switch (exp1_x_state)
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
        case 1:     // move machine forward
        {
            digitalWrite(x_motor_dir1,HIGH);
            digitalWrite(x_motor_dir2,LOW);
            analogWrite(x_motor_speed_pin,30);
            exp1_x_state = 2;
            break;
        }
        case 2:
        {
            if(digitalRead(x_limit_front)==1)
            {
                exp1_x_state = 5;
                digitalWrite(x_motor_dir1,LOW);
                digitalWrite(x_motor_dir2,LOW);
                analogWrite(x_motor_speed_pin,0);

            }
            else if (x_present_force >= fixed_horizontal_force-loadcell_guard_band)
            {
                exp1_x_state = 4;
                digitalWrite(x_motor_dir1,LOW);
                digitalWrite(x_motor_dir2,LOW);
                analogWrite(x_motor_speed_pin,0);
            }
        break;
        }
        case 3:
        {   // move machine backward
            digitalWrite(x_motor_dir1,LOW);
            digitalWrite(x_motor_dir2,HIGH);
            analogWrite(x_motor_speed_pin,30);
            exp1_x_state = 2;
            break;
        }
        case 4:
        {
            if(x_present_force < fixed_horizontal_force-loadcell_guard_band)
            {
                exp1_x_state = 1;
            }
            else if(x_present_force >= fixed_horizontal_force+loadcell_guard_band)
            {
                exp1_x_state = 3;
            }
            break;

        }
        case 5:
        {
            // Serial.println("X case 5");
            break;
        }
        default:
        {

        }
    }

    switch (exp1_y_state)
    {
        case 0:
        {
            zero_state = 0;
            set_zero = true;
            exp1_y_state = 1;
            break;
        }
        case 1:
        {
            if(set_zero_success == true)
            {
                set_zero_success = false;
                delay(1000);
                exp1_y_state = 2;
            }
            break;
        }
        case 2:     // move machine down pwm 200
        {
            digitalWrite(y_motor_dir1,HIGH);
            digitalWrite(y_motor_dir2,LOW);
            analogWrite(y_motor_speed_pin,200);
            exp1_y_state = 3;
            break;
        }
        case 3: // force >1 stop Motor Y
        {
            if(y_present_force >1)
            {
                digitalWrite(y_motor_dir1,LOW);
                digitalWrite(y_motor_dir2,LOW);
                analogWrite(y_motor_speed_pin,0);
                delay(300);
                exp1_y_state = 4;
            }
            break;
        }
        case 4: // start Motor Y Pwm 30
        {
            digitalWrite(y_motor_dir1,HIGH);
            digitalWrite(y_motor_dir2,LOW);
            analogWrite(y_motor_speed_pin,20);
            exp1_y_state = 5;
            break;
        }
        case 5: // get limit or preforce > fixvertical
        {
            if(digitalRead(y_limit_bottom)==1)
            {
                exp1_y_state = 7;
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
            analogWrite(y_motor_speed_pin,20);
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
            }
            break;
        }
        case 8:
        {
            break;
        }
        default:
        {

        }
    }

}

void run_exp2()
{
    int x_present_force = analogRead(x_loadcell_pin);
    int y_present_force = analogRead(y_loadcell_pin);  
    switch (exp2_x_state)
    {
        case 0:
        {
            exp2_x_state = 1;
            break;
        }
        case 1:     // move machine forward
        {
            digitalWrite(x_motor_dir1,HIGH);
            digitalWrite(x_motor_dir2,LOW);
            analogWrite(x_motor_speed_pin,100);
            exp2_x_state = 2;
            break;
        }
        case 2: // move machine to start force
        {
            if(digitalRead(x_limit_front)==1)
            {
                exp2_x_state = 6;
                digitalWrite(x_motor_dir1,LOW);
                digitalWrite(x_motor_dir2,LOW);
                analogWrite(x_motor_speed_pin,0);
            }
            else if (x_present_force == start_force-loadcell_guard_band)
            {
                exp2_x_state = 3;
                digitalWrite(x_motor_dir1,LOW);
                digitalWrite(x_motor_dir2,LOW);
                analogWrite(x_motor_speed_pin,0);
                f_min = x_present_force;
                // Serial.println("Y"+(String(x_present_force)));
                if(start_counter>0)
                {
                    counter_cyclic++;
                }
            }
            // else if((millis()-cyclic_time)>=cyclic)
            // {
            //     // Serial.println("state2.3");
            //     exp2_x_state = 3;
            //     digitalWrite(x_motor_dir1,LOW);
            //     digitalWrite(x_motor_dir2,LOW);
            //     analogWrite(x_motor_speed_pin,0);
            //     f_min = x_present_force;
            //     // Serial.println("Y"+(String(x_present_force)));
            //     if(start_counter>0)
            //     {
            //         counter_cyclic++;
            //     }
            // }
            break;
        }
        case 3: // move machine to stop force
        {  
            // Serial.println("state3");
            digitalWrite(x_motor_dir1,HIGH);
            digitalWrite(x_motor_dir2,LOW);
            analogWrite(x_motor_speed_pin,update_pwm);
            // cyclic_time = millis();
            exp2_x_state = 4;
            break;
        }
        case 4: // machine in stop force
        {
            // Serial.println("state4");
            // Serial.println(cyclic_time);
            if(digitalRead(x_limit_front)==1)
            {
                // Serial.println("state4.1");
                exp2_x_state = 6;
                digitalWrite(x_motor_dir1,LOW);
                digitalWrite(x_motor_dir2,LOW);
                analogWrite(x_motor_speed_pin,0);
            }
            else if (x_present_force == stop_force-loadcell_guard_band)
            {
                // Serial.println("state4.2");
                exp2_x_state = 5;
                digitalWrite(x_motor_dir1,LOW);
                digitalWrite(x_motor_dir2,LOW);
                analogWrite(x_motor_speed_pin,0);
                f_max = x_present_force;
                // Serial.println("S"+(String(x_present_force)));
                start_counter++;

            }
            // else if((millis()-cyclic_time)>=cyclic)
            // {
            //     // Serial.println("state4.3");
            //     exp2_x_state = 5;
            //     digitalWrite(x_motor_dir1,LOW);
            //     digitalWrite(x_motor_dir2,LOW);
            //     analogWrite(x_motor_speed_pin,0);
            //     // cyclic_time = 0;
            //     f_max = x_present_force;
            //     // Serial.println("S"+(String(x_present_force)));
            //     start_counter++;
            // }
            break;
        }
        case 5: // move machine to start force
        {
            // Serial.println("state5");
            digitalWrite(x_motor_dir1,LOW);
            digitalWrite(x_motor_dir2,HIGH);
            analogWrite(x_motor_speed_pin,update_pwm);
            // cyclic_time = millis();
            exp2_x_state = 2;
            break;
        }

        case 6:
        {
            break;
        }
        default:
        {

        }
    }  

    switch (exp2_y_state)
    {
        case 0:
        {
            // Serial.println("m1");
            exp2_y_state = 1;
            break;
        }
        case 1:     // move machine down
        {
            digitalWrite(y_motor_dir1,HIGH);
            digitalWrite(y_motor_dir2,LOW);
            analogWrite(y_motor_speed_pin,70);
            exp2_y_state = 22;
            break;
        }
        case 22:
        {
            if(y_present_force >= 5)
            {
                exp1_y_state = 23;
                digitalWrite(y_motor_dir1,LOW);
                digitalWrite(y_motor_dir2,LOW);
                analogWrite(y_motor_speed_pin,0);
                delay(300);               
            }
            break;
        }
        case 23:     // move machine down
        {
            digitalWrite(y_motor_dir1,HIGH);
            digitalWrite(y_motor_dir2,LOW);
            analogWrite(y_motor_speed_pin,30);
            exp2_y_state = 2;
            break;
        }       
        case 2:
        {
            if(digitalRead(y_limit_bottom)==1)
            {
                exp2_y_state = 5;
                digitalWrite(y_motor_dir1,LOW);
                digitalWrite(y_motor_dir2,LOW);
                analogWrite(y_motor_speed_pin,0);
            }
            else if (y_present_force >= fixed_vertical_force-loadcell_guard_band)
            {
                exp2_y_state = 4;
                digitalWrite(y_motor_dir1,LOW);
                digitalWrite(y_motor_dir2,LOW);
                analogWrite(y_motor_speed_pin,0);
            }
            break;
        }
        case 3:
        {   // move up
            digitalWrite(y_motor_dir1,LOW);
            digitalWrite(y_motor_dir2,HIGH);
            analogWrite(y_motor_speed_pin,20);
            exp2_y_state = 2;
            break;
        }
        case 4:
        {
            if(y_present_force < fixed_vertical_force-loadcell_guard_band)
            {
                exp2_y_state = 23;
            }
            else if(y_present_force >= fixed_vertical_force+loadcell_guard_band)
            {
                exp2_y_state = 3;
            }
            break;
        }
        case 5:
        {
            break;
        }
        default:
        {

        }
    }    


}
