import os
import pyaudio
import json
import sys
from vosk import Model, KaldiRecognizer
import asyncio
from pyartnet import ArtNetNode

#Artnet function
async def artnet_menu(channel_num):
    # Run this code in your async function
    node = ArtNetNode('127.0.0.1', 6454)

    # Create universe 0
    universe = node.add_universe(0)

    # Add a channel to the universe which consists of 3 values
    # Default size of a value is 8Bit (0..255) so this would fill
    # the DMX values 1..3 of the universe
    channel = universe.add_channel(start=1, width=1)

    # Fade channel to 255,0,0 in 5s
    channel.add_fade([channel_num],0)
    # this can be used to wait till the fade is complete
    await channel

    channel.add_fade([0],0)
    # this can be used to wait till the fade is complete
    await channel

#Switch case function too send artnet commands
def switch_case(case):
    if case == 'A':
        asyncio.run(artnet_menu(1))
    elif case == 'B':
        asyncio.run(artnet_menu(2))
    elif case == 'C':
        asyncio.run(artnet_menu(3))
    elif case == 'D':
        asyncio.run(artnet_menu(4))
    elif case == 'E':
        asyncio.run(artnet_menu(5))
    else:
        print('Default case')

#Speech recognition function using vosk
def recognize_speech():
    model_path = "model"
    if not os.path.exists(model_path):
        print(f"Model not found in '{model_path}'. Please download and extract the model.")
        sys.exit(1)

    model = Model(model_path)
    recognizer = KaldiRecognizer(model, 16000)

    pa = pyaudio.PyAudio()
    stream = pa.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=2048, input_device_index=1)
    stream.start_stream()
    print("ready.")
    while True:
        data = stream.read(2048, exception_on_overflow=False)
        if len(data) == 0:
            break
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            recognized_text = result.get('text')
            if recognized_text:
                recognized_text = recognized_text.lower()
                print(f"Recognized: {recognized_text}")
                if "zapnout" in recognized_text:
                    switch_case('A')
                elif "řeřicha" in recognized_text:
                    switch_case('B')
                elif "left" in recognized_text:
                    switch_case('C')
                elif "right" in recognized_text:
                    switch_case('D')
                elif "switch" in recognized_text:
                    switch_case('E')
                else:
                    pass
                    #asyncio.run(artnet_menu(1))

#Main function
if __name__ == "__main__":
    recognize_speech()