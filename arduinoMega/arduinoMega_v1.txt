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

int interval_time = 0;

bool execute_cmd = false;
String cmd_string = "";

int pwm_xaxis = 0;
int cyclic_ms = 0;
int x_max_displacement = 0;
int x_min_displacement = 0;
int x_distance = 0;
int x_loadcell = 0;

int x_moving_time = 0;
int x_total_round = 0;
bool x_stop = false;

int pwm_yaxis = 0;
int y_distance = 0;
int y_max_displacement = 0;
int y_loadcell = 0;
int y_weight = 0;

bool run_machine = false;
int x_axis_state_machine = 0;
int y_axis_state_machine = 0;

unsigned long loadcell_timer = 0;
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
            case 'I':
            {
                interval_time = cmd_string.substring(1,cmd_len).toInt();
                break;
            }
            case 'L':
            {
                x_moving_time = cmd_string.substring(1,cmd_len).toInt();
                break;
            }
            case 'A':
            {
                x_total_round = cmd_string.substring(1,cmd_len).toInt();
                break;
            }
            case 'B':           // break motor x axis
            {
                x_stop = true;
                break;
            }
            // =============== x-axis =============
            // case 'S':   // set pwm to x-axis range from 0 to 255 [0-100%]
            // {
            //     pwm_xaxis = cmd_string.substring(1,cmd_len).toInt();
            //     break;
            // }
            // case 'C':   // cyclic time in milliseconds [not less than 1000]
            // {
            //     cyclic_ms = cmd_string.substring(1,cmd_len).toInt();
            //     break;
            // }
            // case 'L':   // maximum displacement in micrometers
            // {
            //     x_max_displacement = cmd_string.substring(1,cmd_len).toInt();
            //     break;
            // }
            // case 'M':   // minimum displacement in micrometers
            // {
            //     x_min_displacement = cmd_string.substring(1,cmd_len).toInt();
            //     break;
            // }
            // case 'X':
            // {
            //     x_distance = cmd_string.substring(1,cmd_len).toInt();
            //     break;
            // }
            // //======== parameters on Y axis ==========
            case 'Y':   // set pwm to y-axis range from 0 to 255 [0-100%]
            {
                pwm_yaxis = cmd_string.substring(1,cmd_len).toInt();
                break;
            }
            case 'U':
            {
                y_axis_state_machine = 1;
                break;
            }
            case 'D':
            {
                y_axis_state_machine = 2;
                break;
            }
            case 'P':
            {
                y_axis_state_machine = 3;
                break;
            }
            // =============== run and terminate flag ====================
            case 'R':       // run state machine
            {
                x_axis_state_machine = 0;
                run_machine = true;
                break;
            }
            case 'T':       // terminate state machine
            {
                run_machine = false;
                digitalWrite(x_motor_dir1,LOW);
                digitalWrite(x_motor_dir2,LOW);
                analogWrite(x_motor_speed_pin,0);
                break;
            }
            // =========== check command =================
            case 'G':
            {
                Serial.print(pwm_xaxis);
                Serial.print(",");
                Serial.print(cyclic_ms);
                Serial.print(",");
                Serial.print(x_min_displacement);
                Serial.print(",");
                Serial.print(x_max_displacement);
                Serial.print(",");
                Serial.println(x_distance);
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
        if(present_time-loadcell_timer >= interval_time)
        {
            int x_loadcell_value = analogRead(x_loadcell_pin);
            Serial.print("X");
            Serial.println(x_loadcell_value,DEC);
 
            int y_loadcell_value = analogRead(y_loadcell_pin);
            Serial.print("Y");
            Serial.println(y_loadcell_value,DEC);
            loadcell_timer = present_time;

        }
        // ============= x axis state machine =====================
        switch (x_axis_state_machine)
        {
        case 0:
        {
            x_axis_state_machine = 1;
            // Serial.println("case 0");
            break;
        }
        case 1:
        {
            digitalWrite(x_motor_dir1,HIGH);
            digitalWrite(x_motor_dir2,LOW);
            analogWrite(x_motor_speed_pin,pwm_xaxis);
            x_axis_state_machine = 2;
            // Serial.println("case1");
            break;
        }
        case 2:
        {
            // if((digitalRead(x_limit_front)==1) || (x_distance <= x_max_displacement))
            if((digitalRead(x_limit_front)==1))
            {
                digitalWrite(x_motor_dir1,LOW);
                digitalWrite(x_motor_dir2,LOW);
                analogWrite(x_motor_speed_pin,0);
                x_axis_state_machine = 3;
                // Serial.println("case2");
            }
            break;
        }
        case 3:
        {
            digitalWrite(x_motor_dir1,LOW);
            digitalWrite(x_motor_dir2,HIGH);
            analogWrite(x_motor_speed_pin,pwm_xaxis);
            x_axis_state_machine = 4;
            break;
        }
        case 4:
        {
            // if((digitalRead(x_limit_back)==1) || (x_distance >= x_min_displacement))
            if((digitalRead(x_limit_back)==1) )
            {
                digitalWrite(x_motor_dir1,LOW);
                digitalWrite(x_motor_dir2,LOW);
                analogWrite(x_motor_speed_pin,0);
                x_axis_state_machine = 1;
            }
            break;
        }
        default:
            break;
        }
        // ============= y axis state machine =====================
        switch(y_axis_state_machine)
        {
            case 0:
            {
                break;
            }
            case 1:     // move up
            {
                digitalWrite(y_motor_dir1,HIGH);
                digitalWrite(y_motor_dir2,LOW);
                analogWrite(y_motor_speed_pin,pwm_xaxis);
                break;
            }
            case 2:     // move down
            {
                digitalWrite(y_motor_dir1,HIGH);
                digitalWrite(y_motor_dir2,LOW);
                analogWrite(y_motor_speed_pin,pwm_yaxis);
                break;
            }
            case 3:
            {
                digitalWrite(y_motor_dir1,HIGH);
                digitalWrite(y_motor_dir2,LOW);
                analogWrite(y_motor_speed_pin,0);
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
