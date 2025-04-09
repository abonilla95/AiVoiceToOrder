from multiprocessing import Process, Event
from pydub import AudioSegment
from pydub.playback import _play_with_pyaudio
import time
import boto3

polly = boto3.client("polly")


def play_audio_segment(audio_path, stop_event):
    audio = AudioSegment.from_file(audio_path)

    player = _play_with_pyaudio(audio)

    # Monitor stop_event in real time
    while player.is_playing():
        if stop_event.is_set():
            print("[Audio] Stop signal received")
            player.stop()
            break
        time.sleep(0.1)  # Check frequently


def responder_process(user_speaking, stop_audio):
    while True:
        if user_speaking.is_set():
            print("[Responder] Waiting for user to finish...")
            time.sleep(0.5)
            continue

        print("[Responder] Starting audio playback")
        p = Process(target=play_audio_segment, args=("response.mp3", stop_audio))
        p.start()

        # Wait for the audio to finish or get interrupted
        while p.is_alive():
            if stop_audio.is_set():
                p.terminate()
                print("[Responder] Playback terminated due to user speech")
                break
            time.sleep(0.1)

        time.sleep(1)


# Convert text to speech using Amazon Polly
def text_to_speech(text, output_filename):
    response = polly.synthesize_speech(Text=text, OutputFormat="mp3", VoiceId="Joanna")
    with open(output_filename, "wb") as file:
        file.write(response["AudioStream"].read())


def listener_process(user_speaking, stop_audio):
    while True:
        input("[Listener] Press Enter to simulate user speaking\n")
        user_speaking.set()
        stop_audio.set()  # Signal to interrupt any audio
        print("[Listener] User speaking...")
        time.sleep(3)  # Simulate user talking
        user_speaking.clear()
        print("[Listener] User stopped speaking")


def main():
    user_speaking = Event()
    stop_audio = Event()

    listener = Process(target=listener_process, args=(user_speaking, stop_audio))
    responder = Process(target=responder_process, args=(user_speaking, stop_audio))

    listener.start()
    responder.start()

    listener.join()
    responder.join()


if __name__ == "__main__":
    main()
