# Voice Translator Project Context

## 1. Projektübersicht
**Ziel:** Entwicklung eines Voice-Agents / Übersetzungsgeräts auf ESP32-S3 + Backend.  
**Funktionen:**
- Echtzeit-Spracherkennung (Whisper / später eigene APIs)
- Live-Übersetzung auf Display (Original + Zielsprache)
- Wiederholungsfunktion für Konversation (TTS)
- Self-Hosting der Modelle geplant, aktuell Cloud-APIs

---

## 2. Hardware Setup
**ESP32-S3**  
- I2S Mikrofon
- MAX98357 Amplifier
- 3W 4Ω Lautsprecher
- 1602A LCD Display (später OLED mit custom GUI)
- Firmware via PlatformIO (Arduino Framework)

**Server / Dev-Umgebung**
- Ubuntu Home-Server (SSH + Docker)
- VS Code Remote SSH
- MacBook als Interface / Copilot Client
- GitHub Student Developer Pack verfügbar

---

## 3. Repo-Struktur

```text
voice-translator/
├── firmware/        # ESP32 PlatformIO Firmware
│   ├── src/
│   └── include/
├── backend/         # FastAPI / Docker / Python scripts
│   ├── app/
│   └── requirements.txt
├── tools/           # Scripts für Audio, Serial, Debug
│   ├── capture_audio.py
│   └── read_serial.py
├── docs/            # Dokumentation, Kontext
│   └── context.md
└── README.md
