#!/usr/bin/env python3
"""
 ██╗     ██╗   ██╗███╗   ███╗██╗
 ██║     ██║   ██║████╗ ████║██║
 ██║     ██║   ██║██╔████╔██║██║
 ██║     ██║   ██║██║╚██╔╝██║██║
 ███████╗╚██████╔╝██║ ╚═╝ ██║██║
 ╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝

Lumi — Local AI Assistant
Runs on Raspberry Pi 3B+ via Ollama.
"""

import sys
import time
import requests

# ── ANSI escape codes ──────────────────────────────────────────────────────────
RESET   = "\033[0m"
BOLD    = "\033[1m"
WHITE   = "\033[97m"
PURPLE  = "\033[38;2;180;50;255m"
DIM     = "\033[2m"

def truecolor(r: int, g: int, b: int) -> str:
    return f"\033[38;2;{r};{g};{b}m"

def hsv_to_rgb(h: float, s: float = 1.0, v: float = 1.0) -> tuple[int, int, int]:
    """Convert HSV (h in [0,1]) to RGB (each in [0,255])."""
    h = h % 1.0
    i = int(h * 6)
    f = h * 6 - i
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    rgb_map = [(v,t,p),(q,v,p),(p,v,t),(p,q,v),(t,p,v),(v,p,q)]
    r, g, b = rgb_map[i % 6]
    return int(r * 255), int(g * 255), int(b * 255)

# ── ASCII banner ───────────────────────────────────────────────────────────────
LUMI_ART = r"""
 ██╗     ██╗   ██╗███╗   ███╗██╗
 ██║     ██║   ██║████╗ ████║██║
 ██║     ██║   ██║██╔████╔██║██║
 ██║     ██║   ██║██║╚██╔╝██║██║
 ███████╗╚██████╔╝██║ ╚═╝ ██║██║
 ╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝
"""

SUBTITLE = "  local ai assistant  ·  v1.0  ·  type \"bye\" to exit"

def print_rainbow_banner() -> None:
    """Print ASCII art with a smooth HSV rainbow gradient."""
    char_idx = 0
    for line in LUMI_ART.split('\n'):
        for char in line:
            if char not in (' ', '\t', '\n'):
                hue = (char_idx * 0.018) % 1.0
                r, g, b = hsv_to_rgb(hue)
                sys.stdout.write(truecolor(r, g, b) + BOLD + char)
                char_idx += 1
            else:
                sys.stdout.write(char)
        sys.stdout.write('\n')
    sys.stdout.write(RESET)

    # Subtitle in dim white
    sys.stdout.write(f"{DIM}{WHITE}{SUBTITLE}{RESET}\n")
    sys.stdout.write(f"{DIM}{WHITE}{'─' * len(SUBTITLE)}{RESET}\n\n")
    sys.stdout.flush()

# ── Typewriter effect ──────────────────────────────────────────────────────────
def typewriter(text: str, delay: float = 0.016) -> None:
    """Print text one character at a time with a fast typewriter animation."""
    sys.stdout.write(PURPLE)
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write(RESET + '\n')
    sys.stdout.flush()

# ── Spinner while waiting for the model ───────────────────────────────────────
SPINNER_FRAMES = ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]

def spinner_start() -> None:
    """Print an animated spinner (blocking, runs in main thread via generator)."""
    # We poll for completion in the main loop, so this is just the first frame.
    sys.stdout.write(f"{PURPLE}{BOLD}Lumi ›{RESET} {PURPLE}⠋  pensando…{RESET}")
    sys.stdout.flush()

def spinner_update(frame_idx: int) -> None:
    frame = SPINNER_FRAMES[frame_idx % len(SPINNER_FRAMES)]
    sys.stdout.write(f"\r{PURPLE}{BOLD}Lumi ›{RESET} {PURPLE}{frame}  pensando…{RESET}")
    sys.stdout.flush()

def spinner_clear() -> None:
    sys.stdout.write(f"\r{' ' * 30}\r")
    sys.stdout.flush()

# ── Ollama API ─────────────────────────────────────────────────────────────────
OLLAMA_URL    = "http://localhost:11434/api/chat"
DEFAULT_MODEL = "tinyllama"          # best for RPi 3B+ (low RAM); try "phi3" on Pi 4+

SYSTEM_PROMPT = (
    "Sei Lumi, un assistente AI amichevole, intelligente e conciso. "
    "Rispondi sempre in italiano a meno che l'utente non usi un'altra lingua. "
    "Sii utile, diretto e preciso. Non usare markdown eccessivo nel terminale."
)

def ask_ollama(history: list[dict]) -> str:
    """Send conversation history to Ollama and return the assistant reply."""
    payload = {
        "model": DEFAULT_MODEL,
        "messages": [{"role": "system", "content": SYSTEM_PROMPT}] + history,
        "stream": False,
        "options": {
            "num_predict": 512,
            "temperature": 0.7,
        },
    }
    try:
        resp = requests.post(OLLAMA_URL, json=payload, timeout=300)
        resp.raise_for_status()
        return resp.json()["message"]["content"].strip()

    except requests.exceptions.ConnectionError:
        return (
            "⚠️  Non riesco a raggiungere Ollama. "
            "Avvialo prima con:  ollama serve"
        )
    except requests.exceptions.Timeout:
        return (
            "⚠️  Timeout: il modello sta impiegando troppo tempo. "
            "Prova un modello più leggero come tinyllama."
        )
    except Exception as exc:
        return f"⚠️  Errore imprevisto: {exc}"

# ── Main loop ──────────────────────────────────────────────────────────────────
def main() -> None:
    print_rainbow_banner()

    history: list[dict] = []
    greeting = "Ciao, sono Lumi, come posso aiutarti oggi?"

    sys.stdout.write(f"{PURPLE}{BOLD}Lumi ›{RESET} ")
    sys.stdout.flush()
    typewriter(greeting)
    print()

    while True:
        # ── Prompt utente ──
        try:
            sys.stdout.write(f"{WHITE}{BOLD}Tu   ›{RESET} {WHITE}")
            sys.stdout.flush()
            user_input = input()
            sys.stdout.write(RESET)
        except (EOFError, KeyboardInterrupt):
            user_input = "bye"

        user_input_stripped = user_input.strip()

        if not user_input_stripped:
            continue

        if user_input_stripped.lower() == "bye":
            print()
            sys.stdout.write(f"{PURPLE}{BOLD}Lumi ›{RESET} ")
            sys.stdout.flush()
            typewriter("A presto! Torna quando vuoi. 👋")
            print()
            sys.exit(0)

        # ── Chiedi al modello ──
        history.append({"role": "user", "content": user_input_stripped})

        print()
        spinner_start()

        # Spinner animation while polling (simple blocking with sleep)
        import threading

        result_container: dict = {}
        done_event = threading.Event()

        def fetch():
            result_container["reply"] = ask_ollama(history)
            done_event.set()

        thread = threading.Thread(target=fetch, daemon=True)
        thread.start()

        frame = 0
        while not done_event.is_set():
            spinner_update(frame)
            frame += 1
            time.sleep(0.1)

        spinner_clear()

        reply = result_container.get("reply", "⚠️  Nessuna risposta ricevuta.")
        history.append({"role": "assistant", "content": reply})

        sys.stdout.write(f"{PURPLE}{BOLD}Lumi ›{RESET} ")
        sys.stdout.flush()
        typewriter(reply)
        print()


if __name__ == "__main__":
    main()
