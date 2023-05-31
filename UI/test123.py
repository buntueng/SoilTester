import time

t0 = time.time()
t0_int = f'{int(t0[:-2])*0.01:3f}'
# t0_show3digit = f'{int(t0[:-2])*0.001:.3f}'
while True:
    # t = time.time()
    # t_show3digit = f'{int(t[:-2])*0.001:.3f}'
    # time.sleep(0.01)
    # print(type(t))
    # print(t_show3digit-t0_show3digit) # ได้ 0.8062782287597656
    # t = time.time() # เวลาเริ่มต้น
    # t_int = t*0.01
    # <กลุ่มคำสั่งที่ต้องการจับเวลา>
    print(t0_int) # พิมพ์เวลาสุดท้ายลบด้วยเวลาเริ่มต้น
    time.sleep(0.04)