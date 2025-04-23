from multiprocessing import Process
from pydub import AudioSegment
from pydub.playback import _play_with_pyaudio
from transcription_service import transcribe_audio
from llm_service import chatbot_service
import time
import logging


def play_audio_segment(audio_path, stop_event):
    audio = AudioSegment.from_file(audio_path)
    _play_with_pyaudio(audio)


def transcribe_to_response_audio_file(response_audio):
    transcription = transcribe_audio("user_input.wav")
    logging.info("[Responder] Starting audio playback")
    chatbot_service(transcription)


def responder_process(
    conversation_started, conversation_ended, user_speaking, bot_responding, stop_audio
):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter(f"%(asctime)s -responder - %(levelname)s - %(message)s")
    )
    logger.addHandler(handler)

    logging.info("[Responder] Process started.")
    while not conversation_ended.is_set():
        if not conversation_started.is_set():
            continue
        if user_speaking.is_set():
            logging.info("[Responder] Waiting for user to finish...")
            continue
        if bot_responding.is_set():
            start_time = time.time()
            logging.info("[Responder] User is not speaking")
            # convert user_input.wav to text using AWS Transcribe or any other method
            response_audio = ".\\response.mp3"
            transcribe_to_response_audio_file(response_audio)
            play_audio_segment(response_audio, stop_audio)
            # p = Process(target=play_audio_segment, args=(response_audio, stop_audio))
            # p.start()

            # Wait for the audio to finish or get interrupted
            # while p.is_alive():
            #     if stop_audio.is_set():
            #         p.terminate()
            #         logging.info("[Responder] Playback terminated due to user speech")
            #         stop_audio.clear()  # Clear the stop signal
            #         break
            #     time.sleep(0.1)
            total_time = time.time() - start_time
            total_time_seconds = int(total_time)
            logger.info(
                f"[Responder] Total time taken for response: {total_time_seconds} seconds"
            )
            bot_responding.clear()


def main():

    response_audio = ".\\response.mp3"
    transcription = transcribe_audio("user_input.wav")
    logging.info("[Responder] Starting audio playback")
    chat_response = chatbot_service(transcription)
    logging.info("[Responder] Starting audio playback")
    generate_speech(response_audio, chat_response)
    audio = AudioSegment.from_file(response_audio)

    _play_with_pyaudio(audio)


if __name__ == "__main__":
    main()
