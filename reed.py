import machine
import time

reed = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_UP)

while True:
    val1= reed.value()
    time.sleep(0.01)
    val2= reed.value()
    if val1 and not val2:
       print('Boks lukket')
    elif not val1 and val2:
       print('Boks åbnet')