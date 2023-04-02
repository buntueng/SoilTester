const int x_loadcell_pin = A13;

const int x_motor_dir1 = 7;
const int x_motor_dir2 = 5;
const int x_motor_speed_pin = 3;
// limit switches
const int x_limit_front = 18;
const int x_limit_back = 16;

bool execute_cmd = false;
String cmd_string = "";

int pwm_xaxis = 0;
int cyclic_ms = 0;
int x_max_displacement = 0;
int x_min_displacement = 0;
int x_distance = 0;
int x_loadcell = 0;


int pwm_yaxis = 0;
int y_distance = 0;
int y_max_displacement = 0;
int y_loadcell = 0;
int y_weight = 0;

bool run_machine = false;
int x_axis_state_machine = true;

unsigned long loadcell_timer = 0;
void setup()
{
    Serial.begin(115200);
    //============ setup motor pin ================
    pinMode(x_motor_dir1,OUTPUT);
    pinMode(x_motor_dir2,OUTPUT);
    pinMode(x_loadcell_pin,INPUT);
    pinMode(x_motor_speed_pin,OUTPUT);

    pinMode(x_limit_front,INPUT_PULLUP);
    pinMode(x_limit_back,INPUT_PULLUP);
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
    // Serial.print(digitalRead(x_limit_front));
    // Serial.print(',');
    // Serial.println(analogRead(x_loadcell_pin));
    // delay(10);

    if(execute_cmd)
    {
        int cmd_len = cmd_string.length();
        switch(cmd_string[0])
        {
            case 'S':   // set pwm to x-axis range from 0 to 255 [0-100%]
            {
                pwm_xaxis = cmd_string.substring(1,cmd_len).toInt();
                break;
            }
            case 'C':   // cyclic time in milliseconds [not less than 1000]
            {
                cyclic_ms = cmd_string.substring(1,cmd_len).toInt();
                break;
            }
            case 'D':   // maximum displacement in micrometers
            {
                x_max_displacement = cmd_string.substring(1,cmd_len).toInt();
                break;
            }
            case 'M':   // minimum displacement in micrometers
            {
                x_min_displacement = cmd_string.substring(1,cmd_len).toInt();
                break;
            }
            case 'X':
            {
                x_distance = cmd_string.substring(1,cmd_len).toInt();
                break;
            }
            // //======== parameters on Y axis ==========
            // case 'P':   // set pwm to y-axis range from 0 to 255 [0-100%]
            // {
            //     pwm_yaxis = cmd_string.substring(1,cmd_len).toInt();
            //     break;
            // }
            // case 'U':
            // {
            //     y_max_displacement = cmd_string.substring(1,cmd_len).toInt();
            //     break;
            // }
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
        if(present_time-loadcell_timer >= 10)
        {
            int x_loadcell_value = analogRead(x_loadcell_pin);
            Serial.print('X = ');
            Serial.println(x_loadcell_value);
            loadcell_timer = present_time;
        }
        // ==============x axis state machine =====================
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
            // if((digitalRead(x_limit_front)==1) || (x_distance >= x_max_displacement))
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
            // Serial.println("case3");
            break;
        }
        case 4:
        {
            // if((digitalRead(x_limit_back)==1) || (x_distance <= x_min_displacement))
            if((digitalRead(x_limit_back)==1) )
            {
                digitalWrite(x_motor_dir1,LOW);
                digitalWrite(x_motor_dir2,LOW);
                analogWrite(x_motor_speed_pin,0);
                x_axis_state_machine = 1;
                // Serial.println("case4");
            }
            break;
        }
        // delay(1000);
        default:
            break;
        }

    }
    
}
