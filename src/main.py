import asyncio
import esp32
import machine
from machine import deepsleep,Pin

from audio import play

async def main():
    await play()

if machine.reset_cause() == machine.DEEPSLEEP_RESET:
    asyncio.run(main())
pin = Pin(15,Pin.IN)

esp32.wake_on_ext1([pin],esp32.WAKEUP_ANY_HIGH if pin.value() == 0 else esp32.WAKEUP_ALL_LOW)
deepsleep()
