import pyttsx3


def available_voices():
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty("voices") or []
        result = []
        for voice in voices:
            result.append({
                "id": voice.id,
                "name": voice.name,
                "languages": " ".join(str(x) for x in (getattr(voice, "languages", []) or [])),
            })
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
                v for v in voices
                if "urdu" in (str(v.name) + " " + str(v.id) + " " +
                              " ".join(str(x) for x in (getattr(v, "languages", []) or []))).lower()
            ]
            if not matches:
                engine.stop()
                return False, "Windows mein Urdu text-to-speech voice installed nahi hai."
            engine.setProperty("voice", matches[0].id)
        else:
            english = [v for v in voices if "english" in
                       (str(v.name) + " " + str(v.id) + " " +
                        " ".join(str(x) for x in (getattr(v, "languages", []) or []))).lower()]
            if english:
                engine.setProperty("voice", english[0].id)
        engine.setProperty("rate", 175)
        engine.say(text)
        engine.runAndWait()
        engine.stop()
        return True, "Speech complete."
    except Exception as exc:
        return False, f"Speech error: {exc}"
