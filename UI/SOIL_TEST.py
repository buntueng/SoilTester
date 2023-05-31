import customtkinter as ctk
import tkinter as  tk
from tkinter import ttk
from tkinter import filedialog
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import serial as ser
import sys
import glob
from tkinter import messagebox
from get_data_displacement import linear_displacement
from datetime import datetime
import logging
import time
import matplotlib.pyplot as plt
import random

data_file = "./OK.txt"

ctk.set_appearance_mode("System") 
ctk.set_default_color_theme("blue") 
thai_large_font =("TH Niramit AS", 27,"bold")
thai_mid_font =("TH Niramit AS", 20,"bold")
eng_font = ("Time New Roman",25)
eng_small_font = ("Time New Roman",15)

vf_gap = 5
hf_gap = 5

#=================================== setup logging =========================================================
logging.getLogger('matplotlib.font_manager').disabled = True
logging.getLogger('PIL').setLevel(logging.WARNING)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logging_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

fileHandler = logging.FileHandler(filename="exp1_log.log")
fileHandler.setFormatter(logging_format)
logger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logging_format)
logger.addHandler(consoleHandler)


class App(ctk.CTk):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Soil Tester")
        # self.geometry(f"{1700}x{950}")
        self.resizable(False,False)
        

        self.master_frame = ctk.CTkFrame(self,fg_color="powderblue")
        self.master_frame.grid(row=0,column = 0)

        self.graph_frame = ctk.CTkFrame(self.master_frame,fg_color="blanchedalmond",corner_radius=20)
        self.graph_frame .grid(row=0,column=0,padx=5,pady=(5,0),columnspan = 1,sticky=tk.NW)
        
        self.configuration_frame = ctk.CTkFrame(self.master_frame,fg_color="powderblue",corner_radius=20)
        self.configuration_frame.grid(row=0,column=1,padx=(0,10),pady=(5,0),sticky=tk.NW,rowspan=3)

        self.monitor_frame = ctk.CTkFrame(self.master_frame,fg_color="cornflowerblue",corner_radius=20)
        self.monitor_frame.grid(row=1,column=0,padx=5,pady=5,sticky=tk.NW)
        #================================== CANVAS ==================================
        self.fig, self.graph_ax = plt.subplots(figsize=(20, 10), dpi=50)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        plt.yticks(fontsize=20)
        plt.xticks(fontsize=20)
    
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=1,column=0,padx = 10, pady = (0,10),)

        self.x_coordinate = []
        self.y_coordinate = []
        #================================== object ==================================
        graph_fg_colors = "powderblue"
        self.result_graph_label = ctk.CTkLabel(self.graph_frame,text="RESULT GRAPH",bg_color="blanchedalmond",text_color="red",font=thai_large_font)

        self.result_graph_label.grid(row=0, column=0,sticky=tk.N)
        #================================== monitor frame ===========================
        self.data_exp_1 = tk.StringVar()
        self.result_graph_label = ctk.CTkLabel(self.monitor_frame,text="ข้อมูลการทดสอบ",bg_color="cornflowerblue",text_color="azure1",font=thai_large_font)
        self.monitor_text_box = ctk.CTkTextbox(self.monitor_frame,width=1000,height=200,corner_radius=20,bg_color="cornflowerblue",text_color="red",font=thai_large_font)
        
        self.result_graph_label.grid(row=0, column=0,sticky=tk.N)
        self.monitor_text_box.grid(row=1,column=0,padx=5,pady=5,ipadx = 5,sticky=tk.NW)
        #================================== config ==================================
        self.select_port_label = ctk.CTkLabel(self.configuration_frame,text="เลือกพอต",bg_color=graph_fg_colors,text_color="red",font=thai_large_font)
        self.com_port_DIS_X_label = ctk.CTkLabel(self.configuration_frame,text="DIS X PORT",bg_color=graph_fg_colors,text_color="red",font=thai_large_font)
        self.com_port_DIS_X = ctk.CTkOptionMenu(self.configuration_frame,width=100,height=40,values=[""])
        self.com_port_DIS_X.set("เลือกพอต")
        self.com_port_DIS_Y_label = ctk.CTkLabel(self.configuration_frame,text="DIS Y PORT",bg_color=graph_fg_colors,text_color="red",font=thai_large_font)
        self.com_port_DIS_Y = ctk.CTkOptionMenu(self.configuration_frame,width=100,height=40,values=[""])
        self.com_port_DIS_Y.set("เลือกพอต")
        self.com_port_uC_label = ctk.CTkLabel(self.configuration_frame,text="uC PORT",bg_color=graph_fg_colors,text_color="red",font=thai_large_font)
        self.com_port_uC = ctk.CTkOptionMenu(self.configuration_frame,width=100,height=40,values=[""])
        self.com_port_uC.set("เลือกพอต")
        self.select_exp_label = ctk.CTkLabel(self.configuration_frame,text="เลือกการทดสอบ",bg_color=graph_fg_colors,text_color="red",font=thai_large_font)
        self.radiobutton_var = ctk.IntVar(value=0)
        self.radiobutton_EXP1 = ctk.CTkRadioButton(self.configuration_frame, variable=self.radiobutton_var, value=1,text="EXP 1",command=self.select_exp)
        self.radiobutton_EXP2 = ctk.CTkRadioButton(self.configuration_frame, variable=self.radiobutton_var, value=2,text="EXP 2",command=self.select_exp)
        self.radiobutton_EXP3 = ctk.CTkRadioButton(self.configuration_frame, variable=self.radiobutton_var, value=3,text="EXP 3",command=self.select_exp)
        self.radiobutton_EXP4 = ctk.CTkRadioButton(self.configuration_frame, variable=self.radiobutton_var, value=4,text="EXP 4",command=self.select_exp)
        self.exp_param_label = ctk.CTkLabel(self.configuration_frame,text="ตั้งค่าการทดสอบ",bg_color=graph_fg_colors,text_color="red",font=thai_large_font)
        self.pressure_Y_defualt = tk.StringVar(value="100")
        self.pressure_Y_label = ctk.CTkLabel(self.configuration_frame,text="แรงกดแกน Y",bg_color=graph_fg_colors,text_color="red",font=thai_large_font)
        self.pressure_Y_entry = ctk.CTkEntry(self.configuration_frame,width=100,height=40,font=eng_font,corner_radius=20,textvariable=self.pressure_Y_defualt)
        self.pressure_Y_unit_label = ctk.CTkLabel(self.configuration_frame,text="N",bg_color=graph_fg_colors,text_color="red",font=thai_large_font)
        self.pressure_X_defualt = tk.StringVar(value="10")
        self.pressure_min_X_label = ctk.CTkLabel(self.configuration_frame,text="แรงกด MIN X",bg_color=graph_fg_colors,text_color="red",font=thai_large_font)
        self.pressure_min_X_entry = ctk.CTkEntry(self.configuration_frame,width=100,height=40,font=eng_font,corner_radius=20,textvariable=self.pressure_X_defualt)
        self.pressure_min_X_unit_label = ctk.CTkLabel(self.configuration_frame,text="N",bg_color=graph_fg_colors,text_color="red",font=thai_large_font)
        self.pressure_max_X_defualt = tk.StringVar(value="100")
        self.pressure_max_X_label = ctk.CTkLabel(self.configuration_frame,text="แรงกด MAX X",bg_color=graph_fg_colors,text_color="red",font=thai_large_font)
        self.pressure_max_X_entry = ctk.CTkEntry(self.configuration_frame,width=100,height=40,font=eng_font,corner_radius=20,textvariable=self.pressure_max_X_defualt)
        self.pressure_max_X_unit_label = ctk.CTkLabel(self.configuration_frame,text="N",bg_color=graph_fg_colors,text_color="red",font=thai_large_font)
        self.pressure_step_X_defualt = tk.StringVar(value="2")
        self.pressure_step_X_label = ctk.CTkLabel(self.configuration_frame,text="Step แกน X",bg_color=graph_fg_colors,text_color="red",font=thai_large_font)
        self.pressure_step_X_entry = ctk.CTkEntry(self.configuration_frame,width=100,height=40,font=eng_font,corner_radius=20,textvariable=self.pressure_step_X_defualt)
        self.pressure_step_X_unit_label = ctk.CTkLabel(self.configuration_frame,text="N",bg_color=graph_fg_colors,text_color="red",font=thai_large_font)
        self.cyclic_X_defualt = tk.StringVar(value="10")
        self.cyclic_X_label = ctk.CTkLabel(self.configuration_frame,text="จำนวนครั้ง",bg_color=graph_fg_colors,text_color="red",font=thai_large_font)
        self.cyclic_X_entry = ctk.CTkEntry(self.configuration_frame,width=100,height=40,font=eng_font,corner_radius=20,textvariable=self.cyclic_X_defualt)
        self.cyclic_X_unit_label = ctk.CTkLabel(self.configuration_frame,text="ครั้ง",bg_color=graph_fg_colors,text_color="red",font=thai_large_font)
        self.pressure_X_exp2_defualt = tk.StringVar(value="10")
        self.pressure_min_X_exp2_label = ctk.CTkLabel(self.configuration_frame,text="แรงกดเริ่ม",bg_color=graph_fg_colors,text_color="red",font=thai_large_font)
        self.pressure_min_X_exp2_entry = ctk.CTkEntry(self.configuration_frame,width=100,height=40,font=eng_font,corner_radius=20,textvariable=self.pressure_X_exp2_defualt)
        self.pressure_min_X_exp2_unit_label = ctk.CTkLabel(self.configuration_frame,text="N",bg_color=graph_fg_colors,text_color="red",font=thai_large_font)
        self.pressure_max_X_exp2_defualt = tk.StringVar(value="100")
        self.pressure_max_X_exp2_label = ctk.CTkLabel(self.configuration_frame,text="แรงกดสิ้นสุด",bg_color=graph_fg_colors,text_color="red",font=thai_large_font)
        self.pressure_max_X_exp2_entry = ctk.CTkEntry(self.configuration_frame,width=100,height=40,font=eng_font,corner_radius=20,textvariable=self.pressure_max_X_exp2_defualt)
        self.pressure_max_X_exp2_unit_label = ctk.CTkLabel(self.configuration_frame,text="N",bg_color=graph_fg_colors,text_color="red",font=thai_large_font)  
        self.pressure_step_X_exp2_defualt = tk.StringVar(value="100")
        self.pwm_x_label = ctk.CTkLabel(self.configuration_frame,text="PWM X ",bg_color=graph_fg_colors,text_color="red",font=thai_large_font)
        self.pwm_x_entry = ctk.CTkEntry(self.configuration_frame,width=100,height=40,font=eng_font,corner_radius=20,textvariable=self.pressure_step_X_exp2_defualt)
        self.pwm_x_unit_label = ctk.CTkLabel(self.configuration_frame,text="/255",bg_color=graph_fg_colors,text_color="red",font=thai_large_font) 

        self.cyclic_time_defualt = tk.StringVar(value="1000")
        self.cyclic_time_label = ctk.CTkLabel(self.configuration_frame,text="เวลา cyclic",bg_color=graph_fg_colors,text_color="red",font=thai_large_font)
        self.cyclic_time_entry = ctk.CTkEntry(self.configuration_frame,width=100,height=40,font=eng_font,corner_radius=20,textvariable=self.cyclic_time_defualt)
        self.cyclic_time_unit_label = ctk.CTkLabel(self.configuration_frame,text="ms",bg_color=graph_fg_colors,text_color="red",font=thai_large_font) 


        self.set_K_defualt = tk.StringVar(value="50")
        self.set_K_label = ctk.CTkLabel(self.configuration_frame,text="SET K",bg_color=graph_fg_colors,text_color="red",font=thai_large_font)
        self.set_K_entry = ctk.CTkEntry(self.configuration_frame,width=100,height=40,font=eng_font,corner_radius=20,textvariable=self.set_K_defualt)
        self.set_K_unit_label = ctk.CTkLabel(self.configuration_frame,text="N",bg_color=graph_fg_colors,text_color="red",font=thai_large_font)
        self.start_button = ctk.CTkButton(self.configuration_frame,text = "เริ่มการทดสอบ",width=255,height=60,font=eng_font,corner_radius=15,command=self.start_button_pressed)
        self.stop_button = ctk.CTkButton(self.configuration_frame,text = "หยุดการทดสอบ",width=255,height=60,font=eng_font,corner_radius=15,command=self.stop_button_pressed)
        self.save_button = ctk.CTkButton(self.configuration_frame,text = "บันทึก",width=255,height=60,font=eng_font,corner_radius=15,command=self.save_botton_pressed)
        self.set_origin = ctk.CTkButton(self.configuration_frame,text = "ZERO",width=255,height=60,font=eng_font,corner_radius=15,command=self.zero_origin_pressed)
        self.clear_monitor_button = ctk.CTkButton(self.configuration_frame,text = "CLEAR MONITOR",width=255,height=60,font=eng_font,corner_radius=15,command= self.clear_monitor)
        # self.plot_graph = ctk.CTkButton(self.configuration_frame,text = "Plot",width=255,height=60,font=eng_font,corner_radius=15,command=self.plot_xy)

        self.select_port_label.grid(row=0, column=0, padx=(225,5), pady=(0, 0),sticky=tk.N,columnspan = 4)
        self.com_port_DIS_X_label.grid(row=1,column=0,padx=(5,5),pady=(5,0),sticky=tk.NW)
        self.com_port_DIS_X.grid(row=1, column=1, padx=(5,5), pady=(5, 0),sticky=tk.NW)
        self.com_port_DIS_Y_label.grid(row=1,column=2,padx=(5,5),pady=(5,0),sticky=tk.N)
        self.com_port_DIS_Y.grid(row=1, column=3, padx=(5,0), pady=(5, 0),sticky=tk.NW)
        self.com_port_uC_label.grid(row=1,column=4,padx=(5,5),pady=(5,0),sticky=tk.N)
        self.com_port_uC.grid(row=1, column=5, padx=(5,5), pady=(5, 0),sticky=tk.NW)
        self.select_exp_label.grid(row=2, column=0, padx=(225,5), pady=(10, 0),sticky=tk.N,columnspan = 4)
        self.radiobutton_EXP1.grid(row=3, column=0, padx=(55,5), pady=(15, 20),columnspan = 5,sticky=tk.NW)
        self.radiobutton_EXP2.grid(row=3, column=1, padx=(105,5), pady=(15, 20),columnspan = 5,sticky=tk.NW)
        self.radiobutton_EXP3.grid(row=3, column=2, padx=(160,5), pady=(15, 20),columnspan = 5,sticky=tk.NW)
        self.radiobutton_EXP4.grid(row=3, column=3, padx=(210,0), pady=(15, 20),columnspan = 5,sticky=tk.NW)
        self.exp_param_label.grid(row=4, column=0, padx=(225,5), pady=(0, 5),sticky=tk.N,columnspan = 4)
        self.pressure_Y_label.grid(row=5, column=0, padx=(5,10),columnspan = 3,sticky=tk.NW)
        self.pressure_Y_entry.grid(row=5, column=1,columnspan = 3,padx=(30,10),sticky=tk.NW)
        self.pressure_Y_unit_label.grid(row=5, column=2, padx=(35,10),columnspan = 3,sticky=tk.NW)
        self.pressure_min_X_label.grid(row=6, column=0, padx=(5,10), pady=(20, 0),columnspan = 3,sticky=tk.NW)
        self.pressure_min_X_entry.grid(row=6, column=1,columnspan = 3,padx=(30,10), pady=(20, 0),sticky=tk.NW)
        self.pressure_min_X_unit_label.grid(row=6, column=2, padx=(35,10), pady=(20, 0),columnspan = 3,sticky=tk.NW)
        self.pressure_max_X_label.grid(row=7, column=0, padx=(5,10), pady=(20, 0),columnspan = 3,sticky=tk.NW)
        self.pressure_max_X_entry.grid(row=7, column=1,columnspan = 3,padx=(30,10), pady=(20, 0),sticky=tk.NW)
        self.pressure_max_X_unit_label.grid(row=7, column=2, padx=(35,10), pady=(20, 0),columnspan = 3,sticky=tk.NW)
        self.pressure_step_X_label.grid(row=8, column=0, padx=(5,10), pady=(20, 0),columnspan = 3,sticky=tk.NW)
        self.pressure_step_X_entry.grid(row=8, column=1,columnspan = 3,padx=(30,10), pady=(20, 0),sticky=tk.NW)
        self.pressure_step_X_unit_label.grid(row=8, column=2, padx=(35,10), pady=(20, 0),sticky=tk.NW)
        self.set_K_label.grid(row=9, column=0, padx=(5,10), pady=(20, 0),sticky=tk.NW)
        self.set_K_entry.grid(row=9, column=1,columnspan = 3,padx=(30,10), pady=(20, 0),sticky=tk.NW)
        self.set_K_unit_label.grid(row=9, column=2, padx=(35,10), pady=(20, 50),sticky=tk.NW)

        self.cyclic_X_label.grid(row=5, column=3, padx=(5,10),columnspan = 3,sticky=tk.NW)
        self.cyclic_X_entry.grid(row=5, column=4,padx=(5,10),columnspan = 3,sticky=tk.NW)
        self.cyclic_X_unit_label.grid(row=5, column=5, padx=(35,0),columnspan = 3,sticky=tk.NW)
        self.pressure_min_X_exp2_label.grid(row=6, column=3, padx=(5,10), pady=(20, 0),sticky=tk.NW)
        self.pressure_min_X_exp2_entry.grid(row=6, column=4,columnspan = 3,padx=(5,10), pady=(20, 0),sticky=tk.NW)
        self.pressure_min_X_exp2_unit_label.grid(row=6, column=5, padx=(45,0), pady=(20, 0),sticky=tk.NW)
        self.pressure_max_X_exp2_label.grid(row=7, column=3, padx=(5,10), pady=(20, 0),sticky=tk.NW)
        self.pressure_max_X_exp2_entry.grid(row=7, column=4,columnspan = 3,padx=(5,10), pady=(20, 0),sticky=tk.NW)
        self.pressure_max_X_exp2_unit_label.grid(row=7, column=5, padx=(45,0), pady=(20, 0),sticky=tk.NW)
        self.pwm_x_label.grid(row=8, column=3, padx=(5,10), pady=(20, 0),sticky=tk.NW)
        self.pwm_x_entry.grid(row=8, column=4,columnspan = 3,padx=(5,10), pady=(20, 0),sticky=tk.NW)
        self.pwm_x_unit_label.grid(row=8, column=5, padx=(45,0), pady=(20, 0),sticky=tk.NW)

        self.cyclic_time_label.grid(row=9, column=3, padx=(5,10), pady=(20, 0),sticky=tk.NW)
        self.cyclic_time_entry.grid(row=9, column=4,columnspan = 3,padx=(5,10), pady=(20, 0),sticky=tk.NW)
        self.cyclic_time_unit_label.grid(row=9, column=5, padx=(45,0), pady=(20, 0),sticky=tk.NW)

        self.start_button.grid(row=10, column=0, padx=(60,0),columnspan = 7,sticky=tk.NW)
        self.stop_button.grid(row=10,column=1, padx=(240,0),pady = (0,20),columnspan = 7,sticky=tk.NW)
        self.save_button.grid(row=11,column=0, padx=(60,0),columnspan = 7,sticky=tk.NW)
        self.set_origin.grid(row=11,column=1, padx=(240,0),columnspan = 7,sticky=tk.NW)
        self.clear_monitor_button.grid(row=12,column=0, padx=(60,0),columnspan = 7,pady=(20,0),sticky=tk.NW)

        # self.plot_graph.grid(row=12,column=0, padx=(20,15),columnspan = 3,pady=(10,0),sticky=tk.NW)
        #============================================================================

        self.ser_port_uC = ser.Serial(baudrate=115200,parity=ser.PARITY_NONE,stopbits=ser.STOPBITS_ONE,bytesize=ser.EIGHTBITS,timeout=0.5,inter_byte_timeout=0.1)  
        self.ser_port_DIS_X = ser.Serial(baudrate=9600,parity=ser.PARITY_NONE,stopbits=ser.STOPBITS_ONE,bytesize=ser.EIGHTBITS,timeout=0.5,inter_byte_timeout=0.1)  
        self.ser_port_DIS_Y= ser.Serial(baudrate=9600,parity=ser.PARITY_NONE,stopbits=ser.STOPBITS_ONE,bytesize=ser.EIGHTBITS,timeout=0.5,inter_byte_timeout=0.1) 
       
        self.zero_state = 0
        self.set_zero_status = False

        self.radiobutton_var.set(1)

        self.run_exp1_state = 0
        self.run_exp2_state = 0
        self.run_exp3_state = 0
        self.run_exp4_state = 0

        self.start_exp1 = False       
        active_port_list = self.list_serial_ports()
        self.com_port_DIS_X.configure(values=active_port_list)
        self.com_port_DIS_Y.configure(values=active_port_list)
        self.com_port_uC.configure(values=active_port_list)
        self.horizontal_test_force = []
        self.record_timer = time.time()
        self.disable_widget()
        self.select_exp()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.running_flag = False

    def select_exp(self):
        selected_exp = self.radiobutton_var.get()
        if selected_exp == 1:
            self.exp_param_label.configure(state = "normal")
            self.pressure_Y_label.configure(state = "normal")
            self.pressure_Y_entry.configure(state = "normal")
            self.pressure_Y_unit_label.configure(state = "normal")
            self.pressure_min_X_label.configure(state = "disabled")
            self.pressure_min_X_entry.configure(state = "disabled")
            self.pressure_min_X_unit_label.configure(state = "disabled")
            self.pressure_max_X_label.configure(state = "disabled")
            self.pressure_max_X_entry.configure(state = "disabled")
            self.pressure_max_X_unit_label.configure(state = "disabled")
            self.pressure_step_X_label.configure(state = "disabled")
            self.pressure_step_X_entry.configure(state = "disabled")
            self.pressure_step_X_unit_label.configure(state = "disabled")
            self.set_K_label.configure(state = "disabled")
            self.set_K_entry.configure(state = "disabled")
            self.set_K_unit_label.configure(state = "disabled")
            self.cyclic_X_label.configure(state = "disabled")
            self.cyclic_X_entry.configure(state = "disabled")
            self.cyclic_X_unit_label.configure(state = "disabled")
            self.pressure_min_X_exp2_label.configure(state = "disabled")
            self.pressure_min_X_exp2_entry.configure(state = "disabled")
            self.pressure_min_X_exp2_unit_label.configure(state = "disabled")
            self.pressure_max_X_exp2_label.configure(state = "disabled")
            self.pressure_max_X_exp2_entry.configure(state = "disabled")
            self.pressure_max_X_exp2_unit_label.configure(state = "disabled")
            self.pwm_x_label.configure(state = "normal")
            self.pwm_x_entry.configure(state = "normal")
            self.pwm_x_unit_label.configure(state = "normal") 
            self.cyclic_time_label.configure(state = "disabled")
            self.cyclic_time_entry.configure(state = "disabled")
            self.cyclic_time_unit_label.configure(state = "disabled")
        elif selected_exp == 2:
            self.exp_param_label.configure(state = "normal")
            self.pressure_Y_label.configure(state = "normal")
            self.pressure_Y_entry.configure(state = "normal")
            self.pressure_Y_unit_label.configure(state = "normal")
            self.pressure_min_X_label.configure(state = "disabled")
            self.pressure_min_X_entry.configure(state = "disabled")
            self.pressure_min_X_unit_label.configure(state = "disabled")
            self.pressure_max_X_label.configure(state = "disabled")
            self.pressure_max_X_entry.configure(state = "disabled")
            self.pressure_max_X_unit_label.configure(state = "disabled")
            self.pressure_step_X_label.configure(state = "disabled")
            self.pressure_step_X_entry.configure(state = "disabled")
            self.pressure_step_X_unit_label.configure(state = "disabled")
            self.set_K_label.configure(state = "disabled")
            self.set_K_entry.configure(state = "disabled")
            self.set_K_unit_label.configure(state = "disabled")
            self.cyclic_X_label.configure(state = "normal")
            self.cyclic_X_entry.configure(state = "normal")
            self.cyclic_X_unit_label.configure(state = "normal")
            self.pressure_min_X_exp2_label.configure(state = "normal")
            self.pressure_min_X_exp2_entry.configure(state = "normal")
            self.pressure_min_X_exp2_unit_label.configure(state = "normal")
            self.pressure_max_X_exp2_label.configure(state = "normal")
            self.pressure_max_X_exp2_entry.configure(state = "normal")
            self.pressure_max_X_exp2_unit_label.configure(state = "normal")
            self.pwm_x_label.configure(state = "normal")
            self.pwm_x_entry.configure(state = "normal")
            self.pwm_x_unit_label.configure(state = "normal") 
            self.cyclic_time_label.configure(state = "normal")
            self.cyclic_time_entry.configure(state = "normal")
            self.cyclic_time_unit_label.configure(state = "normal")
        elif selected_exp == 3:
            self.exp_param_label.configure(state = "normal")
            self.pressure_Y_label.configure(state = "normal")
            self.pressure_Y_entry.configure(state = "normal")
            self.pressure_Y_unit_label.configure(state = "normal")
            self.pressure_min_X_label.configure(state = "normal")
            self.pressure_min_X_entry.configure(state = "normal")
            self.pressure_min_X_unit_label.configure(state = "normal")
            self.pressure_max_X_label.configure(state = "normal")
            self.pressure_max_X_entry.configure(state = "normal")
            self.pressure_max_X_unit_label.configure(state = "normal")
            self.pressure_step_X_label.configure(state = "normal")
            self.pressure_step_X_entry.configure(state = "normal")
            self.pressure_step_X_unit_label.configure(state = "normal")
            self.set_K_label.configure(state = "normal")
            self.set_K_entry.configure(state = "normal")
            self.set_K_unit_label.configure(state = "normal")
            self.cyclic_X_label.configure(state = "disabled")
            self.cyclic_X_entry.configure(state = "disabled")
            self.cyclic_X_unit_label.configure(state = "disabled")
            self.pressure_min_X_exp2_label.configure(state = "disabled")
            self.pressure_min_X_exp2_entry.configure(state = "disabled")
            self.pressure_min_X_exp2_unit_label.configure(state = "disabled")
            self.pressure_max_X_exp2_label.configure(state = "disabled")
            self.pressure_max_X_exp2_entry.configure(state = "disabled")
            self.pressure_max_X_exp2_unit_label.configure(state = "disabled")
            self.pwm_x_label.configure(state = "disabled")
            self.pwm_x_entry.configure(state = "disabled")
            self.pwm_x_unit_label.configure(state = "disabled")
            self.cyclic_time_label.configure(state = "disabled")
            self.cyclic_time_entry.configure(state = "disabled")
            self.cyclic_time_unit_label.configure(state = "disabled")
        elif selected_exp == 4:
            self.exp_param_label.configure(state = "normal")
            self.pressure_Y_label.configure(state = "normal")
            self.pressure_Y_entry.configure(state = "normal")
            self.pressure_Y_unit_label.configure(state = "normal")
            self.pressure_min_X_label.configure(state = "disabled")
            self.pressure_min_X_entry.configure(state = "disabled")
            self.pressure_min_X_unit_label.configure(state = "disabled")
            self.pressure_max_X_label.configure(state = "disabled")
            self.pressure_max_X_entry.configure(state = "disabled")
            self.pressure_max_X_unit_label.configure(state = "disabled")
            self.pressure_step_X_label.configure(state = "disabled")
            self.pressure_step_X_entry.configure(state = "disabled")
            self.pressure_step_X_unit_label.configure(state = "disabled")
            self.set_K_label.configure(state = "normal")
            self.set_K_entry.configure(state = "normal")
            self.set_K_unit_label.configure(state = "normal")
            self.cyclic_X_label.configure(state = "normal")
            self.cyclic_X_entry.configure(state = "normal")
            self.cyclic_X_unit_label.configure(state = "normal")
            self.pressure_min_X_exp2_label.configure(state = "normal")
            self.pressure_min_X_exp2_entry.configure(state = "normal")
            self.pressure_min_X_exp2_unit_label.configure(state = "normal")
            self.pressure_max_X_exp2_label.configure(state = "normal")
            self.pressure_max_X_exp2_entry.configure(state = "normal")
            self.pressure_max_X_exp2_unit_label.configure(state = "normal")
            self.pwm_x_label.configure(state = "normal")
            self.pwm_x_entry.configure(state = "normal")
            self.pwm_x_unit_label.configure(state = "normal") 
            self.cyclic_time_label.configure(state = "normal")
            self.cyclic_time_entry.configure(state = "normal")
            self.cyclic_time_unit_label.configure(state = "normal")
        else: 
            self.exp_param_label.configure(state = "disabled")
            self.pressure_Y_label.configure(state = "disabled")
            self.pressure_Y_entry.configure(state = "disabled")
            self.pressure_Y_unit_label.configure(state = "disabled")
            self.pressure_min_X_label.configure(state = "disabled")
            self.pressure_min_X_entry.configure(state = "disabled")
            self.pressure_min_X_unit_label.configure(state = "disabled")
            self.pressure_max_X_label.configure(state = "disabled")
            self.pressure_max_X_entry.configure(state = "disabled")
            self.pressure_max_X_unit_label.configure(state = "disabled")
            self.pressure_step_X_label.configure(state = "disabled")
            self.pressure_step_X_entry.configure(state = "disabled")
            self.pressure_step_X_unit_label.configure(state = "disabled")
            self.set_K_label.configure(state = "disabled")
            self.set_K_unit_label.configure(state = "disabled")
            self.cyclic_X_label.configure(state = "disabled")
            self.cyclic_X_entry.configure(state = "disabled")
            self.cyclic_X_unit_label.configure(state = "disabled")
            self.pressure_min_X_exp2_label.configure(state = "disabled")
            self.pressure_min_X_exp2_entry.configure(state = "disabled")
            self.pressure_min_X_exp2_unit_label.configure(state = "disabled")
            self.pressure_max_X_exp2_label.configure(state = "disabled")
            self.pressure_max_X_exp2_entry.configure(state = "disabled")
            self.pressure_max_X_exp2_unit_label.configure(state = "disabled")
            self.pwm_x_label.configure(state = "disabled")
            self.pwm_x_entry.configure(state = "disabled")
            self.pwm_x_unit_label.configure(state = "disabled") 

    def plot_xy(self):
        time_axis = time.time()*1000
        self.x_coordinate.append(time_axis)
        self.y_coordinate.append(random.randint(0,100))
        self.graph_ax.plot(self.x_coordinate,self.y_coordinate)
        self.canvas.draw()
        
        # logger.debug("plot graph")

    def on_closing(self):
        try:
            self.ser_port_DIS_X.close()
            self.ser_port_DIS_Y.close()
            self.ser_port_uC.close()
        except:
            pass
        self.quit()
        self.after(10,self.destoy_windows)
    
    def destoy_windows(self):
        self.destroy()

    def list_serial_ports(self):
            if sys.platform.startswith('win'):
                ports = ['COM%s' % (i + 1) for i in range(2,40)]
            elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
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

    def disable_widget(self):
        self.start_button.configure(state = "normal")
        self.stop_button.configure(state="disabled")
        self.save_button.configure(state="disabled")

    def enable_widget(self):
        self.start_button.configure(state = "normal")

    def check_select_comport(self):
        check_flag = False
        disX = self.com_port_DIS_X.get()
        disY = self.com_port_DIS_Y.get()
        uC_port = self.com_port_uC.get()     
        self.selected_port_list = [uC_port,disX,disY]
        locked_port = self.selected_port_list

        if len(set(self.selected_port_list))<3:           
            self.com_port_uC.configure(state="normal")
            self.com_port_DIS_X.configure(state="normal")
            self.com_port_DIS_Y.configure(state="normal")
            messagebox.showwarning("WARNING", "คุณเลือกคอมพอตไม่ครบ")
        else:
            try:
                self.ser_port_uC.port = uC_port
                self.ser_port_uC.open()
                self.ser_port_uC.close()
                locked_port.remove(uC_port)

                self.ser_port_DIS_X.port = disX
                self.ser_port_DIS_X.open()
                self.ser_port_DIS_X.close()
                locked_port.remove(disX)

                self.ser_port_DIS_Y.port = disY
                self.ser_port_DIS_Y.open()
                self.ser_port_DIS_Y.close()
                locked_port.remove(disY)

                check_flag = True
            except:
                error_message = "busy port:\n"
                for port_name in locked_port:
                    error_message = error_message + port_name + "\n"
                tk.messagebox.showerror(title="พอร์ตที่ใช้งานไม่ได้", message=error_message,)
        return check_flag

    def check_xy_params(self):
        check_flag = False
        param_x = self.pressure_min_X_entry.get()
        param_y = self.pressure_Y_entry.get()
        try:
            int(param_x)
            int(param_y)
            check_flag = True
            # logger.debug("xy params is integer")
        except:
            check_flag = False
            tk.messagebox.showerror(title="xy params error", message="ตรวจสอบ parameter x และ y",)
        return check_flag
    
    def clear_can(self):
        for item in self.canvas.get_tk_widget().find_all():
            self.canvas.get_tk_widget().delete(item)

    def start_button_pressed(self):
        self.monitor_text_box.delete("1.0",tk.END)
        self.x_coordinate=[]
        self.y_coordinate=[]
        self.graph_ax.plot(self.x_coordinate,self.y_coordinate)
        self.canvas.draw()
        if self.check_select_comport() and self.check_xy_params():
            self.com_port_uC.configure(state="disabled")
            self.com_port_DIS_X.configure(state="disabled")
            self.com_port_DIS_Y.configure(state="disabled")
            self.start_button.configure(state="disabled")
            self.stop_button.configure(state="normal")
            self.save_button.configure(state="normal")
            self.start_button.configure(state="disabled")
            self.stop_button.configure(state="normal")
            self.save_button.configure(state="normal")
            self.pressure_min_X_entry.configure(state="disabled")
            self.pressure_Y_entry.configure(state="disabled")
            start_T = int(self.pressure_min_X_entry.get())
            stop_T = int(self.pressure_max_X_entry.get())
            step_T  = int(self.pressure_step_X_entry.get())

            self.running_flag = True
            # clear display and graph

            # check experiments here

            match self.radiobutton_var.get():
                case 1:
                    self.run_exp1_state = 0
                    self.after(10,self.run_exp1)
                case 2:
                    self.run_exp2_state = 0
                    self.after(10,self.run_exp2)
                case 3:
                    self.run_exp3_state = 0
                    self.after(10,self.run_exp3)
                case 4:
                    self.run_exp4_state = 0
                    self.after(10,self.run_exp4)
                case other:
                    logger.warning("Experiment number is out of list")
           
    def run_exp1(self):
        if self.running_flag:
            match self.run_exp1_state:
                case 0:
                    self.ser_port_uC.open()
                    self.obj_dis_x = linear_displacement(portname=self.com_port_DIS_X.get())
                    self.obj_dis_y = linear_displacement(portname=self.com_port_DIS_Y.get())
                    # print(("port x ")+(self.com_port_DIS_X.get())+("  port y ")+(self.com_port_DIS_Y.get()))
                    self.obj_dis_x.run()
                    self.obj_dis_y.run()
                    self.run_exp1_state = 1
                    self.after(2000,self.run_exp1)

                case 1:
                    set_zero = "Z" + "\n"
                    set_zero_byte = set_zero.encode()
                    self.ser_port_uC.write(set_zero_byte)
                    self.run_exp1_state = 2
                    self.after(500,self.run_exp1)

                case 2:
                    setting_result = self.ser_port_uC.readline()
                    setting_result_string = setting_result.rstrip().decode()
                    if setting_result_string =="ZERO COMPLETE":
                        self.run_exp1_state = 3
                    else:
                        pass
                    self.after(500,self.run_exp1)

                case 3:
                    vertical_force = self.pressure_Y_entry.get()
                    if self.ser_port_uC.is_open:
                        vertical_test_force = "N" + vertical_force + "\n" #============================== Y force
                        vertical_test_force_bytes = vertical_test_force.encode()
                        self.ser_port_uC.write(vertical_test_force_bytes)
                        self.run_exp1_state = 4
                        self.after(100,self.run_exp1)

                case 4:
                    setting_result = self.ser_port_uC.readline()
                    setting_result_string = setting_result.strip().decode()
                    if setting_result_string == self.pressure_Y_entry.get():
                        self.run_exp1_state = 5
                    else:
                        self.run_exp1_state = 3
                    self.after(100,self.run_exp1)

                case 5:
                    pwm = self.pwm_x_entry.get()
                    if self.ser_port_uC.is_open:
                        exp1_update_pwm_string = "U" + pwm + "\n" #=============================== update pwm x
                        exp1_update_pwm_byte = exp1_update_pwm_string.encode()
                        self.ser_port_uC.write(exp1_update_pwm_byte)
                        self.run_exp1_state = 6
                        self.after(100,self.run_exp1)
                
                case 6:
                    setting_result = self.ser_port_uC.readline()
                    setting_result_string = setting_result.rstrip().decode()
                    if setting_result_string == self.pwm_x_entry.get():
                        self.run_exp1_state = 7
                    else:
                        self.run_exp1_state = 5
                    self.after(100,self.run_exp1)

                case 7:
                    start_exp1 = "r1\n"
                    start_exp1 = start_exp1.encode()
                    self.ser_port_uC.write(start_exp1)
                    self.run_exp1_state = 8
                    self.after(100,self.run_exp1)
                    self.start_time = time.time()

                case 8:
                    param_result = self.ser_port_uC.readline()
                    param_result_string = param_result.rstrip().decode()
                    status_exp1_test,horizontal_force,vertical_force = param_result_string.split(",")
                    time_stamp = datetime.now().strftime("%H:%M:%S.%f")
                    param_for_exp1 = (time_stamp)+(",")+(status_exp1_test)+(",")+(horizontal_force)+(",")+(vertical_force)+"\n" 
                    self.monitor_text_box.insert(tk.END,param_for_exp1)
                    time_in_x = (time.time()-self.start_time)
                    time_in_x = float('%.3f'%time_in_x)#time in X
                    dispY = (self.obj_dis_y.get_last())
                    if dispY != None:
                        y_show3digit = f'{int(dispY[:-2])*0.001:.3f}'
                        # print(y_show3digit)
                        self.x_coordinate.append(float(time_in_x))
                        self.y_coordinate.append(float(y_show3digit))
                        self.graph_ax.plot(self.x_coordinate,self.y_coordinate)
                        self.canvas.draw()
                    if status_exp1_test == "1":
                        self.run_exp1_state = 9
                    self.after(40,self.run_exp1)

                case 9:
                    stop_exp1 = "t\n"
                    stop_exp1 = stop_exp1.encode()
                    self.ser_port_uC.write(stop_exp1)
                    self.after(100,self.run_exp1)
                    self.run_exp1_state = 10
                
                case 10:
                    self.exp_test_success()
                    logger.debug("EXP1 SUCCESS")

                case other:
                    self.running_flag = False
            
    def run_exp2(self):
        if self.running_flag:
            match self.run_exp2_state:
                case 0:
                    pass
                case 1:
                    pass
                case 2:
                    pass
                case 3:
                    pass
                case 4:
                    pass
                case 5:
                    pass
                case 6:
                    pass
                case _:
                    self.running_flag = False
    
    def run_exp3(self):
        if self.running_flag:
            match self.run_exp3_state:
                case 0:
                    pass
                case 1:
                    pass
                case 2:
                    pass
                case 3:
                    pass
                case 4:
                    pass
                case 5:
                    pass
                case 6:
                    pass
                case other:
                    self.running_flag = False
            
            self.after(self.run_exp3())

    def run_exp4(self):
        if self.running_flag:
            match self.run_exp4_state:
                case 0:
                    pass
                case 1:
                    pass
                case 2:
                    pass
                case 3:
                    pass
                case 4:
                    pass
                case 5:
                    pass
                case 6:
                    pass
                case other:
                    self.running_flag = False
            
            self.after(self.run_exp4())

    def stop_button_pressed(self):
        self.running_flag = False

        self.disable_widget()
        self.ser_port_DIS_X.close()
        self.ser_port_DIS_Y.close()
        self.ser_port_uC.close()
        self.com_port_uC.configure(state="normal")
        self.com_port_DIS_X.configure(state="normal")
        self.com_port_DIS_Y.configure(state="normal")
        self.start_button.configure(state = "normal")
        self.stop_button.configure(state="disabled")
        self.save_button.configure(state="disabled")
        self.pressure_min_X_entry.configure(state = "normal")
        self.pressure_Y_entry.configure(state = "normal")
        self.start_exp1 = False
        self.run_exp1_state = 0
        self.obj_dis_x.stop()
        self.obj_dis_y.stop()

    def exp_test_success(self):
        self.stop_button.configure(state="disabled")
        self.save_button.configure(state="normal")
        self.ser_port_DIS_X.close()
        self.ser_port_DIS_Y.close()
        self.ser_port_uC.close()
        self.running_flag = False
        self.start_exp1 = False
        self.run_exp1_state = 0
        self.obj_dis_x.stop()
        self.obj_dis_y.stop()
        messagebox.showinfo("INFO", "TEST SUCCESS")

    def save_botton_pressed(self):
        self.savefileas()

    def savefileas(self):
        path = None
        try:
            file_path = filedialog.asksaveasfile(filetypes = (("Text files", "*.txt"), ("All files", "*.*")))
            param = self.monitor_text_box.get('1.0', tk.END)
            file_path.write(param)
            file_path.close()
            self.stop_button_pressed()
        
        except:
            # print("Error")
            pass

    def clear_monitor(self):
        self.monitor_text_box.delete('1.0',tk.END)
    
    def zero_origin_pressed(self):
        comport_uc_selected = self.com_port_uC.get()
        if comport_uc_selected == "เลือกพอต":
            messagebox.showwarning("WARNING", "คุณไม่ได้เลือกคอมพอต")
        else:
            self.start_button.configure(state = "disabled")
            self.set_origin.configure(state = "disabled")
            self.ser_port_uC = ser.Serial(baudrate=115200,parity=ser.PARITY_NONE,stopbits=ser.STOPBITS_ONE,bytesize=ser.EIGHTBITS,timeout=0.5,inter_byte_timeout=0.1)  
            uc_port =self.com_port_uC.get()
            self.ser_port_uC.port = uc_port
            self.ser_port_uC.open()
            self.after(2000,self.set_zero)
            self.set_zero_status = True
            self.zero_state = 0

    def set_zero(self):
        match(self.zero_state):
            case 0:
                if self.set_zero_status == True:
                    self.zero_state = 1
                    self.after(100,self.set_zero)
            case 1:
                if self.ser_port_uC.is_open:
                    self.zero_state = 2
                    self.after(100,self.set_zero)
                else:
                    self.zero_state = 0
                    self.after(100,self.set_zero)
            case 2:
                if self.ser_port_uC.is_open:
                    cmd_set_zero = 'Z\n'
                    cmd_set_zero_bytes = cmd_set_zero.encode()
                    self.ser_port_uC.write(cmd_set_zero_bytes)
                    self.zero_state = 3
                    self.after(100,self.set_zero)
                else:
                    pass
            case 3:
                status_set_zero = self.ser_port_uC.readline()
                status_set_zero_string = status_set_zero.rstrip().decode()
                if((status_set_zero_string)=="ZERO COMPLETE"):
                    self.zero_state = 4
                else:
                    pass
                self.after(500,self.set_zero)
            case 4:
                self.monitor_text_box.insert(tk.END,"ORIGIN OK\n")
                self.start_button.configure(state = "normal")
                self.set_origin.configure(state = "normal")
                self.set_zero_status = False
                self.ser_port_uC.close()
            case _:
                pass



if __name__ == "__main__":
    app = App()
    app.eval('tk::PlaceWindow . center')
    app.mainloop()