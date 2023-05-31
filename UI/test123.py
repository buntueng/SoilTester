import time

t = time.time() # เวลาเริ่มต้น
while True:
    t0 = (time.time()-t)
    print('%.3f'%t0)
    time.sleep(0.04)

# f = 156.36595
# print( 'f = '+str(f) )
# print( 'f .1f = %.1f' %f )
# print( 'f .2f = %.2f' %f )
# print( 'f .3f = %.3f' %f )
# print( 'f .4f = %.4f' %f )
# print( 'f .5f = %.5f' %f )