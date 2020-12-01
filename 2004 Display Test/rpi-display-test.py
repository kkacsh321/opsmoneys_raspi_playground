# This requires rpi-displays to be already installed `pip install rpi-display`
from rpi_displays.sainsmart.displays import LCD2004
from time import sleep
from datetime import datetime
import os
import psutil
import socket

lcd = LCD2004()

def get_ip_address():
 ip_address = '';
 s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
 s.connect(("8.8.8.8",80))
 ip_address = s.getsockname()[0]
 s.close()
 return ip_address

def get_cpu_temp():     # get CPU temperature and store it into file "/sys/class/thermal/thermal_zone0/temp"
    tmp = open('/sys/class/thermal/thermal_zone0/temp')
    cpu = tmp.read()
    tmp.close()
    return '{:.2f}'.format( float(cpu)/1000 ) + ' C'
 
def get_time_now():     # get system time
    return datetime.now().strftime('    %H:%M:%S')

def memory():
    memory = psutil.virtual_memory()
    # available = round(memory.available/1024.0/1024.0,1)
    used = round(memory.used/1024.0/1024.0,1)
    total = round(memory.total/1024.0/1024.0,1)
    # return str(available) + 'MB free / ' + str(total) + 'MB total ( ' + str(memory.percent) + '% )'
    return 'MEM:' + str(used) + 'MB/' + str(total) + 'MB' 

def loop():
    lcd.switch_backlight(1)     # turn on LCD backlight
    while(True):         
        lcd.clear()
        lcd.display_string( 'CPU: ' + get_cpu_temp(), 1 )# display CPU temperature
        lcd.display_string( memory(), 2 )
        lcd.display_string( get_time_now(), 3 )   # display the time
        lcd.display_string( get_ip_address(), 4 )
        sleep(5)
        lcd.clear()
        lcd.display_string( "********************", 1 )
        lcd.display_string( "*     Have A       *", 2 )
        lcd.display_string( "*  Fantastic Day!  *", 3 )
        lcd.display_string( "********************", 4 )
        sleep(5)
        lcd.clear()
        lcd.switch_backlight(0)

def destroy():
    lcd.clear()
    lcd.switch_backlight(0)

if __name__ == '__main__':
    print ('Program is starting ... ')
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
