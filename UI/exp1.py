import customtkinter as ctk
import tkinter as  tk
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,)
import serial as ser
import sys
import glob
from tkinter import messagebox
from get_data_displacement import linear_displacement
from datetime import datetime
import logging
import time


ctk.set_appearance_mode("System") 
ctk.set_default_color_theme("blue") 
thai_large_font =("TH Niramit AS", 27,"bold")
thai_mid_font =("TH Niramit AS", 20,"bold")
eng_font = ("Time New Roman",25)
eng_small_font = ("Time New Roman",15)

vf_gap = 5
hf_gap = 5

#=================================== setup logging =========================================================
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logging_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

fileHandler = logging.FileHandler(filename="./exp1_log.log")
fileHandler.setFormatter(logging_format)
logger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logging_format)
logger.addHandler(consoleHandler)


class App(ctk.CTk):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("MONOTONIC TESTER")
        self.resizable(False,False)

        self.master_frame = ctk.CTkFrame(self,fg_color="powderblue")
        self.master_frame.grid(row=0,column = 0)

        self.graph_frame = ctk.CTkFrame(self.master_frame,fg_color="blanchedalmond",corner_radius=20)
        self.graph_frame .grid(row=0,column=0,padx=5,pady=(5,0),columnspan = 1,sticky=tk.NW)
        
        self.configuration_frame = ctk.CTkFrame(self.master_frame,fg_color="powderblue",corner_radius=20)
        self.configuration_frame.grid(row=0,column=1,padx=(0,10),pady=(5,0),ipady=15,sticky=tk.NW)

        self.monitor_frame = ctk.CTkFrame(self.master_frame,fg_color="cornflowerblue",corner_radius=20)
        self.monitor_frame.grid(row=1,column=0,padx=5,pady=5,sticky=tk.NW,columnspan = 2)
        #================================== CANVAS ==================================
        figure = Figure(figsize=(20, 10), dpi=50)
        canvas = FigureCanvasTkAgg(figure, master=self.graph_frame)
        canvas.get_tk_widget().grid(row=1,column=0,padx = 10, pady = (0,10))
        #================================== object ==================================
        graph_fg_colors = "powderblue"
        self.result_graph_label = ctk.CTkLabel(self.graph_frame,text="RESULT GRAPH",bg_color="blanchedalmond",text_color="red",font=thai_large_font)

        self.result_graph_label.grid(row=0, column=0,sticky=tk.N)
        #================================== monitor frame ===========================
        self.data_exp_1 = tk.StringVar()
        self.result_graph_label = ctk.CTkLabel(self.monitor_frame,text="ข้อมูลการทดสอบ",bg_color="cornflowerblue",text_color="azure1",font=thai_large_font)
        self.monitor_text_box = ctk.CTkTextbox(self.monitor_frame,width=1300,height=200,corner_radius=20,bg_color="cornflowerblue",text_color="red",font=thai_large_font)
        
        self.result_graph_label.grid(row=0, column=0,sticky=tk.N)
        self.monitor_text_box.grid(row=1,column=0,padx=5,pady=5,ipadx = 5,sticky=tk.NW)
        #================================== config ==================================
        self.com_port_DIS_X_label = ctk.CTkLabel(self.configuration_frame,text="DIS X PORT",bg_color=graph_fg_colors,text_color="red",font=thai_large_font)
        self.com_port_DIS_X = ctk.CTkOptionMenu(self.configuration_frame,width=100,height=40,values=[""])
        self.com_port_DIS_X.set("เลือกพอต")
        self.com_port_DIS_Y_label = ctk.CTkLabel(self.configuration_frame,text="DIS Y PORT",bg_color=graph_fg_colors,text_color="red",font=thai_large_font)
        self.com_port_DIS_Y = ctk.CTkOptionMenu(self.configuration_frame,width=100,height=40,values=[""])
        self.com_port_DIS_Y.set("เลือกพอต")
        self.com_port_uC_label = ctk.CTkLabel(self.configuration_frame,text="uC PORT",bg_color=graph_fg_colors,text_color="red",font=thai_large_font)
        self.com_port_uC = ctk.CTkOptionMenu(self.configuration_frame,width=100,height=40,values=[""])
        self.com_port_uC.set("เลือกพอต")
        self.pressure_X_defualt = tk.StringVar(value="10")
        self.pressure_X_label = ctk.CTkLabel(self.configuration_frame,text="แรงกดแกน X",bg_color=graph_fg_colors,text_color="red",font=thai_large_font)
        self.pressure_X_entry = ctk.CTkEntry(self.configuration_frame,width=100,height=40,font=eng_font,corner_radius=20,textvariable=self.pressure_X_defualt)
        self.pressure_X_unit_label = ctk.CTkLabel(self.configuration_frame,text="N",bg_color=graph_fg_colors,text_color="red",font=thai_large_font)
        self.pressure_Y_defualt = tk.StringVar(value="20")
        self.pressure_Y_label = ctk.CTkLabel(self.configuration_frame,text="แรงกดแกน Y",bg_color=graph_fg_colors,text_color="red",font=thai_large_font)
        self.pressure_Y_entry = ctk.CTkEntry(self.configuration_frame,width=100,height=40,font=eng_font,corner_radius=20,textvariable=self.pressure_Y_defualt)
        self.pressure_Y_unit_label = ctk.CTkLabel(self.configuration_frame,text="N",bg_color=graph_fg_colors,text_color="red",font=thai_large_font)
        self.start_button = ctk.CTkButton(self.configuration_frame,text = "เริ่มการทดสอบ",width=255,height=60,font=eng_font,corner_radius=15,command=self.start_button_pressed)
        self.stop_button = ctk.CTkButton(self.configuration_frame,text = "หยุดการทดสอบ",width=255,height=60,font=eng_font,corner_radius=15,command=self.stop_button_pressed)
        self.save_button = ctk.CTkButton(self.configuration_frame,text = "บันทึก",width=255,height=60,font=eng_font,corner_radius=15,command=self.save_botton_pressed)


        self.com_port_DIS_X_label.grid(row=0,column=0,padx=(5,5),pady=(10,0),ipadx = 5,sticky=tk.NW)
        self.com_port_DIS_X.grid(row=0, column=1, padx=(5,10), pady=(10, 0),sticky=tk.N)
        self.com_port_DIS_Y_label.grid(row=1,column=0,padx=(5,5),pady=(10,0),ipadx = 5,sticky=tk.NW)
        self.com_port_DIS_Y.grid(row=1, column=1, padx=(5,10), pady=(10, 0),sticky=tk.N)
        self.com_port_uC_label.grid(row=2,column=0,padx=(5,5),pady=(10,0),ipadx = 5,sticky=tk.NW)
        self.com_port_uC.grid(row=2, column=1, padx=(5,10), pady=(10, 0),sticky=tk.N)
        self.pressure_X_label.grid(row=4, column=0, padx=(5,10), pady=(10, 0),sticky=tk.NW)
        self.pressure_X_entry.grid(row=4, column=1,columnspan = 3,padx=(5,10), pady=(10, 0),sticky=tk.NW)
        self.pressure_X_unit_label.grid(row=4, column=2, padx=(5,10), pady=(10, 0),sticky=tk.NW)
        self.pressure_Y_label.grid(row=5, column=0, padx=(5,10), pady=(10, 0),sticky=tk.NW)
        self.pressure_Y_entry.grid(row=5, column=1,columnspan = 3,padx=(5,10), pady=(10, 0),sticky=tk.NW)
        self.pressure_Y_unit_label.grid(row=5, column=2, padx=(5,10), pady=(10, 25),sticky=tk.NW)
        self.start_button.grid(row=6, column=0, padx=(20,15),columnspan = 3,sticky=tk.NW)
        self.stop_button.grid(row=7, column=0, padx=(20,15),columnspan = 3,pady=10,sticky=tk.NW)
        self.save_button.grid(row=8, column=0, padx=(20,15),columnspan = 3,sticky=tk.NW)
        #============================================================================

        self.ser_port_uC = ser.Serial(baudrate=115200,parity=ser.PARITY_NONE,stopbits=ser.STOPBITS_ONE,bytesize=ser.EIGHTBITS,timeout=0.5,inter_byte_timeout=0.1)  
        self.ser_port_DIS_X = ser.Serial(baudrate=9600,parity=ser.PARITY_NONE,stopbits=ser.STOPBITS_ONE,bytesize=ser.EIGHTBITS,timeout=0.5,inter_byte_timeout=0.1)  
        self.ser_port_DIS_Y= ser.Serial(baudrate=9600,parity=ser.PARITY_NONE,stopbits=ser.STOPBITS_ONE,bytesize=ser.EIGHTBITS,timeout=0.5,inter_byte_timeout=0.1) 

        self.run_exp1_state = 0
        self.start_exp1 = False       
        active_port_list = self.list_serial_ports()
        self.com_port_DIS_X.configure(values=active_port_list)
        self.com_port_DIS_Y.configure(values=active_port_list)
        self.com_port_uC.configure(values=active_port_list)
        self.horizontal_test_force = []
        self.record_timer = time.time()
        self.disable_widget()

    def list_serial_ports(self):
            if sys.platform.startswith('win'):
                ports = ['COM%s' % (i + 1) for i in range(1,40)]
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
        param_x = self.pressure_X_entry.get()
        param_y = self.pressure_Y_entry.get()
        try:
            int(param_x)
            int(param_y)
            check_flag = True
            logger.debug("xy params is integer")
        except:
            check_flag = False
            tk.messagebox.showerror(title="xy params error", message="ตรวจสอบ parameter x และ y",)
        return check_flag
    
    def start_button_pressed(self):
        self.monitor_text_box.delete("1.0",tk.END)
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
            self.pressure_X_entry.configure(state="disabled")
            self.pressure_Y_entry.configure(state="disabled")

            # self.horizontal_test_force = [*range(start,stop,step)]
            self.horizontal_test_force = [*range(10,100,2)]
            # print(self.horizontal_test_force)

            self.run_exp1_state = 0
            self.start_exp1 = True
            self.run_monotonic_tester()

    def stop_button_pressed(self):
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
        self.pressure_X_entry.configure(state = "normal")
        self.pressure_Y_entry.configure(state = "normal")
        self.start_exp1 = False
        self.run_exp1_state = 0

    def save_botton_pressed(self):
        print("SAVE")
     
    def run_monotonic_tester(self):
        # logger.debug(self.run_exp1_state)
        match(self.run_exp1_state):
            case 0:
                if self.start_exp1==True:
                    self.ser_port_uC.open()
                    self.ser_port_DIS_X.open()
                    self.ser_port_DIS_Y.open()
                    self.run_exp1_state = 1
                    self.after(2000,self.run_monotonic_tester)

            case 1:
                # print("case1")
                vertical_force = self.pressure_Y_entry.get()
                if self.ser_port_uC.is_open:
                    # print("open")
                    vertical_test_force = "N" + vertical_force + "\n" #============================== Y
                    vertical_test_force_bytes = vertical_test_force.encode()
                    # print(vertical_test_force_bytes)
                    self.ser_port_uC.write(vertical_test_force_bytes)
                    self.run_exp1_state = 2
                    self.after(100,self.run_monotonic_tester)

            case 2:
                setting_result = self.ser_port_uC.readline()
                setting_result_string = setting_result.strip().decode()
                # print("pressure_Y= "+setting_result_string)
                if setting_result_string == self.pressure_Y_entry.get():
                    # print("to 3")
                    self.run_exp1_state = 3
                else:
                    self.run_exp1_state = 1
                self.after(100,self.run_monotonic_tester)
                
            case 3:
                test_horizontal_force_string = f'T{self.horizontal_test_force[0]}\n'
                test_horizontal_force_bytes = test_horizontal_force_string.encode()
                self.ser_port_uC.write(test_horizontal_force_bytes)
                self.run_exp1_state = 4
                self.after(100,self.run_monotonic_tester)

            case 4:
                setting_result = self.ser_port_uC.readline()
                setting_result_string = setting_result.strip().decode()
                if setting_result_string == str(self.horizontal_test_force[0]):
                    self.run_exp1_state = 5
                    self.record_timer = time.time()
                    self.after(100,self.run_monotonic_tester)
                else:
                    self.run_exp1_state = 3
                    self.after(100,self.run_monotonic_tester)
            
            case 5:
                start_exp1 = "r1\n"
                start_exp1 = start_exp1.encode()
                self.ser_port_uC.write(start_exp1)
                self.after(100,self.run_monotonic_tester)
                self.run_exp1_state = 6

            case 6:        
                self.ser_port_uC.write(b'f\n')
                self.run_exp1_state = 7
                self.after(100,self.run_monotonic_tester)

            case 7:
                xy_force_bytes = self.ser_port_uC.readline()
                xy_force_string = xy_force_bytes.strip().decode()
                vertical_force,horizontal_force = xy_force_string.split(",")

                message_string = horizontal_force + "\t" + vertical_force
                logger.debug(message_string)

                horizontal_force = int(horizontal_force)
                vertical_force = int(vertical_force)
                vl_bound = int(self.pressure_Y_entry.get())-vf_gap
                vu_bound = int(self.pressure_Y_entry.get())+vf_gap
                hl_bound = self.horizontal_test_force[0] - hf_gap
                hu_bound = self.horizontal_test_force[0] + hf_gap
                if (horizontal_force >= hl_bound and horizontal_force <= hu_bound ) and (vertical_force >= vl_bound and vertical_force <= vu_bound):
                    self.run_exp1_state = 8
                else:
                    test_pass_time = time.time() - self.record_timer
                    if test_pass_time >= 10:
                        self.run_exp1_state = 9
                    else:
                        self.run_exp1_state = 6
                self.after(10,self.run_monotonic_tester)

            case 8:
                # save results
                logger.debug("save result here")
                if len(self.horizontal_test_force) > 1:
                    self.horizontal_test_force.pop(0)
                    self.run_exp1_state = 1
                else:
                    self.run_exp1_state = 9
                    self.ser_port_uC.write(b't\n')
                self.after(10,self.run_monotonic_tester)

            # case 8:
            #     pass

            case 9:
                self.ser_port_uC.write(b't\n')

            case _:
                pass



if __name__ == "__main__":
    app = App()
    app.eval('tk::PlaceWindow . center')
    app.mainloop()