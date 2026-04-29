from machine import Pin, PWM

MIN = 700000
MAX = 2300000

class Servo:
    def __init__(self, pin):
        self.pwm = PWM(Pin(pin), freq=50)

    def set_angle(self,angle):
        pct = (angle+90)/180
        self.pwm.duty_ns(int(pct * (MAX - MIN) + MIN))        
