import customtkinter as ctk
import tkinter as tk
import os
from PIL import Image
import serial as ser
import sys
import glob
import logging
from tkinter import messagebox
from get_data_displacement import linear_displacement
import time

# ======================== add logging =========================
logger = logging.getLogger('main_logger_soil_test')
logger.setLevel(logging.DEBUG)
logging_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

fileHandler = logging.FileHandler(filename="./software_log.log")
fileHandler.setFormatter(logging_format)
logger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logging_format)
logger.addHandler(consoleHandler)


ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
thai_large_font =("TH Niramit AS", 27,"bold")
thai_mid_font =("TH Niramit AS", 20,"bold")
eng_font = ("Time New Roman",25)

class App(ctk.CTk):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs,)
        self.resizable(False,False)
        # self.geometry("1550x900")

        self.title("SOILD TEST")
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "image")
        self.large_test_image = ctk.CTkImage(Image.open(os.path.join(image_path, "image1.png")), size=(1100, 600))  
        configulation_frame_colors = "azure3"
        #====================================== frame =====================================================
        self.master_frame = ctk.CTkFrame(self,fg_color="powderblue")
        self.master_frame.grid(row=0,column = 0)

        self.image_frame = ctk.CTkFrame(self.master_frame,fg_color="blanchedalmond",corner_radius=20,)
        self.image_frame .grid(row=0,column=0,padx=5,pady=(5,0))
        
        self.configuration_frame = ctk.CTkFrame(self.master_frame,fg_color="azure3",corner_radius=20)
        self.configuration_frame.grid(row=0,column=1,padx=(0,5),pady=5,ipady=161,sticky=tk.NE)

        self.monitor_frame = ctk.CTkFrame(self.master_frame,fg_color="azure3",corner_radius=20)
        self.monitor_frame.grid(row=1,column=0,padx=5,pady=5,sticky=tk.NW)

        self.button_frame = ctk.CTkFrame(self.master_frame,fg_color="powderblue")
        self.button_frame.grid(row=1,column=1,padx=(5,0),pady=(90,0),sticky=tk.NW)
        #======================================== BG ========================================
        # self.image_label = ctk.CTkLabel(self, text="", image=self.bg_image)
        # self.image_label.grid(row=0, column=0,)
        #====================================== object ====================================================
        image_fg_colors = "blanchedalmond"
        self.image_label = ctk.CTkLabel(self.image_frame, text="", image=self.large_test_image)
        # self.image_motor_x_label = ctk.CTkLabel(self.image_frame,text="ความเร็วมอเตอร์แกนX",bg_color=image_fg_colors,text_color="red",font=thai_large_font)
        # self.image_motor_x_entry = ctk.CTkEntry(self.image_frame,bg_color=image_fg_colors,text_color="red",font=thai_large_font,corner_radius=20)
        self.image_pressure_x_label = ctk.CTkLabel(self.image_frame,text="DISPLACEMENT แกนX",bg_color=image_fg_colors,text_color="red",font=thai_large_font)
        self.image_pressure_x_entry = ctk.CTkEntry(self.image_frame,bg_color=image_fg_colors,text_color="red",font=thai_large_font,corner_radius=20)
        self.image_dimention_x_label = ctk.CTkLabel(self.image_frame,text="DAIMENTION แกนX",bg_color=image_fg_colors,text_color="red",font=thai_large_font)
        self.image_dimention_x_entry = ctk.CTkEntry(self.image_frame,bg_color=image_fg_colors,text_color="red",font=thai_large_font,corner_radius=20)            
        # self.image_motor_Y_label = ctk.CTkLabel(self.image_frame,text="ความเร็วมอเตอร์แกนY",bg_color=image_fg_colors,text_color="red",font=thai_large_font)
        # self.image_motor_Y_entry = ctk.CTkEntry(self.image_frame,bg_color=image_fg_colors,text_color="red",font=thai_large_font,corner_radius=20)
        self.image_pressure_Y_label = ctk.CTkLabel(self.image_frame,text="DISPLACEMENT แกนY",bg_color=image_fg_colors,text_color="red",font=thai_large_font)
        self.image_pressure_Y_entry = ctk.CTkEntry(self.image_frame,bg_color=image_fg_colors,text_color="red",font=thai_large_font,corner_radius=20)
        self.image_dimention_Y_label = ctk.CTkLabel(self.image_frame,text="DAIMENTION แกนY",bg_color=image_fg_colors,text_color="red",font=thai_large_font)
        self.image_dimention_Y_entry = ctk.CTkEntry(self.image_frame,bg_color=image_fg_colors,text_color="red",font=thai_large_font,corner_radius=20)     


        self.image_label.grid(row=0, column=0, padx=20, pady=10)
        # self.image_motor_x_label.grid(row=0, column=0, padx=(45,0), pady=(90,0),sticky=tk.W)
        # self.image_motor_x_entry.grid(row=0, column=0, padx=(65,0), pady=(170,0),sticky=tk.W)
        self.image_pressure_x_label.grid(row=0, column=0, padx=(940,0), pady=(385,0),sticky=tk.W)
        self.image_pressure_x_entry.grid(row=0, column=0, padx=(791,0), pady=(385,0),sticky=tk.W) 
        self.image_dimention_x_label.grid(row=0, column=0, padx=(940,0), pady=(280,0),sticky=tk.W)
        self.image_dimention_x_entry.grid(row=0, column=0, padx=(791,0), pady=(280,0),sticky=tk.W)          
        # self.image_motor_Y_label.grid(row=0, column=0, padx=(870,0), pady=(20,0),sticky=tk.NW)
        # self.image_motor_Y_entry.grid(row=0, column=0, padx=(870,0), pady=(50,0),sticky=tk.NW)
        self.image_pressure_Y_label.grid(row=0, column=0, padx=(830,0), pady=(238,0),sticky=tk.N)
        self.image_pressure_Y_entry.grid(row=0, column=0, padx=(480,0), pady=(238,0),sticky=tk.N) 
        self.image_dimention_Y_label.grid(row=0, column=0, padx=(810,0), pady=(290,0),sticky=tk.N)
        self.image_dimention_Y_entry.grid(row=0, column=0, padx=(480,0), pady=(290,0),sticky=tk.N)   
        #=================================== CONFIG FRAME ============================================
        
        # self.select_port.set("")
        self.com_port_label = ctk.CTkLabel(self.configuration_frame,text="คอมพอต",bg_color=configulation_frame_colors,text_color="red",font=thai_large_font)
        self.com_port_option = ctk.CTkOptionMenu(self.configuration_frame,width=100,height=40,values=[''])
        
        self.select_port = tk.StringVar
        # self.select_port.set("เลือกพอร์ต")
        # self.opt.setvar("123")
        self.list_available_port = ['']
        self.opt = tk.OptionMenu(self.configuration_frame, self.select_port, *self.list_available_port)
        self.opt.config(width=10, font=('TH Niramit AS', 16))
        

        self.com_conection_button = ctk.CTkButton(self.configuration_frame,width=50,height=40,text="CONNECT",font=thai_mid_font,command=self.connection_button_pressed)
        self.com_disconection_button = ctk.CTkButton(self.configuration_frame,width=50,height=40,text="DISCONNECT",font=thai_mid_font,command=self.disconnection_pressed)
        
        self.another_label = ctk.CTkLabel(self.configuration_frame,text="xxxxxxxxxxx",bg_color=configulation_frame_colors,text_color="red",font=thai_large_font)
        self.another_entry = ctk.CTkEntry(self.configuration_frame,width=150,height=40,font=eng_font,corner_radius=20)
        self.another_unit_label = ctk.CTkLabel(self.configuration_frame,text="xxxxx",bg_color=configulation_frame_colors,text_color="red",font=thai_large_font)
        self.speed_motor_X_label = ctk.CTkLabel(self.configuration_frame,text="ความเร็วมอเตอร์แกนX",bg_color=configulation_frame_colors,text_color="red",font=thai_large_font)
        self.speed_motor_X_entry = ctk.CTkEntry(self.configuration_frame,width=150,height=40,font=eng_font,corner_radius=20)
        self.speed_motor_X_unit_label = ctk.CTkLabel(self.configuration_frame,text="RPM",bg_color=configulation_frame_colors,text_color="red",font=thai_large_font)
        self.pressure_X_label = ctk.CTkLabel(self.configuration_frame,text="แรงกดแกนX",bg_color=configulation_frame_colors,text_color="red",font=thai_large_font)
        self.pressure_X_entry = ctk.CTkEntry(self.configuration_frame,width=150,height=40,font=eng_font,corner_radius=20)
        self.pressure_X_unit_label = ctk.CTkLabel(self.configuration_frame,text="N/M",bg_color=configulation_frame_colors,text_color="red",font=thai_large_font)
        self.speed_motor_Y_label = ctk.CTkLabel(self.configuration_frame,text="ความเร็วมอเตอร์แกนY",bg_color=configulation_frame_colors,text_color="red",font=thai_large_font)
        self.speed_motor_Y_entry = ctk.CTkEntry(self.configuration_frame,width=150,height=40,font=eng_font,corner_radius=20)
        self.speed_motor_Y_unit_label = ctk.CTkLabel(self.configuration_frame,text="RPM",bg_color=configulation_frame_colors,text_color="red",font=thai_large_font)
        self.pressure_Y_label = ctk.CTkLabel(self.configuration_frame,text="แรงกดแกนY",bg_color=configulation_frame_colors,text_color="red",font=thai_large_font)
        self.pressure_Y_entry = ctk.CTkEntry(self.configuration_frame,width=150,height=40,font=eng_font,corner_radius=20)
        self.pressure_Y_unit_label = ctk.CTkLabel(self.configuration_frame,text="N/M",bg_color=configulation_frame_colors,text_color="red",font=thai_large_font)
        self.clear_button_entry = ctk.CTkButton(self.configuration_frame,text = "CLEAR",width=150,height=40,font=eng_font,corner_radius=20,command=self.clear_button_pressed)


        self.com_port_label.grid(row=0,column=0,padx=5,pady=5,ipadx = 5,sticky=tk.NW)
        # self.com_port_option.grid(row=0, column=0, padx=(110,5), pady=(10, 10))

        self.opt.grid(row=0, column=0, padx=(110,5), pady=(10, 10))

        self.com_conection_button.grid(row=0, column=1, padx=(5,5), pady=(10, 10),sticky=tk.NW)
        self.com_disconection_button.grid(row=0, column=1, padx=(70,5), pady=(10, 10),columnspan = 3)
        self.another_label.grid(row=1, column=0, padx=10,sticky=tk.NW)
        self.another_entry.grid(row=1, column=1, padx=(0,5))
        self.another_unit_label.grid(row=1, column=2, padx=(0,5))
        self.speed_motor_X_label.grid(row=2,column=0,padx=5,pady=(12,0),ipadx = 5,sticky=tk.NW)
        self.speed_motor_X_entry.grid(row=2, column=1, padx=(0,5), pady=(10, 10))
        self.speed_motor_X_unit_label.grid(row=2, column=2, padx=(0,5), pady=(10, 10))
        self.pressure_X_label.grid(row=3, column=0, padx=10,sticky=tk.NW)
        self.pressure_X_entry.grid(row=3, column=1, padx=(0,5))
        self.pressure_X_unit_label.grid(row=3, column=2, padx=(0,5))
        self.speed_motor_Y_label.grid(row=4,column=0,padx=5,pady=(12,0),ipadx = 5,sticky=tk.NW)
        self.speed_motor_Y_entry.grid(row=4, column=1, padx=(0,5), pady=(10, 10))
        self.speed_motor_Y_unit_label.grid(row=4, column=2, padx=(0,5), pady=(10, 10))
        self.pressure_Y_label.grid(row=5, column=0, padx=10,sticky=tk.NW)
        self.pressure_Y_entry.grid(row=5, column=1, padx=(0,5))
        self.pressure_Y_unit_label.grid(row=5, column=2, padx=(0,5))
        self.clear_button_entry.grid(row=6, column=1, padx=(0,5),pady=10,sticky=tk.N)

        #===================================================== button ===========================================
        self.start_button = ctk.CTkButton(self.button_frame,width=200,height=75,text="เริ่มการทดสอบ",font=thai_large_font,command=self.start_button_pressed)
        self.stop_button = ctk.CTkButton(self.button_frame,width=200,height=75,text="หยุดการทดสอบ",font=thai_large_font,command=self.stop_button_pressed)        

        self.start_button.grid(row=0, column=0, padx=(0,5), pady=(10, 10),sticky=tk.NW)
        self.stop_button.grid(row=0, column=1, padx=10, pady=(10, 10),sticky=tk.NW)

        #================================================= MONITOR FRAME ========================================
        self.monitor_label = ctk.CTkLabel(self.monitor_frame,text="MONITOR",bg_color=configulation_frame_colors,text_color="red",font=eng_font)
        self.monitor_text_box = ctk.CTkTextbox(self.monitor_frame,width=1120,height=200,corner_radius=20,bg_color=configulation_frame_colors,text_color="red",font=thai_large_font)

        self.monitor_label.grid(row=0,column=0,padx=5,pady=5,ipadx = 5,sticky=tk.N)
        self.monitor_text_box.grid(row=1,column=0,padx=5,pady=5,ipadx = 5,sticky=tk.NW)

        self.start_machine = False
        self.stop_machine = False
        self.machine_state = 0
        self.ser_port = ser.Serial(baudrate = 115200,parity = ser.PARITY_NONE,   stopbits = ser.STOPBITS_ONE, bytesize = ser.EIGHTBITS,
        timeout=0.5,   inter_byte_timeout=0.1)        
        self.check_serial_port()
        self.disable_widgets()

    def disable_widgets(self):
        self.another_entry.configure(state="disabled")
        self.pressure_X_entry.configure(state="disabled")
        self.speed_motor_X_entry.configure(state="disabled")
        self.pressure_Y_entry.configure(state="disabled")
        self.speed_motor_Y_entry.configure(state="disabled")
        self.image_pressure_x_entry.configure(state="disabled")
        self.image_dimention_x_entry.configure(state="disabled")
        self.image_pressure_Y_entry.configure(state="disabled")
        self.image_dimention_Y_entry.configure(state="disabled")
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="disabled")
        self.monitor_text_box.configure(state="disabled")
        self.com_conection_button.configure(state="normal")
        self.com_disconection_button.configure(state="disabled")
        self.clear_button_entry.configure(state="disabled")

    def enable_widgets(self):
        self.another_entry.configure(state="normal")
        self.pressure_X_entry.configure(state="normal")
        self.speed_motor_X_entry.configure(state="normal")
        self.pressure_Y_entry.configure(state="normal")
        self.speed_motor_Y_entry.configure(state="normal")
        self.image_pressure_x_entry.configure(state="normal")
        self.image_dimention_x_entry.configure(state="normal")
        self.image_pressure_Y_entry.configure(state="normal")
        self.image_dimention_Y_entry.configure(state="normal")
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.monitor_text_box.configure(state="normal")
        self.com_conection_button.configure(state="disabled")
        self.com_disconection_button.configure(state="normal")
        self.clear_button_entry.configure(state="normal")

    def start_button_widgets(self):
        self.another_entry.configure(state="disabled")
        self.pressure_X_entry.configure(state="disabled")
        self.speed_motor_X_entry.configure(state="disabled")
        self.pressure_Y_entry.configure(state="disabled")
        self.speed_motor_Y_entry.configure(state="disabled")
        self.image_pressure_x_entry.configure(state="disabled")
        self.image_dimention_x_entry.configure(state="disabled")
        self.image_pressure_Y_entry.configure(state="disabled")
        self.image_dimention_Y_entry.configure(state="disabled")
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.monitor_text_box.configure(state="normal")
        self.com_disconection_button.configure(state="normal")
        self.clear_button_entry.configure(state="disabled")

    def stop_button_widgets(self):
        self.another_entry.configure(state="normal")
        self.pressure_X_entry.configure(state="normal")
        self.speed_motor_X_entry.configure(state="normal")
        self.pressure_Y_entry.configure(state="normal")
        self.speed_motor_Y_entry.configure(state="normal")
        self.image_pressure_x_entry.configure(state="normal")
        self.image_dimention_x_entry.configure(state="normal")
        self.image_pressure_Y_entry.configure(state="normal")
        self.image_dimention_Y_entry.configure(state="normal")
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.monitor_text_box.configure(state="disabled") 
        self.com_disconection_button.configure(state="normal")
        self.clear_button_entry.configure(state="normal")

    def clear_button_pressed(self):
        self.speed_motor_X_entry.delete(0,'end')
        self.pressure_X_entry.delete(0,'end')
        self.speed_motor_Y_entry.delete(0,'end')
        self.pressure_Y_entry.delete(0,'end')
        self.another_entry.delete(0,'end')

    def check_serial_port(self):
        list_available_port = self.list_serial_ports()
        print((list_available_port))
        if len(list_available_port) == 0:
            # self.com_port_option.set("เลือกพอต")
            self.after(200,self.check_serial_port)

        else:
            menu = self.opt["menu"]
            menu.delete(0, "end")
            print(type(menu))
            for list_c in list_available_port:
                 menu.add_command(label=list_c,command=lambda value=list_c: self.select_port.set(value))


    def list_serial_ports(self):
            if sys.platform.startswith('win'):
                ports = ['COM%s' % (i + 1) for i in range(2,20)]
            elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
                # this excludes your current terminal "/dev/tty"
                ports = glob.glob('/dev/tty[A-Za-z]*')
            elif sys.platform.startswith('darwin'):
                ports = glob.glob('/dev/tty.*')
            else:
                raise EnvironmentError('Unsupported platform')
            result = []
            for port in ports:
                try:
                    s = ser.Serial(port)
                    s.close()
                    result.append(port)
                except (OSError, ser.SerialException):
                    pass
            return result

    # def listToString(self):
    #     s = self.com_port_option.get()
    #     str1 = ""
    #     for ele in s:
    #         str1 += ele
    #     return str1
 
    def connection_button_pressed(self):
        self.machine_state = 0
        self.run_machine()
       
    def disconnection_pressed(self):
        print("DISCONECT")
        self.ser_port.close()
        self.disable_widgets()
        self.machine_state = 0
        messagebox.showinfo("DISABLE","DISABLE COM PORT")
        self.com_conection_button.configure(state="normal")
        self.com_disconection_button.configure(state="disabled")
        self.after(300,self.check_serial_port)
    
    def start_button_pressed(self):
        self.start_machine = True
        self.start_button_widgets()
        self.speed_motor_X_entry.delete(0,'end')
        self.after(500,self.run_machine)

    def stop_button_pressed(self):
        self.machine_state = 1
        self.start_machine = False
        self.stop_button_widgets()
        self.after(500,self.run_machine)

    def run_machine(self):
        logger.debug(self.machine_state)
        # data = linear_displacement.get_data()
        # print(data)
        match self.machine_state:
            case 0:
                logger.debug(self.com_port_option.get())
                self.port_name = self.com_port_option.get()[0]
                if len(self.port_name) >= 4:
                    self.ser_port.port = self.port_name
                    if not self.ser_port.is_open:
                        try:
                            self.ser_port.open()
                            logger.debug('try to open port')
                        except BaseException as exc:
                            logger.error(exc)
                    self.machine_state = 1
                    self.after(3000,self.run_machine)
            case 1:
                if self.ser_port.is_open:
                    self.enable_widgets()
                    self.machine_state = 2
                    logger.debug("port is open")
                else:
                    self.machine_state = 0
                    self.disable_widgets()
            case 2:
                if self.start_machine:
                    speed_motor_x = self.speed_motor_X_entry.get()
                    pressure_X = self.pressure_X_entry.get()
                    speed_motor_Y = self.speed_motor_Y_entry.get()
                    pressure_Y = self.pressure_Y_entry.get()
                    if speed_motor_x != "" and pressure_X != "" and speed_motor_Y !="" and pressure_Y != "":
                        logger.debug("all params filled")
                        param = (f'{speed_motor_x},{pressure_X},{speed_motor_Y},{pressure_Y}\n')
                        param = param.encode()
                        self.ser_port.write(param)
                        print(param)
                        self.after(200,self.run_machine)
                        self.machine_state = 3
                    else:
                        logger.debug("some params is empty")

            case 3:
                # print("state3")
                if self.ser_port.inWaiting():
                    self.read_cmd = self.ser_port.readline().rstrip().decode()
                    print(self.read_cmd)
                    if self.read_cmd =="OK":
                        self.machine_state =4
                self.after(200,self.run_machine)
                
            case 4:
                self.after(200,self.run_machine)

            case 5:
                pass

            case _:
                # self.after(500,self.run_machine)
                # logger.error("NOT RUN MACHINE")
                pass
        # dd = linear_displacement(portname="COM4")
        # dd.run()
        # for i in range(1000):
        #     int_data = dd.get_data()
        #     if int_data != None:
        #         logger.debug(int_data)
        #     time.sleep(0.01)
        # dd.stop()




if __name__ == "__main__":
    app = App()
    app.eval('tk::PlaceWindow . center')
    app.mainloop()
