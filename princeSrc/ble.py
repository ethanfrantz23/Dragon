import aioble
import asyncio
import bluetooth

KILL_PRINCE_SERVICE_UUID = bluetooth.UUID("bc5639d4-486b-4163-9cff-b8f9b9300281")
KILL_PRINCE_CHARACTERISTIC_UUID = bluetooth.UUID('9e25a6f5-1b35-4001-849c-208384667707')

_ADV_INTERVAL_US = const(250000)

kill_prince_service = aioble.Service(KILL_PRINCE_SERVICE_UUID)
kill_prince_char = aioble.Characteristic(kill_prince_service, KILL_PRINCE_CHARACTERISTIC_UUID, read=True, write=True, notify=True)

aioble.register_services(kill_prince_service)

async def TaskCanceler(task,cancel):
    try:
        return await task
    finally:
        cancel.cancel()

async def wait_for_connection():
    while True:
        async with await aioble.advertise(
                _ADV_INTERVAL_US,
                name="Prince Philip",
                services=[KILL_PRINCE_SERVICE_UUID],
                appearance=0x0000,
                manufacturer=(0xabcd, b"1234"),
            ) as connection:
            print("Connection from", connection.device)
            t1 = asyncio.create_task(wait_for_kill_prince())
            t2 = asyncio.create_task(TaskCanceler(connection.disconnected(timeout_ms=None), t1))
            await asyncio.gather(t1, t2)
            print("Disconnected from", connection.device)

async def wait_for_kill_prince():
    await kill_prince_char.written(timeout_ms=None)
    print("Kill Prince written:", kill_prince_char.read())

async def run():
    await wait_for_connection()
    