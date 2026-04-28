import os
import time
from machine import Pin

from wavplayer import WavPlayer

wp = WavPlayer(
    id=0,
    sck_pin=Pin(5),
    ws_pin=Pin(4),
    sd_pin=Pin(6),
    ibuf=40000,
    root='/files',
)

wp.play("dragon.wav", loop=False)
# wait until the entire WAV file has been played
while wp.isplaying() == True:
    # other actions can be done inside this loop during playback
    pass
