import asyncio
from machine import Pin
from neopixel import NeoPixel

pin = Pin(18, Pin.OUT)
np = NeoPixel(pin, 1)

class ColorMode:
    RGB = 0
    GRB = 1

RED = const((255,0,0))
GREEN = const((0,255,0))
BLUE = const((0,0,255))
YELLOW = const((255,255,0))
ORANGE = const((250,80,0))
WHITE = const((255,255,255))
PURPLE = const((255,0,255))

COLOR_MODE = ColorMode.GRB

def convertAndWrite(np):
    if COLOR_MODE == ColorMode.GRB:
        for i in range(np.n):
            np[i] = (np[i][1],np[i][0],np[i][2])
    np.write()

async def Fade(color,color2=(0,0,0),speed=1,cycles=None):
    try:
        await asyncio.sleep_ms(50)
        diff = tuple(c-c2 for c,c2 in zip(color,color2))
        delta = tuple(n / 30 for n in diff)
        slp = int(500 / speed / 30)

        x = 0
        while cycles is None or cycles > x:
            x += 1
            for i in range(30):
                np[0] = tuple(int(d*i)+c for d,c in zip(delta,color2))
                convertAndWrite(np)
                await asyncio.sleep_ms(slp)

            for i in range(30,0,-1):
                np[0] = tuple(int(d*i)+c for d,c in zip(delta,color2))
                convertAndWrite(np)
                await asyncio.sleep_ms(slp)
    except asyncio.CancelledError:
        #ignore
        pass
    finally:
        #always turn off when done
        np[0] = (0,0,0)
        convertAndWrite(np)
        

async def Set(color=None,brightness=1):
    if color:
        await asyncio.sleep_ms(50)
    np[0] = tuple(int(x*brightness) for x in color) if color else (0,0,0)
    convertAndWrite(np)

async def Flash(color,color2=(0,0,0),speed=1,cycles=None):
    try:
        await asyncio.sleep_ms(50)
        slp = int(500 / speed)
        x = 0
        while cycles is None or cycles > x:
            x += 1
            np[0] = color
            convertAndWrite(np)
            await asyncio.sleep_ms(slp)
            
            np[0] = color2
            convertAndWrite(np)
            await asyncio.sleep_ms(slp)
    except asyncio.CancelledError:
        #ignore
        pass
    finally:
        #always turn off when done
        np[0] = (0,0,0)
        convertAndWrite(np)
        