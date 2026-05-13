from machine import Pin, PWM
import asyncio

MIN = 700000
MAX = 2300000

class Servo:
    def __init__(self, pin):
        self.pwm = PWM(Pin(pin), freq=50)

    def set_angle(self,angle):
        pct = (angle+90)/180
        self.pwm.duty_ns(int(pct * (MAX - MIN) + MIN))        

async def animate_servo(servo, angles, duration, delay=0):
    await asyncio.sleep_ms(delay)
    for angle in angles:
        servo.set_angle(angle)
        await asyncio.sleep_ms(int(1000*duration/len(angles)))
    