import os
import machine
from time import sleep
uart = machine.UART(0, 115200,timeout=1)
print(uart)
uart.write(b'hhh')
b = None
msg = ""
while True:
    if uart.any():
        b = uart.readline()
        print(type(b))
        print(b)
        try:
            msg = b.decode('utf-8')
            print(type(msg))
            print(">> " + msg)
        except:
            pass