# 🗣️ Jarvis Voice Assistant for Raspberry Pi

This project is a **hands-free voice assistant** built for Raspberry Pi using:

- 🔊 [ElevenLabs](https://www.elevenlabs.io/) for conversational AI
- 🐗 [Picovoice Porcupine](https://picovoice.ai/products/porcupine/) for offline wake word detection ("Jarvis")
- 🎙️ `PyAudio` for microphone and speaker I/O
- 📡 `.env` for secure API key management

---

## 🧠 What it does

1. Listens continuously for the wake word: **"Jarvis"**
2. When detected, starts a **live voice conversation** using ElevenLabs
3. Prevents feedback by muting the mic during playback

---

## 📁 Project Structure

```
my_voice_assistant/
│
├── app/
│   ├── fixed_audio_interface.py      # Audio interface with mic/speaker separation
│   ├── conversation_starter.py       # Starts ElevenLabs voice session
│   └── wake_word_listener.py         # Listens for wake word using Porcupine
│
├── main.py                           # Entry point
├── .env                              # Stores API keys (never commit this!)
├── requirements.txt                  # Python dependencies
└── README.md                         # You're here
```

---

## 🚀 Getting Started

### ✅ Requirements

- Raspberry Pi (or any Linux box)
- Python 3.7+
- Microphone + speaker
- [Create an ElevenLabs account](https://www.elevenlabs.io/)
- [Create a Picovoice account](https://console.picovoice.ai/) and get your Porcupine Access Key

---

### 🛠️ Installation

1. Clone this repo:

```bash
git clone https://github.com/YOUR_USERNAME/my_voice_assistant.git
cd my_voice_assistant
```

2. Create `.env` file:

```env
ELEVENLABS_API_KEY=your-elevenlabs-api-key
ELEVENLABS_AGENT_ID=your-elevenlabs-agent-id
PORCUPINE_ACCESS_KEY=your-porcupine-access-key
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run it:

```bash
python3 main.py
```

Now it will listen for **"Jarvis"**, and launch the voice assistant when triggered.

---

## 📦 Python Dependencies

```text
elevenlabs
pvporcupine
pyaudio
python-dotenv
```

---

## 🔒 Security Notes

- Your API keys are stored in `.env`. **Never commit this file.**
- Add `.env` to `.gitignore`.

---

## 🧠 Future Ideas

- Add LED feedback (e.g., green when listening, red when speaking)
- Automatically stop sessions after timeout
- Run as systemd service on boot
- Add custom commands for smart home, reminders, etc.

---

## 📄 License

MIT License – free to use and adapt.

---

## ❤️ Credits

- [ElevenLabs](https://www.elevenlabs.io/)
- [Picovoice Porcupine](https://picovoice.ai/)
