import machine
import time
import network
import socket
import ujson
import _thread
from pimoroni import Button
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2, PEN_P4
from mywifi import networksetting
import ntptime
import utime
import jpegdec
from pimoroni import RGBLED

display = PicoGraphics(display=DISPLAY_PICO_DISPLAY_2, pen_type=PEN_P4, rotate=0)
display.set_backlight(0.5)
display.set_font("bitmap8")
button_a = Button(12)
button_b = Button(13)
button_x = Button(14)
button_y = Button(15)
wake_button = button_x
rgb_led = RGBLED(6, 7, 8)

WHITE = display.create_pen(255, 255, 255)
BLACK = display.create_pen(0, 0, 0)
CYAN = display.create_pen(0, 255, 255)
MAGENTA = display.create_pen(255, 0, 255)
YELLOW = display.create_pen(255, 255, 0)
GREEN = display.create_pen(0, 255, 0)
RED = display.create_pen(255, 0, 0)
BLUE = display.create_pen(0, 0, 255)

TIMEZONE_OFFSET = 2
MAX_ENTRIES = 7 

timestamps = {'A': None, 'B': None}

def clear():
    button_timer = 0
    display.set_pen(WHITE)
    display.clear()
    display.update()

def bag():
    button_timer = 0
    display.set_pen(WHITE)
    display.clear()
    WIDTH, HEIGHT = display.get_bounds()
    filename = "medicine.jpg"
    j = jpegdec.JPEG(display)
    j.open_file(filename)
    x = 0
    y = 0
    width = WIDTH
    height = HEIGHT

    j.decode(x,y,jpegdec.JPEG_SCALE_FULL, dither=False)
    display.update()
        

def log_delete():
    global button_pressed
    button_timer = 0
    button_pressed = False
    undo_button = 0
    clear()
    return button_pressed

def sync_time():
    print('Syncing time with NTP server...')
    ntptime.settime()
    print('Time synchronized')

def picoprogram():
        global button_pressed
        button_timer = 0
        button_pressed = False
        undo_button = 0
        clear()
        bag()
        reed = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_UP)
        last_state = reed.value()
        button_log = []
        box_log = []
        while True:
            val1= reed.value()
            time.sleep(0.01)
            val2= reed.value()
            if val1 and not val2:
                print('Boks lukket')
                clear()
                display.set_pen(BLUE)
                display.text("Boks lukkes", 10, 10, 240, 4)
                display.update()
                time.sleep(1)
                bag()
            elif not val1 and val2:
                print('Boks åbnet')
                print('Boks lukket')
                clear()
                display.set_pen(BLUE)
                display.text("Boks åbnes", 10, 10, 240, 4)
                display.update()
                time.sleep(1)
                bag()
        
            if button_a.read() and not button_pressed:
                clear()
                year, month, mday, hour, minute, second, weekday, yearday = utime.localtime(utime.time() + TIMEZONE_OFFSET * 3600)
                date_str = "{:04}-{:02}-{:02}".format(year, month, mday)
                time_str = "{:02}:{:02}:{:02}".format(hour, minute, second)
                datetime_str = "Dato: {} Tid: {}".format(date_str, time_str)
                print("Medicin givet:", date_str, "Tid:", time_str)
                display.set_pen(GREEN)
                display.text("MEDICIN GIVET" + datetime_str, 10, 10, 240, 4)
                display.update()
                rgb_led.set_rgb(0, 255, 0)
                undo_button =time.time()
                time.sleep(5)
                rgb_led.set_rgb(0, 0, 0)
                button_pressed = True
                bag()
            elif button_b.read():
                clear()
                year, month, mday, hour, minute, second, weekday, yearday = utime.localtime(utime.time() + TIMEZONE_OFFSET * 3600)
                date_str = "{:04}-{:02}-{:02}".format(year, month, mday)
                time_str = "{:02}:{:02}:{:02}".format(hour, minute, second)
                datetime_str = "Dato: {} Tid: {}".format(date_str, time_str)
                print("Utilsigtet hændelse", date_str, "Tid:", time_str)
                display.set_pen(RED)
                display.text("Utilsigtet hændelse"+ datetime_str, 10, 10, 240, 4)
                display.update()
                rgb_led.set_rgb(255, 0, 0)
                undo_button =time.time()
                time.sleep(5)
                button_pressed = True
                bag()
            elif button_x.read():
                clear()
                display.set_pen(BLUE)
                display.text("Skema for tryk på knap A:", 10, 10, 240, 4)
                display.text("Skema for tryk på knap B:", 10, 90, 240, 4)
                display.update()
                time.sleep(1)
                bag()
            elif button_y.read():
                if undo_button != 0 and time.time() - undo_button <=10:
                    clear()
                    display.set_pen(RED)
                    display.text("Fortryd", 10, 10, 240, 4)
                    undo_button = 0
                    button_pressed = False
                    rgb_led.set_rgb(0, 0, 0)
                    display.update()
                    time.sleep(1)
                    bag()
                if undo_button != 0 and time.time() - undo_button >10:
                    clear()
                    display.set_pen(RED)
                    display.text("For sent", 10, 10, 240, 4)
                    undo_button = 0
                    display.update()
                    time.sleep(1)
                    bag()
                button_timer += 1
                if button_timer >=2:
                    clear()
                    display.set_pen(BLUE)
                    display.text("Log ryddet", 10, 10, 240, 4)
                    rgb_led.set_rgb(0, 0, 0)
                    display.update()
                    time.sleep(1)
                    button_pressed = log_delete()
                    bag()
                    '''
            else:
                button_timer = 0
                display.set_pen(BLACK)
                display.text("Startskærm", 10, 10, 240, 4)
                display.update()
                time.sleep(0.1)
                '''
            
            
def andriodapp():
    ssid, password = networksetting()

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    
    max_wait = 10
    print('Waiting for connection')
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1    
        time.sleep(1)
    status = None
    if wlan.status() != 3:
        raise RuntimeError('Connections failed')
    else:
        status = wlan.ifconfig()
        print('Connection to', ssid, 'successfully established!', sep=' ')
        print('IP-address: ' + status[0])
    ipAddress = status[0]

    led = machine.Pin("LED", machine.Pin.OUT)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', 5000))
    s.listen(1)
    print('Waiting for a connection...')

    while True:
        conn, addr = s.accept()
        print('Connection from', addr)

        
        data = conn.recv(1024).decode()
        print(data)
        command = ujson.loads(data)
        print(command)

        
        if command['gpio'] == 'on':
            print('Turning LED on...')
            led.value(1)
        elif command['gpio'] == 'off':
            print('Turning LED off...')
            led.value(0)
        else:
            print('Error')
        conn.close()


sync_time()
_thread.start_new_thread(picoprogram, ())


andriodapp()


