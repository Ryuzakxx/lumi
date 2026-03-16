<div align="center">

```
 ██╗     ██╗   ██╗███╗   ███╗██╗
 ██║     ██║   ██║████╗ ████║██║
 ██║     ██║   ██║██╔████╔██║██║
 ██║     ██║   ██║██║╚██╔╝██║██║
 ███████╗╚██████╔╝██║ ╚═╝ ██║██║
 ╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝
```

**Local AI assistant for Raspberry Pi — powered by Ollama**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python)
![Ollama](https://img.shields.io/badge/Ollama-local%20LLM-black?style=flat-square)
![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-3B%2B-C51A4A?style=flat-square&logo=raspberrypi)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

</div>

---

## What is Lumi?

**Lumi** is a lightweight, fully local AI chatbot designed to run directly on a **Raspberry Pi 3B+** (and above) from a terminal. No internet connection required, no cloud APIs, no subscription — just you, your Pi, and a local language model.

Lumi uses [Ollama](https://ollama.com) under the hood to serve the LLM locally, and communicates with it via its REST API.

---

## Features

| Feature | Description |
|---|---|
| 🌈 **Rainbow ASCII banner** | Kali Linux-style RGB gradient title on startup |
| ⌨️ **Typewriter animation** | Fast typewriter effect for all bot responses |
| 🟣 **Color-coded chat** | Lumi messages in purple, user messages in white |
| ⠙ **Thinking spinner** | Animated spinner while the model is generating |
| 💬 **Conversation memory** | Full chat history is sent on every turn |
| 🔒 **100% local** | No data leaves your device |
| 🥧 **Raspberry Pi optimized** | Lightweight stack, minimal dependencies |

---

## Requirements

- Raspberry Pi 3B+ (or any machine running Linux/macOS/Windows)
- Python **3.10+**
- [Ollama](https://ollama.com) installed and running
- A compatible model pulled (e.g. `tinyllama`, `phi3`, `llama3.2:1b`)

---

## Installation

### 1 — Install Ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### 2 — Pull a lightweight model

For Raspberry Pi 3B+ (1 GB RAM) it is strongly recommended to use `tinyllama`:

```bash
ollama pull tinyllama
```

For more powerful hardware (Pi 4 / Pi 5 / PC):

```bash
ollama pull phi3        # ~2.3 GB — great quality/speed balance
ollama pull llama3.2:1b # ~1.3 GB — Meta's 1B parameter model
```

### 3 — Clone this repository

```bash
git clone https://github.com/YOUR_USERNAME/lumi.git
cd lumi
```

### 4 — Install Python dependencies

```bash
pip install -r requirements.txt
```

---

## Usage

Make sure Ollama is running:

```bash
ollama serve
```

Then launch Lumi in a new terminal:

```bash
python3 lumi.py
```

Type your message and press **Enter** to chat. To exit, type:

```
bye
```

---

## Configuration

At the top of `lumi.py` you can tweak a few constants:

```python
OLLAMA_URL    = "http://localhost:11434/api/chat"  # Ollama endpoint
DEFAULT_MODEL = "tinyllama"                         # Model to use
```

```python
SYSTEM_PROMPT = "..."  # Lumi's personality and instructions
```

```python
# In typewriter():
delay: float = 0.016   # Seconds per character — lower = faster
```

---

## Recommended models by hardware

| Hardware | RAM | Recommended model |
|---|---|---|
| Raspberry Pi 3B+ | 1 GB | `tinyllama` |
| Raspberry Pi 4 | 4/8 GB | `phi3`, `llama3.2:1b` |
| Raspberry Pi 5 | 8 GB | `llama3.2:3b`, `mistral` |
| Desktop / Laptop | 16 GB+ | `llama3`, `mixtral` |

---

## Project structure

```
lumi/
├── lumi.py           # Main bot script
├── requirements.txt  # Python dependencies
└── README.md         # This file
```

---

## Roadmap

- [x] Terminal chat with typewriter animation
- [x] Full conversation memory within session
- [x] Animated spinner while model is thinking
- [x] Color-coded UI (rainbow banner, purple bot, white user)
- [ ] **Voice input** — speech-to-text via `whisper.cpp` or `vosk` (offline, Pi-friendly)
- [ ] **Voice output** — text-to-speech via `piper-tts` (fast, runs locally on Pi)
- [ ] Wake-word detection (e.g. "Hey Lumi")
- [ ] Persistent conversation history (saved to disk across sessions)
- [ ] Plugin / tool system (weather, reminders, file search…)
- [ ] Web UI companion (Flask or FastAPI frontend)

---

## License

MIT — do whatever you want with it.

---

<div align="center">
Made with ❤️ and way too many terminal colors.
</div>
