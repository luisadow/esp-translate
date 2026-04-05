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
esp-translate/
├── platformio.ini   # ESP32 PlatformIO project config
├── src/             # Firmware source
├── include/         # Firmware headers
├── lib/             # Local libraries
├── test/            # Firmware tests
├── backend/         # Backend scaffold (noch nicht implementiert)
│   ├── app/
│   └── requirements.txt
├── tools/           # Serial/Debug-Helfer
│   ├── read_serial.py
│   └── udev/
│       └── 99-esp32-1.rules
├── docs/            # Dokumentation, Kontext
│   └── context.md
└── README.md
```
