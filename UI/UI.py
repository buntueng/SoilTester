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
import math


debug = True

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
        super().__init__(*args, **kwargs)
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
        self.configuration_frame.grid(row=0,column=1,padx=(0,10),pady=(10,0),ipady=15,sticky=tk.NE)

        self.monitor_frame = ctk.CTkFrame(self.master_frame,fg_color="azure3",corner_radius=20)
        self.monitor_frame.grid(row=1,column=0,padx=5,pady=5,sticky=tk.NW)

        self.button_frame = ctk.CTkFrame(self.master_frame,fg_color="powderblue")
        self.button_frame.grid(row=1,column=1,padx=(5,0),pady=(90,0),sticky=tk.NW)
        #======================================== BG ========================================
        # self.image_label = ctk.CTkLabel(self, text="", image=self.bg_image)
        # self.image_label.grid(row=0, column=0,)
        #====================================== object ====================================================
        self.image_dimention_x_string = tk.StringVar()
        self.image_dimention_y_string = tk.StringVar()
        image_fg_colors = "blanchedalmond"
        self.image_label = ctk.CTkLabel(self.image_frame, text="", image=self.large_test_image)
        self.image_pressure_x_label = ctk.CTkLabel(self.image_frame,text="แรงกด แกนX",bg_color=image_fg_colors,text_color="red",font=thai_large_font)
        self.image_pressure_x_entry = ctk.CTkEntry(self.image_frame,bg_color=image_fg_colors,text_color="red",font=thai_large_font,corner_radius=20)
        self.image_dimention_x_label = ctk.CTkLabel(self.image_frame,text="DISPLACEMENT แกนX",bg_color=image_fg_colors,text_color="red",font=thai_large_font)
        self.image_dimention_x_entry = ctk.CTkEntry(self.image_frame,bg_color=image_fg_colors,text_color="red",font=thai_large_font,corner_radius=20,textvariable=self.image_dimention_x_string)            
        self.image_pressure_Y_label = ctk.CTkLabel(self.image_frame,text="แรงกด แกนY",bg_color=image_fg_colors,text_color="red",font=thai_large_font)
        self.image_pressure_Y_entry = ctk.CTkEntry(self.image_frame,bg_color=image_fg_colors,text_color="red",font=thai_large_font,corner_radius=20)
        self.image_dimention_Y_label = ctk.CTkLabel(self.image_frame,text="DISPLACEMENT แกนY",bg_color=image_fg_colors,text_color="red",font=thai_large_font)
        self.image_dimention_Y_entry = ctk.CTkEntry(self.image_frame,bg_color=image_fg_colors,text_color="red",font=thai_large_font,corner_radius=20,textvariable=self.image_dimention_y_string)     


        self.image_label.grid(row=0, column=0, padx=20, pady=10)
        self.image_pressure_x_label.grid(row=0, column=0, padx=(940,0), pady=(385,0),sticky=tk.W)
        self.image_pressure_x_entry.grid(row=0, column=0, padx=(791,0), pady=(385,0),sticky=tk.W) 
        self.image_dimention_x_label.grid(row=0, column=0, padx=(940,0), pady=(280,0),sticky=tk.W)
        self.image_dimention_x_entry.grid(row=0, column=0, padx=(791,0), pady=(280,0),sticky=tk.W)          
        self.image_pressure_Y_label.grid(row=0, column=0, padx=(750,0), pady=(295,0),sticky=tk.N)
        self.image_pressure_Y_entry.grid(row=0, column=0, padx=(480,0), pady=(290,0),sticky=tk.N) 
        self.image_dimention_Y_label.grid(row=0, column=0, padx=(830,0), pady=(238,0),sticky=tk.N)
        self.image_dimention_Y_entry.grid(row=0, column=0, padx=(480,0), pady=(238,0),sticky=tk.N)   
        #=================================== CONFIG FRAME ============================================
        self.select_port = tk.StringVar

        self.com_port_CT_X_label = ctk.CTkLabel(self.configuration_frame,text="CONTROL X",bg_color=configulation_frame_colors,text_color="red",font=thai_large_font)
        self.com_port_CT_X = ctk.CTkOptionMenu(self.configuration_frame,width=100,height=40,values=[""])
        self.com_conection_button_CT_X = ctk.CTkButton(self.configuration_frame,width=100,height=40,text="CONNECT",font=thai_mid_font,command=self.run_CT_x)
        self.com_disconection_button_CT_X = ctk.CTkButton(self.configuration_frame,width=100,height=40,text="DISCONNECT",font=thai_mid_font,command=self.disconnection_CT_X_pressed)
        self.com_port_CT_X.set("เลือกพอต")

        self.com_port_dis_X_label = ctk.CTkLabel(self.configuration_frame,text="DIS X",bg_color=configulation_frame_colors,text_color="red",font=thai_large_font)
        self.com_port_dis_X = ctk.CTkOptionMenu(self.configuration_frame,width=100,height=40,values=[""])
        self.com_port_dis_X.set("เลือกพอต")

        self.com_port_CT_Y_label = ctk.CTkLabel(self.configuration_frame,text="CONTROL Y",bg_color=configulation_frame_colors,text_color="red",font=thai_large_font)
        self.com_port_CT_Y = ctk.CTkOptionMenu(self.configuration_frame,width=100,height=40,values=[""])
        self.com_port_CT_Y.set("เลือกพอต")

        self.com_port_dis_Y_label = ctk.CTkLabel(self.configuration_frame,text="DIS Y",bg_color=configulation_frame_colors,text_color="red",font=thai_large_font)
        self.com_port_dis_Y = ctk.CTkOptionMenu(self.configuration_frame,width=100,height=40,values=[""])
        self.com_port_dis_Y.set("เลือกพอต")

        self.cyclic_label = ctk.CTkLabel(self.configuration_frame,text="CYCLIC",bg_color=configulation_frame_colors,text_color="red",font=thai_large_font)
        self.cyclic_entry = ctk.CTkEntry(self.configuration_frame,width=150,height=40,font=eng_font,corner_radius=20,placeholder_text="0-1000")
        self.cyclic_unit_label = ctk.CTkLabel(self.configuration_frame,text="RPM",bg_color=configulation_frame_colors,text_color="red",font=thai_large_font)
        self.speed_motor_X_label = ctk.CTkLabel(self.configuration_frame,text="ความเร็วมอเตอร์แกนX",bg_color=configulation_frame_colors,text_color="red",font=thai_large_font)
        self.speed_motor_X_entry = ctk.CTkEntry(self.configuration_frame,width=150,height=40,font=eng_font,corner_radius=20,placeholder_text="0-100%")
        self.speed_motor_X_unit_label = ctk.CTkLabel(self.configuration_frame,text="PWM",bg_color=configulation_frame_colors,text_color="red",font=thai_large_font)
        self.pressure_X_label = ctk.CTkLabel(self.configuration_frame,text="แรงกดแกนX",bg_color=configulation_frame_colors,text_color="red",font=thai_large_font)
        self.pressure_X_entry = ctk.CTkEntry(self.configuration_frame,width=150,height=40,font=eng_font,corner_radius=20,placeholder_text="0 - 10kg")
        self.pressure_X_unit_label = ctk.CTkLabel(self.configuration_frame,text="N",bg_color=configulation_frame_colors,text_color="red",font=thai_large_font)

        self.MIN_X_label = ctk.CTkLabel(self.configuration_frame,text="MIN X",bg_color=configulation_frame_colors,text_color="red",font=thai_large_font)
        self.MIN_X_entry = ctk.CTkEntry(self.configuration_frame,width=90,height=40,font=eng_font,corner_radius=20,placeholder_text="0-4uM")
        self.MIN_X_unit_label = ctk.CTkLabel(self.configuration_frame,text="mm",bg_color=configulation_frame_colors,text_color="red",font=thai_large_font)
        
        self.MAX_X_label = ctk.CTkLabel(self.configuration_frame,text="MAX X",bg_color=configulation_frame_colors,text_color="red",font=thai_large_font)
        self.MAX_X_entry = ctk.CTkEntry(self.configuration_frame,width=90,height=40,font=eng_font,corner_radius=20,placeholder_text="0-4uM")
        self.MAX_X_unit_label = ctk.CTkLabel(self.configuration_frame,text="mm",bg_color=configulation_frame_colors,text_color="red",font=thai_large_font)

        self.speed_motor_Y_label = ctk.CTkLabel(self.configuration_frame,text="ความเร็วมอเตอร์แกนY",bg_color=configulation_frame_colors,text_color="red",font=thai_large_font)
        self.speed_motor_Y_entry = ctk.CTkEntry(self.configuration_frame,width=150,height=40,font=eng_font,corner_radius=20,placeholder_text="0-100%")
        self.speed_motor_Y_unit_label = ctk.CTkLabel(self.configuration_frame,text="PWM",bg_color=configulation_frame_colors,text_color="red",font=thai_large_font)
        self.pressure_Y_label = ctk.CTkLabel(self.configuration_frame,text="แรงกดแกนY",bg_color=configulation_frame_colors,text_color="red",font=thai_large_font)
        self.pressure_Y_entry = ctk.CTkEntry(self.configuration_frame,width=150,height=40,font=eng_font,corner_radius=20,placeholder_text="0-10kg")
        self.pressure_Y_unit_label = ctk.CTkLabel(self.configuration_frame,text="N",bg_color=configulation_frame_colors,text_color="red",font=thai_large_font)
        self.clear_button_entry = ctk.CTkButton(self.configuration_frame,text = "CLEAR",width=150,height=40,font=eng_font,corner_radius=20,command=self.clear_button_pressed)

        self.MIN_Y_label = ctk.CTkLabel(self.configuration_frame,text="MIN Y",bg_color=configulation_frame_colors,text_color="red",font=thai_large_font)
        self.MIN_Y_entry = ctk.CTkEntry(self.configuration_frame,width=90,height=40,font=eng_font,corner_radius=20,placeholder_text="0-4uM")
        self.MIN_Y_unit_label = ctk.CTkLabel(self.configuration_frame,text="mm",bg_color=configulation_frame_colors,text_color="red",font=thai_large_font)

        self.MAX_Y_label = ctk.CTkLabel(self.configuration_frame,text="MAX Y",bg_color=configulation_frame_colors,text_color="red",font=thai_large_font)
        self.MAX_Y_entry = ctk.CTkEntry(self.configuration_frame,width=90,height=40,font=eng_font,corner_radius=20,placeholder_text="0-4uM")
        self.MAX_Y_unit_label = ctk.CTkLabel(self.configuration_frame,text="mm",bg_color=configulation_frame_colors,text_color="red",font=thai_large_font)


        self.com_port_CT_X_label.grid(row=0,column=0,padx=(5,0),pady=(10,0),ipadx = 5,sticky=tk.NW)
        self.com_port_CT_X.grid(row=0, column=0, padx=(115,0), pady=(10, 0),columnspan = 3,sticky=tk.NW)

        self.com_port_dis_X_label.grid(row=0,column=0,padx=(150,0),pady=(10,0),columnspan = 2,sticky=tk.N)
        self.com_port_dis_X.grid(row=0, column=0, padx=(260,0),pady=(10,0),columnspan = 3,sticky=tk.N)

        self.com_port_CT_Y_label.grid(row=1,column=0,padx=(5,0),pady=(5,0),ipadx = 5,sticky=tk.NW)
        self.com_port_CT_Y.grid(row=1, column=0, padx=(115,0), pady=(5, 5),columnspan = 3,sticky=tk.NW)

        self.com_port_dis_Y_label.grid(row=1,column=0,padx=(150,0),pady=(5,0),columnspan = 2,sticky=tk.N)
        self.com_port_dis_Y.grid(row=1, column=0, padx=(260,0),pady=(5,0),columnspan = 3,sticky=tk.N)

        self.com_conection_button_CT_X.grid(row=2, column=0, padx=(115,5), pady=(0, 5),columnspan = 1,sticky=tk.N)
        self.com_disconection_button_CT_X.grid(row=2, column=0, padx=(265,5), pady=(0, 5),columnspan = 3,sticky=tk.N)

        self.cyclic_label.grid(row=4, column=0, padx=10,sticky=tk.NW)
        self.cyclic_entry.grid(row=4, column=1, padx=(0,5))
        self.cyclic_unit_label.grid(row=4, column=2, padx=(0,5))
        self.speed_motor_X_label.grid(row=5,column=0,padx=5,pady=(12,0),ipadx = 5,sticky=tk.NW)
        self.speed_motor_X_entry.grid(row=5, column=1, padx=(0,5), pady=(10, 10))
        self.speed_motor_X_unit_label.grid(row=5, column=2, padx=(0,5), pady=(10, 10),sticky=tk.NW)
        self.pressure_X_label.grid(row=6, column=0, padx=10,sticky=tk.NW)
        self.pressure_X_entry.grid(row=6, column=1, padx=(0,5))
        self.pressure_X_unit_label.grid(row=6, column=2, padx=(0,5),sticky=tk.NW)

        self.MIN_X_label.grid(row=7, column=0, padx=10,pady = (10,0),sticky=tk.NW)
        self.MIN_X_entry.grid(row=7, column=0, padx=(70,5),pady = (10,0),columnspan = 3,sticky=tk.NW)
        self.MIN_X_unit_label.grid(row=7, column=0, padx=(165,0),pady = (10,0),columnspan = 3,sticky=tk.NW)

        self.MAX_X_label.grid(row=7, column=0, padx=(225,0),pady = (10,0),sticky=tk.NW,columnspan = 3)
        self.MAX_X_entry.grid(row=7, column=0, padx=(245,0),pady = (10,0),sticky=tk.N,columnspan = 3)
        self.MAX_X_unit_label.grid(row=7, column=0, padx=(375,0),pady = (10,0),columnspan = 3,sticky=tk.N)

        self.speed_motor_Y_label.grid(row=8,column=0,padx=5,pady=(12,0),ipadx = 5,sticky=tk.NW)
        self.speed_motor_Y_entry.grid(row=8, column=1, padx=(0,5), pady=(10, 10))
        self.speed_motor_Y_unit_label.grid(row=8, column=2, padx=(0,5), pady=(10, 10),sticky=tk.NW)
        self.pressure_Y_label.grid(row=9, column=0, padx=10,sticky=tk.NW)
        self.pressure_Y_entry.grid(row=9, column=1, padx=(0,5))
        self.pressure_Y_unit_label.grid(row=9, column=2, padx=(0,5),sticky=tk.NW)

        self.MIN_Y_label.grid(row=10, column=0, padx=10,pady = (10,0),sticky=tk.NW)
        self.MIN_Y_entry.grid(row=10, column=0, padx=(70,5),pady = (10,0),columnspan = 3,sticky=tk.NW)
        self.MIN_Y_unit_label.grid(row=10, column=0, padx=(165,0),pady = (10,0),columnspan = 3,sticky=tk.NW)

        self.MAX_Y_label.grid(row=10, column=0, padx=(225,0),pady = (10,0),sticky=tk.NW,columnspan = 3)
        self.MAX_Y_entry.grid(row=10, column=0, padx=(245,0),pady = (10,0),sticky=tk.N,columnspan = 3)
        self.MAX_Y_unit_label.grid(row=10, column=0, padx=(375,0),pady = (10,0),columnspan = 3,sticky=tk.N)

        self.clear_button_entry.grid(row=11, column=1, padx=(0,5),pady=10,sticky=tk.N)

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

        


        self.ser_port_CT_X = ser.Serial(baudrate = 115200,parity = ser.PARITY_NONE,   stopbits = ser.STOPBITS_ONE, bytesize = ser.EIGHTBITS,
        timeout=0.5,   inter_byte_timeout=0.1)  

        self.ser_port_dis_X = ser.Serial(baudrate = 9600 ,parity = ser.PARITY_NONE,   stopbits = ser.STOPBITS_ONE, bytesize = ser.EIGHTBITS,
        timeout=0.5,   inter_byte_timeout=0.1)  
        
        self.ser_port_CT_Y = ser.Serial(baudrate = 115200 ,parity = ser.PARITY_NONE,   stopbits = ser.STOPBITS_ONE, bytesize = ser.EIGHTBITS,
        timeout=0.5,   inter_byte_timeout=0.1) 

        self.ser_port_dis_Y = ser.Serial(baudrate = 9600 ,parity = ser.PARITY_NONE,   stopbits = ser.STOPBITS_ONE, bytesize = ser.EIGHTBITS,
        timeout=0.5,   inter_byte_timeout=0.1)  

        self.stop_machine = False
        self.con_dis_x = False
        self.start_mc = False
        self.status_read_dis = False
        self.status_run_mc = False
        self.machine_state = 0
        self.start_read_dis = 0

        self.disable_widgets_ct_X()
        self.disable_widgets_dis_X()
        self.disable_widgets_CT_Y()
        self.disable_widgets_dis_Y()
        active_port_list = self.list_serial_ports()
        self.com_port_CT_X.configure(values=active_port_list)
        self.com_port_dis_X.configure(values = active_port_list)
        self.com_port_CT_Y.configure(values = active_port_list)
        self.com_port_dis_Y.configure(values = active_port_list)


    def disable_widgets_ct_X(self):
        self.com_disconection_button_CT_X.configure(state="disabled")
        self.com_conection_button_CT_X.configure(state="normal")
        self.image_pressure_x_label.configure(state="disabled")
        self.image_pressure_x_entry.configure(state="disabled")
        self.speed_motor_X_label.configure(state="disabled")
        self.speed_motor_X_entry.configure(state="disabled")
        self.pressure_X_label.configure(state="disabled")
        self.pressure_X_entry.configure(state="disabled")
        self.speed_motor_X_unit_label.configure(state="disabled")
        self.pressure_X_unit_label.configure(state="disabled")
        self.cyclic_label.configure(state="disabled")
        self.cyclic_entry.configure(state="disabled")
        self.cyclic_unit_label.configure(state="disabled")
        self.MIN_X_label.configure(state="disabled")
        self.MIN_X_entry.configure(state="disabled")
        self.MIN_X_unit_label.configure(state="disabled")
        self.MAX_X_label.configure(state="disabled")
        self.MAX_X_entry.configure(state="disabled")
        self.MAX_X_unit_label.configure(state="disabled")
        self.MIN_Y_label.configure(state="disabled")
        self.MIN_Y_entry.configure(state="disabled")
        self.MIN_Y_unit_label.configure(state="disabled")
        self.MAX_Y_label.configure(state="disabled")
        self.MAX_Y_entry.configure(state="disabled")
        self.MAX_Y_unit_label.configure(state="disabled")        
        self.stop_button.configure(state="disabled")

    def enable_widgets_ct_x(self):
        self.com_disconection_button_CT_X.configure(state="normal")
        self.com_conection_button_CT_X.configure(state="disabled")
        self.image_pressure_x_label.configure(state="normal")
        self.image_pressure_x_entry.configure(state="normal")
        self.speed_motor_X_label.configure(state="normal")
        self.speed_motor_X_entry.configure(state="normal")
        self.pressure_X_label.configure(state="normal")
        self.pressure_X_entry.configure(state="normal")
        self.speed_motor_X_unit_label.configure(state="normal")
        self.pressure_X_unit_label.configure(state="normal")
        self.cyclic_label.configure(state="normal")
        self.cyclic_entry.configure(state="normal")
        self.cyclic_unit_label.configure(state="normal")
        self.MIN_X_label.configure(state="normal")
        self.MIN_X_entry.configure(state="normal")
        self.MIN_X_unit_label.configure(state="normal")
        self.MAX_X_label.configure(state="normal")
        self.MAX_X_entry.configure(state="normal")
        self.MAX_X_unit_label.configure(state="normal")
        self.MIN_Y_label.configure(state="normal")
        self.MIN_Y_entry.configure(state="normal")
        self.MIN_Y_unit_label.configure(state="normal")
        self.MAX_Y_label.configure(state="normal")
        self.MAX_Y_entry.configure(state="normal")
        self.MAX_Y_unit_label.configure(state="normal")       

    def disable_widgets_dis_X(self):
        self.image_dimention_x_entry.configure(state="disabled")
        self.image_dimention_x_label.configure(state="disabled")
        
    def start_widgets(self):
        self.cyclic_label.configure(state="disabled")
        self.cyclic_entry.configure(state="disabled")
        self.cyclic_unit_label.configure(state="disabled")
        self.speed_motor_X_label.configure(state="disabled")
        self.speed_motor_X_entry.configure(state="disabled")
        self.pressure_X_label.configure(state="disabled")
        self.pressure_X_entry.configure(state="disabled")
        self.speed_motor_X_unit_label.configure(state="disabled")
        self.pressure_X_unit_label.configure(state="disabled")
        self.speed_motor_Y_label.configure(state="disabled")
        self.speed_motor_Y_entry.configure(state="disabled")
        self.speed_motor_Y_unit_label.configure(state="disabled")
        self.pressure_Y_label.configure(state="disabled")
        self.pressure_Y_entry.configure(state="disabled")
        self.pressure_Y_unit_label.configure(state="disabled")
        self.MIN_X_label.configure(state="disabled")
        self.MIN_X_entry.configure(state="disabled")
        self.MIN_X_unit_label.configure(state="disabled")
        self.MAX_X_label.configure(state="disabled")
        self.MAX_X_entry.configure(state="disabled")
        self.MAX_X_unit_label.configure(state="disabled")
        self.MIN_Y_label.configure(state="disabled")
        self.MIN_Y_entry.configure(state="disabled")
        self.MIN_Y_unit_label.configure(state="disabled")
        self.MAX_Y_label.configure(state="disabled")
        self.MAX_Y_entry.configure(state="disabled")
        self.MAX_Y_unit_label.configure(state="disabled")      

    def stop_widgets(self):
        self.cyclic_label.configure(state="normal")
        self.cyclic_entry.configure(state="normal")
        self.cyclic_unit_label.configure(state="normal")
        self.speed_motor_X_label.configure(state="normal")
        self.speed_motor_X_entry.configure(state="normal")
        self.pressure_X_label.configure(state="normal")
        self.pressure_X_entry.configure(state="normal")
        self.speed_motor_X_unit_label.configure(state="normal")
        self.pressure_X_unit_label.configure(state="normal")
        self.speed_motor_Y_label.configure(state="normal")
        self.speed_motor_Y_entry.configure(state="normal")
        self.speed_motor_Y_unit_label.configure(state="normal")
        self.pressure_Y_label.configure(state="normal")
        self.pressure_Y_entry.configure(state="normal")
        self.pressure_Y_unit_label.configure(state="normal")
        self.MIN_X_label.configure(state="normal")
        self.MIN_X_entry.configure(state="normal")
        self.MIN_X_unit_label.configure(state="normal")
        self.MAX_X_label.configure(state="normal")
        self.MAX_X_entry.configure(state="normal")
        self.MAX_X_unit_label.configure(state="normal")
        self.MIN_Y_label.configure(state="normal")
        self.MIN_Y_entry.configure(state="normal")
        self.MIN_Y_unit_label.configure(state="normal")
        self.MAX_Y_label.configure(state="normal")
        self.MAX_Y_entry.configure(state="normal")
        self.MAX_Y_unit_label.configure(state="normal")  

    def enable_widgets_dis_x(self):
        self.image_dimention_x_entry.configure(state="normal")
        self.image_dimention_x_label.configure(state="normal")

    def disable_widgets_CT_Y(self):
        self.speed_motor_Y_label.configure(state="disabled")
        self.speed_motor_Y_entry.configure(state="disabled")
        self.speed_motor_Y_unit_label.configure(state="disabled")
        self.pressure_Y_label.configure(state="disabled")
        self.pressure_Y_entry.configure(state="disabled")
        self.pressure_Y_unit_label.configure(state="disabled")
        self.image_pressure_Y_label.configure(state="disabled")
        self.image_pressure_Y_entry.configure(state="disabled")

    def enable_widgets_CT_Y(self):
        self.speed_motor_Y_label.configure(state="normal")
        self.speed_motor_Y_entry.configure(state="normal")
        self.speed_motor_Y_unit_label.configure(state="normal")
        self.pressure_Y_label.configure(state="normal")
        self.pressure_Y_entry.configure(state="normal")
        self.pressure_Y_unit_label.configure(state="normal")
        self.image_pressure_Y_label.configure(state="normal")
        self.image_pressure_Y_entry.configure(state="normal")

    def disable_widgets_dis_Y(self):
        self.image_dimention_Y_label.configure(state="disabled")
        self.image_dimention_Y_entry.configure(state="disabled")

    def enable_widgets_dis_Y(self):
        self.image_dimention_Y_label.configure(state="normal")
        self.image_dimention_Y_entry.configure(state="normal")

    def start_button_widgets(self):
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")

    def stop_button_widgets(self):
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")

    def clear_button_pressed(self):
        self.speed_motor_X_entry.delete(0,'end')
        self.pressure_X_entry.delete(0,'end')
        self.speed_motor_Y_entry.delete(0,'end')
        self.pressure_Y_entry.delete(0,'end')
        self.cyclic_entry.delete(0,'end')
        self.MIN_X_entry.delete(0,'end')
        self.MAX_X_entry.delete(0,'end')
        self.MIN_Y_entry.delete(0,'end')
        self.MAX_Y_entry.delete(0,'end')

    def run_check_serial(self):
        self.check_serial_port()

    def check_serial_port(self):
        list_available_port = self.list_serial_ports()
        if len(list_available_port) == 0:
            list_available_port = " "
        if len(list_available_port) > 0:
            self.com_port_CT_X.configure(values=list_available_port)
            self.com_port_dis_X.configure(values = list_available_port)
            self.com_port_CT_Y.configure(values = list_available_port)
            self.com_port_dis_Y.configure(values = list_available_port)

    def list_serial_ports(self):
            if sys.platform.startswith('win'):
                ports = ['COM%s' % (i + 1) for i in range(1,40)]
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

    def run_CT_x(self):
        self.con_CT_x_status = 0
        self.con_CT_x = True
        self.connection_CT_X_button_pressed()

    def connection_CT_X_button_pressed(self):

        CTX_port = self.com_port_CT_X.get()
        CTY_port = self.com_port_CT_Y.get()
        disX = self.com_port_dis_X.get()
        disY = self.com_port_dis_Y.get()

        self.selected_port_list = [CTX_port,CTY_port,disX,disY]
        # print(self.selected_port_list)
        locked_port = self.selected_port_list
        if len(set(self.selected_port_list))<4:
            self.com_port_CT_X.configure(state=tk.NORMAL)
            self.com_port_CT_Y.configure(state=tk.NORMAL)
            self.com_port_dis_X.configure(state=tk.NORMAL)
            self.com_port_dis_Y.configure(state=tk.NORMAL)
        else:
            # open all ports
            try:
                self.ser_port_CT_X.port = CTX_port
                self.ser_port_CT_Y.port = CTY_port
                self.ser_port_dis_X.port = disX
                self.ser_port_dis_Y.port = disY

                self.ser_port_CT_X.open()
                locked_port.remove(CTX_port)
                self.ser_port_CT_Y.open()
                locked_port.remove(CTY_port)
                self.ser_port_dis_X.open()
                # self.ser_port_dis_X.close()
                locked_port.remove(disX)
                self.ser_port_dis_Y.open()
                # self.ser_port_dis_Y.close()
                locked_port.remove(disY)
                self.enable_widgets_ct_x()
                self.enable_widgets_CT_Y()
                self.enable_widgets_dis_x()
                self.enable_widgets_dis_Y()
                self.com_port_CT_X.configure(state=tk.DISABLED)
                self.com_port_CT_Y.configure(state=tk.DISABLED)
                self.com_port_dis_X.configure(state=tk.DISABLED)
                self.com_port_dis_Y.configure(state=tk.DISABLED)
                # self.image_dimention_x_string.set(200)
            except:
                error_message = "busy port:\n"
                for port_name in locked_port:
                    error_message = error_message + port_name + "\n"
                tk.messagebox.showerror(title="พอร์ตที่ใช้งานไม่ได้", message=error_message,)
        
    def disconnection_CT_X_pressed(self):
        self.ser_port_CT_X.close()
        self.ser_port_CT_Y.close()
        self.ser_port_dis_X.close()
        self.ser_port_dis_Y.close()
        self.disable_widgets_ct_X()
        self.disable_widgets_dis_X()
        self.disable_widgets_CT_Y()
        self.disable_widgets_dis_Y()
        self.com_port_CT_X.configure(state=tk.NORMAL)
        self.com_port_CT_Y.configure(state=tk.NORMAL)
        self.com_port_dis_X.configure(state=tk.NORMAL)
        self.com_port_dis_Y.configure(state=tk.NORMAL)

    def start_button_pressed(self):
        self.start_read_dis = 0
        self.start_mc = 0
        self.status_read_dis = True
        self.status_run_mc = True
        self.read_displacement()
        self.start_button_widgets()
        self.start_widgets()
        self.after(500,self.run_mc)

    def stop_button_pressed(self):
        self.start_read_dis = 0
        self.start_mc = 0
        self.status_read_dis = False
        self.status_run_mc = False
        self.disx_obj.stop()
        self.disy_obj.stop()
        self.ser_port_dis_X.close()
        self.ser_port_dis_Y.close()
        self.image_dimention_x_entry.delete(0,'end')
        self.image_dimention_Y_entry.delete(0,'end')
        self.stop_widgets()
        self.stop_button_widgets()

    def read_displacement(self):
        match(self.start_read_dis):

            case 0:
                if self.status_read_dis == True:
                    self.start_read_dis = 1

            case 1:
                # create displacement object
                self.ser_port_dis_X.close()
                self.ser_port_dis_Y.close()
                self.disx_obj = linear_displacement(portname=self.com_port_dis_X.get())
                self.disy_obj = linear_displacement(portname=self.com_port_dis_Y.get())
                self.disx_obj.run()
                self.disy_obj.run()
                self.image_dimention_x_entry.configure(state="disabled")
                self.image_dimention_Y_entry.configure(state="disabled")
                self.start_read_dis = 2

            case 2:
                disx_length = self.disx_obj.get_data()
                disy_length = self.disy_obj.get_data()
                if disx_length != None:
                    try:
                        x_show3digit = f'{int(disx_length[:-2])*0.001:.3f}'
                        self.image_dimention_x_string.set(x_show3digit)
                        # logger.debug(x_show3digit)
                    except:
                        pass
                        # logger.error("Start disx_obj")

                if disy_length != None:
                    try:
                        Y_show3digit = f'{int(disy_length[:-2])*0.001:.3f}'
                        self.image_dimention_y_string.set(Y_show3digit)
                        # logger.debug(Y_show3digit)
                    except:
                        pass
                        # logger.error("Start disy_obj")                
        self.after(10,self.read_displacement)

    def run_mc (self):
        match(self.start_mc):
            
            case 0:
                if self.status_run_mc == True:
                    self.start_mc = 1
                    self.after(50,self.run_mc)

            case 1:
                if self.ser_port_CT_X.is_open:
                    self.cyclic_param = self.cyclic_entry.get()
                    self.motor_x_param = self.speed_motor_X_entry.get()
                    self.motor_x_param = str(int(255/100*int(self.motor_x_param)))
                    self.load_cell_x_param = self.pressure_X_entry.get()
                    self.MIN_X_param = self.MIN_X_entry.get()
                    self.MAX_X_param = self.MAX_X_entry.get()
                    
                    logger.debug(self.cyclic_param)
                    logger.debug(self.motor_x_param)
                    logger.debug(self.load_cell_x_param)
                    logger.debug(self.MIN_X_param)
                    logger.debug(self.MAX_X_param)

                    if self.ser_port_CT_Y.is_open:
                        self.motor_y_param = self.speed_motor_Y_entry.get()
                        # self.motor_y_param = str(int(255/100*int(self.motor_y_param)))
                        self.load_cell_y_param = self.pressure_Y_entry.get()
                        self.MIN_Y_param = self.MIN_Y_entry.get()
                        self.MAX_Y_param = self.MAX_Y_entry.get()
                        logger.debug(self.motor_y_param)
                        logger.debug(self.load_cell_y_param)
                        logger.debug(self.MIN_Y_param)
                        logger.debug(self.MAX_Y_param)
                        self.start_mc = 2
                self.after(10,self.run_mc)

            case 2:
                if self.cyclic_param:
                    cyclic_write = ("C")+(self.cyclic_param)+("\n")
                    cyclic_write = cyclic_write.encode() #========================== CYCLIC
                    print(cyclic_write)
                    self.ser_port_CT_X.write(cyclic_write)
                    self.start_mc = 3
                    self.after(10,self.run_mc)
                else:
                    messagebox.showwarning("WARNING", "คุณไท่ได้กรอก parameter ของ CYCLIC")
                    self.stop_button_pressed()

            case 3:
                if self.motor_x_param:
                    speed_X_write = ("S")+(self.motor_x_param)+("\n")
                    speed_X_write = speed_X_write.encode() #==================================== SPEED X
                    print(speed_X_write)
                    self.ser_port_CT_X.write(speed_X_write)
                    self.start_mc = 4
                    self.after(10,self.run_mc)
                else:
                    messagebox.showwarning("WARNING", "คุณไท่ได้กรอก parameter ของ MOTOR X")
                    self.stop_button_pressed()

            case 4:
                if self.load_cell_x_param:
                    loadcell_X_write = ("X")+(self.load_cell_x_param)+("\n")
                    loadcell_X_write = loadcell_X_write.encode() #================== LOADCELL X
                    print(loadcell_X_write)
                    self.ser_port_CT_X.write(loadcell_X_write)
                    self.start_mc = 5
                    self.after(10,self.run_mc)
                else:
                    messagebox.showwarning("WARNING", "คุณไท่ได้กรอก parameter ของ LOADCELL X")
                    self.stop_button_pressed()

            case 5:
                if self.MIN_X_param:
                    MIN_X_write = ("M")+(self.MIN_X_param)+("\n")
                    MIN_X_write = MIN_X_write.encode() #============ DISPLACMENT X
                    print(MIN_X_write)
                    self.ser_port_CT_X.write(MIN_X_write)
                    self.start_mc = 6
                    self.after(10,self.run_mc)
                else:
                    messagebox.showwarning("WARNING", "คุณไท่ได้กรอก parameter ของ MIN X")
                    self.stop_button_pressed()

            case 6:
                if self.MAX_X_param:
                    MAX_X_write = ("L")+(self.MAX_X_param)+("\n")
                    MAX_X_write = MAX_X_write.encode() #============ DISPLACMENT X
                    print(MAX_X_write)
                    self.ser_port_CT_X.write(MAX_X_write)
                    self.start_mc = 7
                    self.after(10,self.run_mc)
                else:
                    messagebox.showwarning("WARNING", "คุณไท่ได้กรอก parameter ของ MAX X")
                    self.stop_button_pressed()
                
            case 7:
                self.ser_port_CT_X.write(b'G\n')
                check_param_X = self.ser_port_CT_X.readline()
                check_param_X = check_param_X.strip().decode()
                check_param_X = check_param_X.split(",")
                speed_x = check_param_X[0]
                cyclic  = check_param_X[1]
                x_min  = check_param_X[2]
                x_max  = check_param_X[3]
                x_distans = check_param_X[4]
                if self.cyclic_param == cyclic:
                    if(self.motor_x_param == speed_x):
                        if(self.MIN_X_param == x_min):
                            if(self.MAX_X_param == x_max):
                                if(self.load_cell_x_param == x_distans):
                                    self.start_mc = 8   
                                    self.after(10,self.run_mc)
                                    
            case 8:
                self.ser_port_CT_X.write(b'R\n')
                print("OK")
                # self.after(100,self.run_mc)



            case _:
                pass
        # self.after(100,self.run_mc)

if __name__ == "__main__":
    app = App()
    app.eval('tk::PlaceWindow . center')
    app.mainloop()
