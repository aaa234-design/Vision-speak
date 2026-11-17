import pyttsx3


def _voice_text(voice):
    parts = [str(getattr(voice, "name", "")), str(getattr(voice, "id", ""))]
    for language in (getattr(voice, "languages", []) or []):
        if isinstance(language, bytes):
            language = language.decode("utf-8", errors="ignore")
        parts.append(str(language))
    return " ".join(parts).lower()


def available_voices():
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty("voices") or []
        result = [
            {"id": voice.id, "name": voice.name, "languages": _voice_text(voice)}
            for voice in voices
        ]
        engine.stop()
        return result
    except Exception:
        return []


def speak(text, language="English"):
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty("voices") or []
        if language.lower() == "urdu":
            matches = [
                voice for voice in voices
                if any(tag in _voice_text(voice) for tag in ("urdu", "ur-pk", "ur_pk", "ur"))
            ]
            if not matches:
                engine.stop()
                return False, (
                    "Windows mein Urdu TTS voice nahi mili. Settings > Time & language > "
                    "Language & region mein Urdu speech voice install karein, phir app restart karein."
                )
            engine.setProperty("voice", matches[0].id)
        else:
            english = [
                voice for voice in voices
                if any(tag in _voice_text(voice) for tag in ("english", "en-us", "en-gb", "en_"))
            ]
            if english:
                engine.setProperty("voice", english[0].id)

        engine.setProperty("rate", 175)
        engine.say(str(text))
        engine.runAndWait()
        engine.stop()
        return True, "Speech complete."
    except Exception as exc:
        return False, f"Speech error: {exc}"
