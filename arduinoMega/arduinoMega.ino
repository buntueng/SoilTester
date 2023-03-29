bool execute_cmd = false;
String cmd_string = "";

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
        Serial.println(cmd_string);
        execute_cmd = false;
        cmd_string = "";
    }
    
}