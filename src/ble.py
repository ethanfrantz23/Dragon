import aioble
import asyncio
import bluetooth

KILL_PRINCE_SERVICE_UUID = bluetooth.UUID("bc5639d4-486b-4163-9cff-b8f9b9300281")
KILL_PRINCE_CHARACTERISTIC_UUID = bluetooth.UUID('9e25a6f5-1b35-4001-849c-208384667707')

async def killPrince():
    async with aioble.scan(duration_ms=5000, interval_us=30000, window_us=30000, active=True) as scanner:
        found=[]
        princes = []
        async for result in scanner:
            a = result.device.addr_hex()
            if a not in found:
                print('device: ', a)
                found.append(a)
                for service in result.services():            
                    print('service: ', service)
                    if service == KILL_PRINCE_SERVICE_UUID:
                        princes.append(result)
                print('========================================')
                    
        for prince in princes:
            print('prince: ', prince)
            try:
                connection = await prince.device.connect(timeout_ms=2000)
                print('connected to prince')
                service = await connection.service(KILL_PRINCE_SERVICE_UUID)
                char = await service.characteristic(KILL_PRINCE_CHARACTERISTIC_UUID)
                await char.write(b'KILL')
            except asyncio.TimeoutError:
                print('Timeout')
        
        