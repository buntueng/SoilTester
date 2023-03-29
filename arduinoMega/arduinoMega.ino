bool execute_cmd = false;
String cmd_string = "";

int pwm_xaxis = 0;
int cyclic_ms = 0;
int x_max_displacement = 0;
int x_distance = 0;
int x_loadcell = 0;


int pwm_yaxis = 0;
int y_distance = 0;
int y_max_displacement = 0;
int y_loadcell = 0;
int y_weight = 0;

bool run_machine = false;
int state_machine = true;
void setup()
{
    Serial.begin(115200);
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
            //======== parameters on Y axis ==========
            case 'P':   // set pwm to y-axis range from 0 to 255 [0-100%]
            {
                pwm_yaxis = cmd_string.substring(1,cmd_len).toInt();
                break;
            }
            case 'U':
            {
                y_max_displacement = cmd_string.substring(1,cmd_len).toInt();
                break;
            }
            // =============== run and terminate flag ====================
            case 'R':       // run state machine
            {
                state_machine = 0;
                run_machine = true;
                break;
            }
            case 'T':       // terminate state machine
            {
                run_machine = false;
                break;
            }
            // =========== check command =================
            case 'G':
            {
                Serial.print(pwm_xaxis);
                Serial.print(",");
                Serial.print(cyclic_ms);
                Serial.print(",");
                Serial.print(x_max_displacement);
                Serial.print(",");
                Serial.print(pwm_yaxis);
                Serial.print(",");
                Serial.println(y_max_displacement);
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

    }
    
}