import time
from pimoroni import Button
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2, PEN_P4


display = PicoGraphics(display=DISPLAY_PICO_DISPLAY_2, pen_type=PEN_P4, rotate=0)
display.set_backlight(0.5)
display.set_font("bitmap8")


button_a = Button(12)
button_b = Button(13)
button_x = Button(14)
button_y = Button(15)


WHITE = display.create_pen(255, 255, 255)
BLACK = display.create_pen(0, 0, 0)
CYAN = display.create_pen(0, 255, 255)
MAGENTA = display.create_pen(255, 0, 255)
YELLOW = display.create_pen(255, 255, 0)
GREEN = display.create_pen(0, 255, 0)
RED = display.create_pen(255, 0, 0)
BLUE = display.create_pen(0, 0, 255)

button_timer = 0
button_pressed = False
undo_button = 0

def clear():
    button_timer = 0
    display.set_pen(WHITE)
    display.clear()
    display.update()
    
def log_delete(button_pressed):
    button_timer = 0
    button_pressed = False
    undo_button = 0
    clear()
    return button_pressed

clear()


while True:    
    if button_a.read() and not button_pressed:
        clear()
        display.set_pen(GREEN)
        display.text("Medicin givet", 10, 10, 240, 4)
        display.update()
        undo_button =time.time()
        time.sleep(1)
        button_pressed = True
        clear()
    elif button_b.read():
        clear()
        display.set_pen(RED)
        display.text("Medicin ikke givet", 10, 10, 240, 4)
        display.update()
        time.sleep(1)
        clear()
    elif button_x.read():
        clear()
        display.set_pen(BLUE)
        display.text("X", 10, 10, 240, 4)
        display.update()
        time.sleep(1)
        clear()
    elif button_y.read():
        if undo_button != 0 and time.time() - undo_button <=10:
            clear()
            display.set_pen(RED)
            display.text("Fortryd", 10, 10, 240, 4)
            undo_button = 0
            button_pressed = False
            display.update()
            time.sleep(1)
            clear()
        if undo_button != 0 and time.time() - undo_button >10:
            clear()
            display.set_pen(RED)
            display.text("For sent", 10, 10, 240, 4)
            undo_button = 0
            display.update()
            time.sleep(1)
            clear()
        button_timer += 1
        if button_timer >=2:
            clear()
            display.set_pen(BLUE)
            display.text("Log ryddet", 10, 10, 240, 4)
            display.update()
            time.sleep(1)
            button_pressed = log_delete(button_pressed)
            clear()
    else:
        button_timer = 0
        display.set_pen(BLACK)
        display.text("Startskærm", 10, 10, 240, 4)
        display.update()
    time.sleep(0.1)