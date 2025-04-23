import time
import wave
import logging
import pyaudio
import numpy as np
import noisereduce as nr
import speech_recognition as sr


def listener_process(
    conversation_started, conversation_ended, user_speaking, bot_responding, stop_audio
):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter(f"%(asctime)s -listener - %(levelname)s - %(message)s")
    )
    logger.addHandler(handler)

    logging.info("Listener process started.")
    while not conversation_ended.is_set():
        user_speaking.set()
        stop_audio.set()  # Signal to interrupt any audio
        logging.info("[Listener] User speaking...")
        record_audio(
            conversation_started,
            conversation_ended,
            user_speaking,
            bot_responding,
            stop_audio,
        )
        user_speaking.clear()
        logging.info("[Listener] User stopped speaking")


def record_audio(
    conversation_started, conversation_ended, user_speaking, bot_responding, stop_audio
):
    audio_format = pyaudio.paInt16
    channels = 1
    rate = 16000
    chunk = 1024
    silence_threshold = 500  # Adjust this value based on your microphone sensitivity
    silence_duration = 10  # Duration of silence in seconds to stop recording
    conversation_duration = (
        1.5  # Duration of conversation in seconds to consider as a pause
    )
    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=audio_format,
        channels=channels,
        rate=rate,
        input=True,
        frames_per_buffer=chunk,
    )

    logging.info("Recording...")
    frames = []
    silent_chunks = 0
    conversation_chunks = int(rate / chunk * conversation_duration)
    max_silent_chunks = int(rate / chunk * silence_duration)
    file_count = 0
    started_talking = False
    all_frames = []

    while True:
        data = stream.read(chunk)
        frames.append(data)
        all_frames.append(data)

        # Convert audio data to numpy array for noise reduction
        audio_array = np.frombuffer(data, dtype=np.int16)
        reduced_noise = nr.reduce_noise(y=audio_array, sr=rate)

        # Check if the audio level is below the silence threshold
        audio_level = max(abs(reduced_noise))
        if audio_level < silence_threshold:
            silent_chunks += 1
        else:
            if not conversation_started.is_set():
                conversation_started.set()
            started_talking = True
            silent_chunks = 0

        if not conversation_started.is_set():
            logging.info("[Listener] Waiting for conversation to start...")
            continue
        else:

            # Stop recording if silence exceeds the maximum duration
            if silent_chunks >= max_silent_chunks:
                logging.info(
                    "[Listener] Maximum silence duration reached, stopping recording."
                )
                conversation_ended.set()
                break
            if started_talking:

                if not stop_audio.is_set():
                    stop_audio.set()
            if conversation_started.is_set() and not started_talking:
                logging.info("[Listener] Waiting for user to start speaking again...")
                continue

            # Save audio chunk if silence is detected for the specified duration
            if (
                started_talking
                and silent_chunks > conversation_chunks
                and silent_chunks < max_silent_chunks
            ):
                logging.info("[Listener] Conversation pause detected.")
                if user_speaking.is_set():
                    logging.info("[Listener] Saving chunk of recording.")
                    file_count += 1
                    save_audio_chunk(
                        frames, f"user_input.wav", audio, audio_format, channels, rate
                    )
                    user_speaking.clear()
                    logging.info("[Listener] Waiting for responder to finish...")
                    frames = []  # Reset frames for the next chunk
                    started_talking = False
                    bot_responding.set()  # Signal to the responder that the user has finished speaking
                    while bot_responding.is_set():
                        logging.info("[Listener] Waiting for responder to finish...")
                        time.sleep(0.1)
                    user_speaking.set()
                    started_talking = False
                    silent_chunks = 0

    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save any remaining audio frames
    if all_frames:
        file_count += 1
        save_audio_chunk(
            all_frames, f"user_conversation.wav", audio, audio_format, channels, rate
        )


def save_audio_chunk(frames, filename, audio, audio_format, channels, rate):
    wf = wave.open(filename, "wb")
    wf.setnchannels(channels)
    wf.setsampwidth(audio.get_sample_size(audio_format))
    wf.setframerate(rate)
    wf.writeframes(b"".join(frames))
    wf.close()
    logging.info(f"Saved: {filename}")
