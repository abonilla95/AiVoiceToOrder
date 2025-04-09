import time
import wave
import pyaudio
import numpy as np
import noisereduce as nr
import speech_recognition as sr

def listener_process(user_speaking, stop_audio):
    while True:
        input("[Listener] Press Enter to simulate user speaking\n")
        user_speaking.set()
        stop_audio.set()  # Signal to interrupt any audio
        print("[Listener] User speaking...")
        time.sleep(3)  # Simulate user talking
        user_speaking.clear()
        print("[Listener] User stopped speaking")

# Record audio using PyAudio
def record_audio(filename):
    audio_format = pyaudio.paInt16
    channels = 1
    rate = 16000
    chunk = 1024
    silence_threshold = 500  # Adjust this value based on your microphone sensitivity
    silence_duration = 5  # Duration of silence in seconds to stop recording
    conversation_duration = 2
    audio = pyaudio.PyAudio()
    stream = audio.open(format=audio_format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)

    print("Recording...")
    frames = []
    silent_chunks = 0
    conversation_chunks = int(rate / chunk * conversation_duration)
    max_silent_chunks = int(rate / chunk * silence_duration)

    while True:
        data = stream.read(chunk)
        frames.append(data)

        # Convert audio data to numpy array for noise reduction
        audio_array = np.frombuffer(data, dtype=np.int16)
        reduced_noise = nr.reduce_noise(y=audio_array, sr=rate)

        # Check if the audio level is below the silence threshold
        audio_level = max(abs(reduced_noise))
        if audio_level < silence_threshold:
            silent_chunks += 1
        else:
            silent_chunks = 0

        # Stop recording if silence is detected for the specified duration
        if silent_chunks > conversation_chunks and silent_chunks < max_silent_chunks:
            print("Conversation pause detected, writing chunk of recording.")
            break
        else:
            print("Silence detected, stopping recording.")
            break
    stream.stop_stream()
    stream.close()
    audio.terminate()

    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(audio.get_sample_size(audio_format))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()

