import serial
import time
import threading
import logging

logger = logging.getLogger('main_logger')
logger.setLevel(logging.DEBUG)
logging_format = logging.Formatter('  %(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

fileHandler = logging.FileHandler(filename="./software_log.log")
fileHandler.setFormatter(logging_format)
logger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logging_format)
logger.addHandler(consoleHandler)

class linear_displacement:
    def __init__(self,portname=None):
        self.serial_port = serial.Serial(port=portname,baudrate=9600,timeout=0.5)
        self.data_list = []
        self.temp_data = ""
        self.serial_state = 0
        self.run_mthread = True
        self.displacement_thread = None

    def run(self):
        self.displacement_thread = threading.Thread(target=self.read_data,)
        self.run_mthread = True
        self.displacement_thread.start()

    def read_data(self):
        while self.run_mthread:
            if self.serial_port.inWaiting():
            # if self.serial_port.in_waiting():   
                input_char = self.serial_port.read()
                if ord(input_char) == 0:
                    # logger.debug(self.temp_data)
                    try:
                        self.data_list.append(self.temp_data)
                        self.temp_data = ""
                    except:
                        self.temp_data = ""
                elif ord(input_char) >= 80:
                    self.temp_data = ""
                else:
                    self.temp_data = self.temp_data + input_char.decode()
            time.sleep(0.005)


    def stop(self):
        self.run_mthread = False
        self.displacement_thread.join()
        self.serial_port.close()
        self.displacement_thread = None

    def get_last(self):
        return_value = None
        if len(self.data_list) > 0:
            return_value = self.data_list[-1]
            self.data_list = []
        return return_value

    def get_data(self):
        return_value = None
        if len(self.data_list) > 0:
            return_value = self.data_list[0]
            self.data_list.pop(0)
        return return_value

    def clear_data(self):
        self.data_list = []

if __name__ == "__main__":
    print("11111")
    # dd = linear_displacement(portname="COM17")
    # dd.run()
    # in_data = dd.get_data()
    # while True:
    #     in_data = dd.get_data()
    #     if in_data != None:
    #         logger.debug(in_data)
    #     time.sleep(0.01)
    # for i in range(1000):
    #     int_data = dd.get_data()
    #     if int_data != None:
    #         logger.debug(int_data)
    #     time.sleep(0.01)
    # dd.stop()
    # dd.run()
    # for i in range(3000):
    #     int_data = dd.get_data()
    #     if int_data != None:
    #         logger.debug(int_data)
    #     time.sleep(0.01)
    # dd.stop()