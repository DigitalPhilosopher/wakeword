import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs.conversational_ai.conversation import Conversation
from app.fixed_audio_interface import FixedAudioInterface
from app.logger import logger

load_dotenv()

def start_conversation():
    agent_id = os.getenv("ELEVENLABS_AGENT_ID")
    api_key = os.getenv("ELEVENLABS_API_KEY")

    if not agent_id or not api_key:
        logger.error("ELEVENLABS_AGENT_ID and ELEVENLABS_API_KEY must be set in .env file.")
        raise ValueError("ELEVENLABS_AGENT_ID and ELEVENLABS_API_KEY must be set in .env file.")

    try:
        client = ElevenLabs(api_key=api_key)
        logger.info("Successfully initialized ElevenLabs client")

        conversation = Conversation(
            client,
            agent_id,
            requires_auth=bool(api_key),
            audio_interface=FixedAudioInterface(),
            callback_agent_response=lambda response: logger.info(f"Agent: {response}"),
            callback_agent_response_correction=lambda original, corrected: logger.info(f"Agent: {original} -> {corrected}"),
            callback_user_transcript=lambda transcript: logger.info(f"User: {transcript}"),
        )

        logger.info("Starting conversation session...")
        conversation.start_session()
        logger.info("Conversation session ended")
    except Exception as e:
        logger.error(f"Error in conversation: {str(e)}")
        raise
