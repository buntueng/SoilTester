from datetime import datetime
import time

start_time = time.time()

def format_time():
    t = datetime.now()
    s = t.strftime('%Y-%m-%d %H:%M:%S.%f')
    return s[:-3]

for i in range(50):
    # time_stamp = datetime.now().strftime("%H:%M:%S.%f")
    # time_stamp_in_millisec = datetime.now().strftime("%f")
    # time_stamp_in_millisec = int(time_stamp_in_millisec)
    # time_stamp_in_millisec_3digit = float('%f'%time_stamp_in_millisec)
    # time_in_x = (time.time()-start_time)
    # time_in_x = float('%.3f'%time_in_x)#time in X
    print((format_time()))
    time.sleep(0.04)

