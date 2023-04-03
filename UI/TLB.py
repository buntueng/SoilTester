import tkinter  as tk
from tkinter import ttk
from tkinter import messagebox
import customtkinter
from sticker_label import generate_stcker_label,print_sticker,generate_white_stcker_label
from pathlib import Path
from PIL import Image,ImageTk
from mysql.connector import connect
import time
import serial
import threading
import logging
import ctypes
from win32con import WM_INPUTLANGCHANGEREQUEST
from win32gui import GetForegroundWindow
from win32api import SendMessage


# ======================== add logging =========================
logger = logging.getLogger('main_logger')
logger.setLevel(logging.DEBUG)
logging_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

fileHandler = logging.FileHandler(filename="./software_log.log")
fileHandler.setFormatter(logging_format)
logger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logging_format)
logger.addHandler(consoleHandler)


customtkinter.set_appearance_mode("System") 
customtkinter.set_default_color_theme("blue")  

current_path = Path(__file__).resolve().parents[0]
barcode1_file_path = Path(current_path, 'barcode1.png')
barcode2_file_path = Path(current_path, 'barcode2.png')

thai_large_font =("TH Niramit AS", 37)
thai_font = ("TH Niramit AS", 50)
thai_small_front = ("TH Niramit AS", 15)
eng_font = ("Time New Roman",20)

comport = 'COM5'
ser = serial.Serial(port=comport,baudrate=115200,timeout=2)
# time.sleep(1.5)

class App(customtkinter.CTk,):
    width = 965
    height = 730
    label_list = []
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.character_dict = {3615:'a',3636:'b',3649:'c',3585:'d',3635:'e',3604:'f',3648:'g',3657:'h',3619:'i',3656:'j',3634:'k',3626:'l',3607:'m'
                              ,3639:'n',3609:'o',3618:'p',3654:'q',3614:'r',3627:'s',3632:'t',3637:'u',3629:'v',3652:'w',3611:'x',3633:'y',3612:'z'
                              ,3620:'A',3642:'B',3593:'C',3599:'D',3598:'E',3650:'F',3596:'G',3655:'H',3603:'I',3659:'J',3625:'K',3624:'L',63:'M'
                              ,3660:'N',3631:'O',3597:'P',3664:'Q',3601:'R',3590:'S',3608:'T',3658:'U',3630:'V',34:'W',41:'X',3661:'Y',40:'Z'
                              ,3653:'1',47:'2',45:'3',3616:'4',3606:'5',3640:'6',3638:'7',3588:'8',3605:'9',3592:'0'}

        self.title("Tube Labeling")
        self.iconbitmap("hospital.ico")
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(False, False)

        self.thread_is_running = False

        self.entry_stringvar = tk.StringVar()
        # self.entry_stringvar.trace("w", lambda name, index,mode, var=self.entry_stringvar: self.test_insert(var))

        self.master_frame = customtkinter.CTkFrame(self,fg_color="skyblue1")
        self.master_frame.pack(pady=5, padx=5, fill="both", expand=True)

        self.top_frame = customtkinter.CTkFrame(master=self.master_frame,fg_color="skyblue1")
        self.top_frame.grid(row=0,column=0,pady=(5,5), padx=(5,0),sticky=tk.N)


        self.mid_left_frame = customtkinter.CTkFrame(master=self.master_frame,fg_color="skyblue1",)
        self.mid_left_frame.grid(row=2,column=0,pady=(5,0), padx=(5,0),sticky=tk.N)
        #==================================== top frame =====================================
        self.lab_number_label = customtkinter.CTkLabel(master=self.top_frame, text=" LN ",font=("TH Niramit AS", 60,"bold"))
        
        self.lab_namber_entry = customtkinter.CTkEntry(master=self.top_frame,placeholder_text="Lab number",width=700,height=50,font=("TH Niramit AS", 50,"bold"),corner_radius=15,textvariable=self.entry_stringvar)
        self.barcode_button = customtkinter.CTkButton(master=self.top_frame,text="ตกลง",width=100,height=50,font=("TH Niramit AS", 50,"bold"),command=self.barcode_button_pressed)

        self.lab_number_label.grid(row=0, column=0,  padx=10,  pady=(10,0))
        self.lab_namber_entry.grid(row=0, column=1,padx=5,  pady=(10,0))
        self.barcode_button.grid(row=0, column=2,padx=(10,10), pady=(10,0))
        #==================================== mid left frame ==========================================
        self.preview_cavas = customtkinter.CTkCanvas(master=self.mid_left_frame, bg='#FFFFFF', width=900, height=450,)
   
        self.preview_cavas.grid(row=0,column=0,padx=(20,0),pady=5,sticky=tk.NW,)

        # =========================== events binding =========================================
        self.create_treeview()
        self.bind('<Return>',self.insert_treeview)

        self.print_hn = None
        self.print_fname = None
        self.print_surname = None
        self.print_title_name = None
        self.print_box = None
        self.print_age = None
        self.print_lab_section = None
        self.print_info = None
        self.print_status = None
        self.insert_fname = None
        self.insert_surname = None
        self.insert_title_name = None
        self.insert_print_status = None
        self.sticker_image = None
        self.exit_state_loop = False

        self.run()
        self.run_change_key()
    #=================================== run thread Change_keyboard_language ==================================
    def run_change_key(self):
        lang = threading.Thread(target = self.Change_keyboard_language)
        lang.start()
    #========================================= Change_keyboard_language =======================================
    def Change_keyboard_language(self):
        while True:
            w_handle = (ctypes.windll.user32.GetForegroundWindow())
            w_tid = (ctypes.windll.user32.GetWindowThreadProcessId(w_handle, "x"))
            layout=ctypes.windll.user32.GetKeyboardLayout(w_tid)
            if layout==-255851511:
                pass
            else:
                if layout==67699721:
                    pass
                else:
                    if layout==-69075998:
                        pass
                    else:
                        if SendMessage( GetForegroundWindow(), WM_INPUTLANGCHANGEREQUEST, 0, 0x4090409) == 0:
                            logger.debug('change_language_success')
                            
            time.sleep(1)
    #=====================================================================================
    def create_treeview(self):
        treeview_style = ttk.Style()
        treeview_style.configure("custom.Treeview", highlightthickness=10, bd=10, font=('Time New Roman', 10))
        treeview_style.configure("custom.Treeview.Heading", font=('TH Niramit AS', 12,'bold'))
        treeview_style.layout("custom.Treeview", [('custom.Treeview.treearea', {'sticky': 'nswe'})])
        treeview_style.configure("custom.Treeview", background="#BBFFFF",fieldbackground="black", foreground="black")
        treeview_style.map("custom.Treeview", background=[("selected", "seagreen4")])

        cass_name_treeview_colum = ("cass_name","LN",)
        self.tlb_table_summary_treeview = ttk.Treeview(self.master_frame, columns=cass_name_treeview_colum, style="custom.Treeview", show='headings',height=6)
        self.tlb_table_summary_treeview.heading("cass_name",text="ชื่อ")
        self.tlb_table_summary_treeview.column("cass_name", width=500,anchor=tk.CENTER)
        self.tlb_table_summary_treeview.heading("LN",text="LN")
        self.tlb_table_summary_treeview.column("LN", width=400,anchor=tk.CENTER)
        self.tlb_table_summary_treeview.grid(row=1, column=0, padx=(30,5),sticky=tk.NW)

    def update_print_status(self):
                db_connector =  connect(host="localhost", user="root", port = 3333, passwd="edgelabeling555",  database="sbj",  charset="utf8"  )
                database_cursor = db_connector.cursor()
                sql_query = f'UPDATE lab_label       \
                              SET print_status = 1   \
                              WHERE lab_label.lab_order_number = {self.first_get_ln} LIMIT 1'
                database_cursor.execute(sql_query)
                db_connector.commit()
                db_connector.close()

    def re_print_status(self):
                db_connector =  connect(host="localhost", user="root", port = 3333, passwd="edgelabeling555",  database="sbj",  charset="utf8"  )
                database_cursor = db_connector.cursor()
                sql_query = f'UPDATE lab_label       \
                              SET print_status = 0   \
                              WHERE lab_label.lab_order_number = {self.ln_number} LIMIT 1'
                database_cursor.execute(sql_query)
                print(self.ln_number)
                db_connector.commit()
                db_connector.close()
    
    def insert_treeview(self,e):
        count_ln_entry = self.lab_namber_entry.get()
        
        if len(count_ln_entry) >0:
            try:
                self.ln_number = self.lab_namber_entry.get()
                self.lab_namber_entry.delete(0,'end')
                # #============================================================================================
                db_connector =  connect(host="localhost", user="root", port = 3333, passwd="edgelabeling555",  database="sbj",  charset="utf8"  )
                database_cursor = db_connector.cursor()
                sql_query = f'SELECT fname,surname,title,print_status \
                            FROM lab_label,lab_main \
                            WHERE lab_label.lab_order_number = {self.ln_number} and lab_label.lab_order_number = lab_main.lab_order_number LIMIT 1'
                database_cursor.execute(sql_query)
                result_list = database_cursor.fetchall()
                db_connector.close()

                if len(result_list)>0:
                    self.insert_fname = result_list[0][0].decode('utf8') #========= Fname
                    self.insert_surname = result_list[0][1].decode('utf8') #========= surname
                    self.insert_title_name = result_list[0][2].decode('utf8') #========= title name
                    self.insert_print_status = result_list[0][3] #====== print_status

                    if self.insert_print_status == 0:
                        self.tlb_table_summary_treeview.insert("",'end',values=((self.insert_title_name,self.insert_fname,self.insert_surname),self.ln_number,))
                        self.lab_namber_entry.delete(0,'end')
                    if self.insert_print_status == 1:
                        chack_re_print = messagebox.askquestion("warning","     คุณเคย Print ไปแล้ว"+"\n"+"\n"+"ต้องการ Print ใหม่หรือไม่")
                        if chack_re_print == "yes":
                            self.tlb_table_summary_treeview.insert("",'end',values=((self.insert_title_name,self.insert_fname,self.insert_surname),self.ln_number,))
                            self.re_print_status()
                        else:
                            pass
            except:
                logger.info('can not find this LN in database')
        else:
            messagebox.showwarning("ERROR", "CAN NOT SEARCH")

    def clear_treeview(self):
        self.tlb_table_summary_treeview.delete(self.tlb_table_summary_treeview.get_children()[0])
    
    def search_ln(self):
        try:
            #================================== PRINT ============================================
            first_item_treeview = self.tlb_table_summary_treeview.get_children()[0]
            self.first_get_ln = self.tlb_table_summary_treeview.item(first_item_treeview)["values"][1]

            db_connector =  connect(host="localhost", user="root", port = 3333, passwd="edgelabeling555",  database="sbj",  charset="utf8"  )
            database_cursor = db_connector.cursor()
            sql_query = f'SELECT hn,fname,surname,title,box,age,lab_section,testprint,print_status \
                        FROM lab_label,lab_main \
                        WHERE lab_label.lab_order_number = {self.first_get_ln} and lab_label.lab_order_number = lab_main.lab_order_number LIMIT 1'
            database_cursor.execute(sql_query)
            result_list = database_cursor.fetchall()
            db_connector.close()

            if len(result_list)>0:
                self.print_hn = result_list[0][0].decode('utf8') #========= HN
                self.print_fname = result_list[0][1].decode('utf8') #========= Fname
                self.print_surname = result_list[0][2].decode('utf8') #========= surname
                self.print_title_name = result_list[0][3].decode('utf8') #========= title name
                self.print_box = result_list[0][4] #====== BOX
                self.print_age = result_list[0][5].decode('utf8') #====== AGE
                self.print_lab_section = result_list[0][6].decode('utf8') #======= WARD
                self.print_info = result_list[0][7]
                self.print_status = result_list[0][8]

            self.white_sticker_image = generate_white_stcker_label()
            self.sticker_image = None

            if self.print_status == 0:
                self.sticker_image = generate_stcker_label(hn=self.print_hn,title=self.print_title_name,fname=self.print_fname,surname=self.print_surname,lab_order=self.first_get_ln
                                                            ,age=self.print_age,ward=self.print_lab_section,test_label=self.print_info)
                sticker_image_resize = self.sticker_image.resize((900,450),Image.Resampling.LANCZOS)
                self.photo_label1 = ImageTk.PhotoImage(sticker_image_resize)
                self.preview_cavas.create_image(450,225,image=self.photo_label1)
                self.exit_state_loop = False
                return True
            else:
                return False
        except:
            logger.info('NO PRINTER IMAGE')
            return False

    #============================================================================================
    def run(self):
        t1 = threading.Thread(target = self.run_machine)
        t1.start()
    
    def run_machine(self):
        state_machine = 0
        sleep_time = 0.2
        count_error = 0
        jam_counter = 0
        while True:
            # message = f"current state = {state_machine}"
            # logger.debug(message)
            match state_machine:
                case 0:
                    self.count_list_tree = self.tlb_table_summary_treeview.get_children()
                    if len(self.count_list_tree) > 0:
                        state_machine = 1
                case 1:
                    self.search_ln()
                    # sleep_time=2 #============== DEBUG =================
                    if self.sticker_image != None:
                        print_sticker(self.sticker_image)
                    state_machine = 2
                    sleep_time = 2.5
                case 2:
                    sleep_time = 0.3
                    box_location = self.print_box
                    match box_location:
                        case "1":
                            ser.write(b'1g1\n')
                            state_machine = 3
                        case "2":
                            ser.write(b'1g2\n')
                            state_machine = 3
                        case "3":
                            ser.write(b'1g3\n')
                            state_machine = 3
                        case "4":
                            ser.write(b'1g4\n')
                            state_machine = 3
                        case "5":
                            ser.write(b'1g5\n')
                            state_machine = 3
                        case "6":
                            ser.write(b'1g6\n')
                            state_machine = 3
                        case _:
                            pass
                case 3:
                    self.read_cmd = ser.readline()
                    read_cmd = self.read_cmd.strip()
                    if read_cmd == b'run machine':
                        state_machine = 4
                    elif read_cmd == b'stop machine':
                        state_machine = 100
                    elif read_cmd == b'printer module not response':
                        state_machine = 100
                    elif read_cmd == b'sliding not origin':
                        state_machine = 100
                    elif read_cmd == b'prox sensor error':
                        state_machine = 100
                    elif read_cmd == b'limit switch':
                        state_machine = 100
                    elif read_cmd == b'silo module not response':
                        state_machine = 100
                    elif read_cmd == b'tube jam':
                        state_machine = 100
                    elif read_cmd == b'printer module not response':
                        state_machine = 100
                    elif read_cmd == b'try condition error':
                        state_machine = 100    
                    elif read_cmd == b'running_error':
                        state_machine = 100 
                    else:
                        pass
                case 4:
                    ser.write(b'1c\n')
                    state_machine = 5
                case 5:
                    self.read_cmd = ser.readline()
                    read_cmd = self.read_cmd.strip()
                    match read_cmd:
                        case b'complete':
                            state_machine = 6
                        case b'stop machine':
                            state_machine = 100
                        case b'printer module not response':
                            state_machine = 100
                        case b'sliding not origin':
                            state_machine = 100
                        case b'prox sensor error':
                            state_machine = 100
                        case b'limit switch':
                            state_machine = 100
                        case b'silo module not response':
                            state_machine = 100
                        case b'tube jam':
                            jam_counter = jam_counter + 1
                            state_machine = 100
                        case b'printer module not response':
                            state_machine = 100
                        case b'try condition error':
                            state_machine = 100    
                        case b'running_error':
                            state_machine = 100    
                        case _:
                            ser.flushInput()
                            state_machine = 4
                case 6:
                    self.preview_cavas.delete("all")
                    self.clear_treeview()
                    self.update_print_status()
                    state_machine = 0
                case 100:
                    ser.write(b'1r\n')
                    state_machine = 101
                    count_error = count_error + 1
                case 101:
                    ser.write(b'1c\n')
                    state_machine = 102
                    time.sleep(3.5)
                case 102:
                    self.read_cmd = ser.readline()
                    read_cmd = self.read_cmd.strip()

                    match read_cmd:
                        case b'idle':
                            state_machine = 0
                            logger.debug("Redy")
                        case _:
                            ser.flushInput()
                            state_machine = 101
                    if count_error == 3:
                        msg = messagebox.askquestion("the machine has a problem","คุณแก้ไขแล้วหรือยัง")
                        if msg =="yes":
                            count_error = 0
                            state_machine = 0
                        else :
                            state_machine = 1000
                    if jam_counter == 3:
                        msg = messagebox.askquestion(f"Tube jam","หลอดติดที่ตำแหน่ง "+str(box_location)+"\n"+" คุณแก้ไขแล้วหรือยัง ")
                        if msg =="yes":
                            jam_counter = 0
                            state_machine = 0 
                        else:
                            state_machine = 1000
                case _:
                    ser.readline()
                    sleep_time = 10
            time.sleep(sleep_time)

    #==========================================================================================================
    def barcode_button_pressed(self):
        # print_sticker(self.sticker_image)
        pass



if __name__ == "__main__":
    customtkinter.set_appearance_mode("light")
    app = App()
    app.eval('tk::PlaceWindow . center')
    app.mainloop()
