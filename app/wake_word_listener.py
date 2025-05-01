import os
import pvporcupine
import pyaudio
import struct
from dotenv import load_dotenv
from app.conversation_starter import start_conversation
from app.logger import logger

load_dotenv()

def listen_for_wake_word():
    access_key = os.getenv("PORCUPINE_ACCESS_KEY")

    if not access_key:
        logger.error("PORCUPINE_ACCESS_KEY must be set in .env file.")
        raise ValueError("PORCUPINE_ACCESS_KEY must be set in .env file.")

    try:
        porcupine = pvporcupine.create(
            access_key=access_key,
            keywords=["jarvis"]
        )
        logger.info("Successfully initialized Porcupine wake word detector")
    except Exception as e:
        logger.error(f"Failed to initialize Porcupine: {str(e)}")
        raise

    pa = pyaudio.PyAudio()
    stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length
    )

    logger.info("Listening for wake word...")

    try:
        while True:
            pcm = stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
            keyword_index = porcupine.process(pcm)
            if keyword_index >= 0:
                logger.info("Wake word detected!")
                start_conversation()
    except Exception as e:
        logger.error(f"Error in wake word detection: {str(e)}")
        raise
    finally:
        logger.info("Shutting down wake word listener...")
        stream.stop_stream()
        stream.close()
        pa.terminate()
        porcupine.delete()
        logger.info("Wake word listener shutdown complete")
