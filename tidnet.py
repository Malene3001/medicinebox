import network
import ntptime
import utime
from machine import Pin

SSID = ''
PASSWORD = ''

button = Pin(12, Pin.IN, Pin.PULL_UP)
TIMEZONE_OFFSET = 2

def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    
    while not wlan.isconnected():
        pass
    
    print('Connected to WiFi')
    print('Network config:', wlan.ifconfig())

def sync_time():
    print('Syncing time with NTP server...')
    ntptime.settime()
    print('Time synchronized')

def button_pressed(pin):
    year, month, mday, hour, minute, second, weekday, yearday = utime.localtime(utime.time() + TIMEZONE_OFFSET * 3600)
    date_str = "{:04}-{:02}-{:02}".format(year, month, mday)
    time_str = "{:02}:{:02}:{:02}".format(hour, minute, second)
    print("Dato:", date_str, "Tid:", time_str)

connect_to_wifi()
sync_time()
button.irq(trigger=Pin.IRQ_FALLING, handler=button_pressed)

while True:
    utime.sleep(1)
