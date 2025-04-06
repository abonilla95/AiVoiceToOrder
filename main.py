import time
import requests
import pyaudio
import wave
import boto3
import noisereduce as nr
import numpy as np
import speech_recognition as sr

# AWS clients
transcribe = boto3.client('transcribe')
polly = boto3.client('polly')

# Record audio using PyAudio
def record_audio(filename):
    audio_format = pyaudio.paInt16
    channels = 1
    rate = 16000
    chunk = 1024
    silence_threshold = 500  # Adjust this value based on your microphone sensitivity
    silence_duration = 2  # Duration of silence in seconds to stop recording

    audio = pyaudio.PyAudio()
    stream = audio.open(format=audio_format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)

    print("Recording...")
    frames = []
    silent_chunks = 0
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
        if silent_chunks > max_silent_chunks:
            print("Silence detected, stopping recording.")
            break

    print("Recording finished.")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(audio.get_sample_size(audio_format))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()

# Transcribe audio using Amazon Transcribe
def transcribe_audio(file_uri):
    job_name = "TranscriptionJob" + str(int(time.time()))
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': file_uri},
        MediaFormat='wav',
        LanguageCode='en-US'
    )

    # Wait for the job to complete
    while True:
        status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break
        print("Waiting for transcription to complete...")
        time.sleep(5)

    if status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
        transcript_file_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
        response = requests.get(transcript_file_uri)
        return response.json()['results']['transcripts'][0]['transcript']
    else:
        raise Exception("Transcription failed.")

# Send text to AI model and get response (Assuming a simple mock AI response)
def get_ai_response(text):
    # Mock response for illustration
    return "This is the AI response to your input: " + text

# Convert text to speech using Amazon Polly
def text_to_speech(text, output_filename):
    response = polly.synthesize_speech(Text=text, OutputFormat='mp3', VoiceId='Joanna')
    with open(output_filename, 'wb') as file:
        file.write(response['AudioStream'].read())

# Play the generated audio file
def play_audio(filename):
    chunk = 1024
    wf = wave.open(filename, 'rb')
    audio = pyaudio.PyAudio()

    # Open a stream to play the audio
    stream = audio.open(format=audio.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

    # Read and play the audio in chunks
    data = wf.readframes(chunk)
    while data:
        stream.write(data)
        data = wf.readframes(chunk)

    # Close the stream
    stream.stop_stream()
    stream.close()
    audio.terminate()

if __name__ == "__main__":
    # Step 1: Record audio
    audio_filename = "input_audio.wav"
    record_audio(audio_filename)

    # # Step 2: Transcribe audio
    # # Upload the audio file to an S3 bucket first
    # # Assuming the audio file is already in S3
    # s3_bucket_uri = 's3://your-bucket-name/input_audio.wav'
    # transcript = transcribe_audio(s3_bucket_uri)

    # # Step 3: Get AI model response
    # ai_response = get_ai_response(transcript)

    # # Step 4: Convert AI response to speech
    # output_audio_filename = "ai_response.mp3"
    # text_to_speech(ai_response, output_audio_filename)

    # print(f"AI response audio saved to {output_audio_filename}")
    # Step 5: Play the audio response
    # play_audio(output_audio_filename)
    # print("Playing AI response audio...")
