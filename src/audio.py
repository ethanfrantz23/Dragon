import asyncio
from machine import I2S
from machine import Pin


async def play():

    audio_out = I2S(
        0,
        sck=Pin(5),
        ws=Pin(4),
        sd=Pin(6),        
        ibuf=40000,
        mode=I2S.TX,
        bits=16,
        format=I2S.MONO,
        rate=16000,
    )

    wav = open("/files/{}".format("dragon.wav"), "rb")

    swriter = asyncio.StreamWriter(audio_out)

    _ = wav.seek(44)  # advance to first byte of Data section in WAV file

    # allocate sample array
    # memoryview used to reduce heap allocation
    wav_samples = bytearray(10000)
    wav_samples_mv = memoryview(wav_samples)

    # continuously read audio samples from the WAV file
    # and write them to an I2S DAC
    print("==========  START PLAYBACK ==========")

    while True:
        num_read = wav.readinto(wav_samples_mv)
        # end of WAV file?
        if num_read == 0:
            # end-of-file, return
            return
        else:
            # apply temporary workaround to eliminate heap allocation in uasyncio Stream class.
            # workaround can be removed after acceptance of PR:
            #    https://github.com/micropython/micropython/pull/7868
            # swriter.write(wav_samples_mv[:num_read])
            swriter.out_buf = wav_samples_mv[:num_read]
            await swriter.drain()
