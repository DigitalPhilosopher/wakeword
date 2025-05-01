import os
import pvporcupine
import pyaudio
import struct
from dotenv import load_dotenv
from app.conversation_starter import start_conversation

load_dotenv()

def listen_for_wake_word():
    access_key = os.getenv("PORCUPINE_ACCESS_KEY")

    if not access_key:
        raise ValueError("PORCUPINE_ACCESS_KEY must be set in .env file.")

    porcupine = pvporcupine.create(
        access_key=access_key,
        keywords=["jarvis"]
    )

    pa = pyaudio.PyAudio()
    stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length
    )

    print("Listening for wake word...")

    try:
        while True:
            pcm = stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
            keyword_index = porcupine.process(pcm)
            if keyword_index >= 0:
                start_conversation()
    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()
        porcupine.delete()
