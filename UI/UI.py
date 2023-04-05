import customtkinter as ctk
import tkinter as  tk
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,)
import serial as ser
import sys
import glob
from tkinter import messagebox
from get_data_displacement import linear_displacement
from datetime import datetime


ctk.set_appearance_mode("System") 
ctk.set_default_color_theme("blue") 
thai_large_font =("TH Niramit AS", 27,"bold")
thai_mid_font =("TH Niramit AS", 20,"bold")
eng_font = ("Time New Roman",25)
eng_small_font = ("Time New Roman",15)

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

        self.ser_port_uC = ser.Serial(baudrate = 115200,parity = ser.PARITY_NONE,   stopbits = ser.STOPBITS_ONE, bytesize = ser.EIGHTBITS,
        timeout=0.5,   inter_byte_timeout=0.1)  

        self.ser_port_DIS_X = ser.Serial(baudrate = 9600 ,parity = ser.PARITY_NONE,   stopbits = ser.STOPBITS_ONE, bytesize = ser.EIGHTBITS,
        timeout=0.5,   inter_byte_timeout=0.1)  
        
        self.ser_port_DIS_Y= ser.Serial(baudrate = 9600 ,parity = ser.PARITY_NONE,   stopbits = ser.STOPBITS_ONE, bytesize = ser.EIGHTBITS,
        timeout=0.5,   inter_byte_timeout=0.1) 

        self.run_exp1_state = 0
        self.run_start = False       
        active_port_list = self.list_serial_ports()
        self.com_port_DIS_X.configure(values=active_port_list)
        self.com_port_DIS_Y.configure(values = active_port_list)
        self.com_port_uC.configure(values = active_port_list)
        self.disable_widget()

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

    def disable_widget(self):
        self.start_button.configure(state = "normal")
        self.stop_button.configure(state="disabled")
        self.save_button.configure(state="disabled")

    def enable_widget(self):
        self.start_button.configure(state = "normal")

    def start_button_pressed(self):
        self.monitor_text_box.delete("1.0",tk.END)
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
            param_x = self.pressure_X_entry.get()
            param_y = self.pressure_Y_entry.get()
            if len(param_x)!= 0 and param_x != " " and param_x !="  " and param_x != "   ":
                if len(param_y)!= 0 and param_y != " " and param_y !="  " and param_y != "   ":
                    try:
                        self.ser_port_uC.port = uC_port
                        self.ser_port_DIS_X.port = disX
                        self.ser_port_DIS_Y.port = disY
                        self.ser_port_uC.open()
                        locked_port.remove(uC_port)
                        self.ser_port_DIS_X.open()
                        locked_port.remove(disX)
                        self.ser_port_DIS_Y.open()
                        locked_port.remove(disY)
                        self.enable_widget()
                        self.com_port_uC.configure(state="disabled")
                        self.com_port_DIS_X.configure(state="disabled")
                        self.com_port_DIS_Y.configure(state="disabled")
                        self.start_button.configure(state="disabled")
                        self.stop_button.configure(state="normal")
                        self.save_button.configure(state="normal")
                        self.start_button.configure(state = "disabled")
                        self.stop_button.configure(state="normal")
                        self.save_button.configure(state="normal")
                        self.pressure_X_entry.configure(state = "disabled")
                        self.pressure_Y_entry.configure(state = "disabled")
                        self.run_start = True
                        self.after(1000,self.run_monotonic_tester)
                    except:
                        error_message = "busy port:\n"
                        for port_name in locked_port:
                            error_message = error_message + port_name + "\n"
                        tk.messagebox.showerror(title="พอร์ตที่ใช้งานไม่ได้", message=error_message,)
                else:
                    messagebox.showwarning("WARNING", "คุณไม่ได้กรอก parameter Y")
            else:
                messagebox.showwarning("WARNING", "คุณไม่ได้กรอก parameter X")
        
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
        self.run_start = False
        self.run_exp1_state = 0
        self.obj_dis_x.stop()

    def save_botton_pressed(self):
        print("SAVE")
     
    def run_monotonic_tester(self):
        # print(self.run_exp1_state)
        match(self.run_exp1_state):
            case 0:
                if self.run_start == True:
                    self.run_exp1_state = 1
                    self.after(100,self.run_monotonic_tester)

            case 1:
                self.pres_X_get = self.pressure_X_entry.get()
                if self.pres_X_get != None:
                   if self.ser_port_uC.is_open:
                        max_horizontal_force = "T" + self.pres_X_get + "\n"
                        max_horizontal_force = max_horizontal_force.encode()
                        self.ser_port_uC.write(max_horizontal_force)
                        self.run_exp1_state = 2
                        self.after(100,self.run_monotonic_tester)

            case 2:
                self.pres_Y_get = self.pressure_Y_entry.get()
                if self.pres_Y_get != None:
                   if self.ser_port_uC.is_open:
                        fixed_vertical_force = "N" + self.pres_Y_get + "\n"
                        fixed_vertical_force = fixed_vertical_force.encode()
                        self.ser_port_uC.write(fixed_vertical_force)
                        self.run_exp1_state = 3
                        self.after(100,self.run_monotonic_tester)

            case 3:
                self.ser_port_uC.write(b'c\n')
                self.run_exp1_state = 4
                self.after(100,self.run_monotonic_tester)

            case 4:
                check_param = self.ser_port_uC.readline()
                check_param = check_param.decode().rsplit(",")
                check_fixed_vertical_force = check_param[0]
                check_max_horizontal_force = check_param[1]
                if check_max_horizontal_force == self.pres_X_get:
                    if check_fixed_vertical_force == self.pres_Y_get:
                        self.run_exp1_state = 5
                        self.after(100,self.run_monotonic_tester)
            
            case 5:        
                self.ser_port_DIS_X.close()
                self.obj_dis_x = linear_displacement(portname=self.com_port_DIS_X.get())
                self.obj_dis_x.run()
                self.run_exp1_state = 6
                self.after(100,self.run_monotonic_tester)


            case 6:
                out_data_dis_x = self.obj_dis_x.get_data()
                tim_now = datetime.now()
                time_stamp = tim_now.strftime("%H:%M:%S.%f")
                if out_data_dis_x != None:
                    try:
                        x_show3digit = f'{int(out_data_dis_x[:-2])*0.001:.3f}'
                        DIS_X_data = (x_show3digit + "," + time_stamp+"\n")
                        print(DIS_X_data)
                        self.monitor_text_box.insert("1.0",DIS_X_data)
                        # print(x_show3digit + "," + time_stamp)
                    except:
                        pass
                self.after(100,self.run_monotonic_tester)

            case 7:
                pass
                


            case _:
                pass



if __name__ == "__main__":
    app = App()
    app.eval('tk::PlaceWindow . center')
    app.mainloop()