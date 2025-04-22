import time
startup_time = time.time()
import logging
from multiprocessing import Process, Event
from listener import listener_process
from bot_responder import responder_process

def setup_logging(process_name):
    logging.basicConfig(
        level=logging.INFO,
        format=f'%(asctime)s - {process_name} - %(levelname)s - %(message)s'
    )

def main():
    conversation_started = Event()
    conversation_ended = Event()
    user_speaking = Event()
    bot_responding = Event()
    stop_audio = Event()
    end_startup_time = time.time()
    startup_duration = end_startup_time - startup_time
    print(f"Startup time: {startup_duration:.2f} seconds")
    print("Starting main process...")
    listener = Process(target=listener_process, args=(conversation_started, conversation_ended, user_speaking, bot_responding, stop_audio))

    responder = Process(target=responder_process, args=(conversation_started, conversation_ended, user_speaking, bot_responding, stop_audio))

    listener.start()
    responder.start()

    listener.join()
    responder.join()


if __name__ == "__main__":
    main()
