#include <Arduino.h>
#include <cstdarg>
#include <cstdio>

namespace {
constexpr uint32_t kStatusIntervalMs = 5000;
uint32_t lastStatusAt = 0;

void beginLogPorts() {
  Serial.begin(115200);
#if ARDUINO_USB_MODE && !ARDUINO_USB_CDC_ON_BOOT
  USBSerial.begin(115200);
#endif
}

bool isPrimaryLogPortReady() {
#if ARDUINO_USB_MODE && !ARDUINO_USB_CDC_ON_BOOT
  return static_cast<bool>(USBSerial);
#else
  return static_cast<bool>(Serial);
#endif
}

void logLine(const char* text) {
  Serial.print(text);
#if ARDUINO_USB_MODE && !ARDUINO_USB_CDC_ON_BOOT
  USBSerial.print(text);
#endif
}

void logf(const char* fmt, ...) {
  char buffer[192];
  va_list args;
  va_start(args, fmt);
  vsnprintf(buffer, sizeof(buffer), fmt, args);
  va_end(args);
  logLine(buffer);
}

void logBootDiagnostics() {
  const uint32_t flashBytes = ESP.getFlashChipSize();
  const uint32_t psramBytes = ESP.getPsramSize();
  const uint32_t freePsramBytes = ESP.getFreePsram();

  logf("BOOT Flash detected: %u MB\n", flashBytes / (1024U * 1024U));
  logf(
      "BOOT PSRAM detected: %u MB, free: %u KB\n",
      psramBytes / (1024U * 1024U),
      freePsramBytes / 1024U);

  if (flashBytes < (16U * 1024U * 1024U)) {
    logf("ERR Flash size below expected 16MB (%u bytes)\n", flashBytes);
  }
  if (psramBytes < (8U * 1024U * 1024U)) {
    logf("ERR PSRAM size below expected 8MB (%u bytes)\n", psramBytes);
  }
}
}  // namespace

void setup() {
  beginLogPorts();

  const uint32_t waitStart = millis();
  while (!isPrimaryLogPortReady() && (millis() - waitStart) < 1500U) {
    // Wait briefly for USB CDC so early BOOT logs are visible.
  }

  logLine("BOOT Firmware bring-up start\n");

  if (psramFound()) {
    logLine("BOOT PSRAM init OK\n");
  } else {
    logLine("ERR PSRAM init failed\n");
  }

  logBootDiagnostics();
  lastStatusAt = millis();
}

void loop() {
  const uint32_t now = millis();
  if (now - lastStatusAt >= kStatusIntervalMs) {
    lastStatusAt = now;
    logf(
        "BOOT Alive t=%lu ms free_heap=%uKB free_psram=%uKB\n",
        static_cast<unsigned long>(now),
        ESP.getFreeHeap() / 1024U,
        ESP.getFreePsram() / 1024U);
  }

  delay(1);
}
