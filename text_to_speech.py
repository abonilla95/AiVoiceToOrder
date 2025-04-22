import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from a .env file
load_dotenv()

# Retrieve the API key from the environment variables
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    client = OpenAI(
        api_key=api_key,
    )
else:
    raise ValueError("OPENAI_API_KEY not found in environment variables.")


def text_to_speech(text: str) -> str:
        
    with client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="coral",
        input=text,
        instructions="Speak in a cheerful and positive tone.",
    ) as response:
        response.stream_to_file("response.mp3")