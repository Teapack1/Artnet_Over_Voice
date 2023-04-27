#Test file to check if the microphone is working
import pyaudio

pa = pyaudio.PyAudio()
for i in range(pa.get_device_count()):
    device_info = pa.get_device_info_by_index(i)
    if device_info["maxInputChannels"] > 0:
        print(f"Input Device index {i} - {device_info['name']}")
