from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2 as DISPLAY
display = PicoGraphics(display=DISPLAY)

import jpegdec

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