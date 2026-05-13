import asyncio
import esp32
import json
import machine
from machine import deepsleep,Pin
import time

from audio import play
from servo import animate_servo, Servo

async def main():
    with open('files/angles.json', 'r') as f:
        angles = json.load(f)
    servo = Servo(1)
    await asyncio.gather(play(), animate_servo(servo, angles, 2, 800))

print('reset cause: ', machine.reset_cause())
if machine.reset_cause() == machine.DEEPSLEEP_RESET:
    print('running code')
    asyncio.run(main())
pin = Pin(2,Pin.IN,Pin.PULL_UP, hold=True)
print('setting up deep sleep hold')
esp32.gpio_deep_sleep_hold(True)
print('setting up wake on ext1')
esp32.wake_on_ext1([pin],esp32.WAKEUP_ANY_HIGH if pin.value() == 0 else esp32.WAKEUP_ALL_LOW)
print('waiting for 1 second')
time.sleep(1)
print('going to deep sleep')
deepsleep()
