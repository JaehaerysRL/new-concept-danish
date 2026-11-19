"""Shared TTS helpers: Gemini TTS on Vertex AI, content-hash cache, ffmpeg encoding.

Credentials come from GOOGLE_APPLICATION_CREDENTIALS (service-account JSON kept outside the repo).
Every synthesis is cached under audio/cache/<sha256>.wav, keyed by (model, voice, style, text),
so re-running only pays for sentences that actually changed.
"""

from __future__ import annotations

import hashlib
import os
import subprocess
import threading
import time
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AUDIO = ROOT / "audio"
CACHE = AUDIO / "cache"
OUT = ROOT / "dist" / "practice" / "audio"      # served next to index.html; committed

DEFAULT_MODEL = "gemini-3.8-flash-tts"
LOCATION = os.environ.get("NCD_GCP_LOCATION", "global")
# Plain text only: gemini-3.8-flash-tts reads any inline instruction aloud ("Læs følgende … højt") and
# rejects system_instruction (400), so style prompting is off. Kept as a parameter for models that honour it.
STYLE = ""
RATE = 24000

_client = None
_client_lock = threading.Lock()


def client():
    """One shared client; the lock stops worker threads from each building (and dropping) their own."""
    global _client
    with _client_lock:
        if _client is None:
            import google.auth
            from google import genai
            _, project = google.auth.default()
            from google.genai import types
            _client = genai.Client(vertexai=True, project=os.environ.get("NCD_GCP_PROJECT", project), location=LOCATION,
                                   http_options=types.HttpOptions(timeout=120_000))  # ms; a hung call must not stall a batch
    return _client


def cache_key(text: str, voice: str, model: str = DEFAULT_MODEL, style: str = STYLE) -> str:
    return hashlib.sha256("\x1f".join((model, voice, style, text)).encode("utf-8")).hexdigest()


def _write_wav(path: Path, data: bytes) -> None:
    if data[:4] == b"RIFF":               # some models already return a complete WAV file
        path.write_bytes(data)
        return
    with wave.open(str(path), "wb") as w:  # others return raw 16-bit mono PCM
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(data)


TRANSIENT = ("429", "500", "503", "504", "RESOURCE_EXHAUSTED", "UNAVAILABLE", "DEADLINE", "imed out", "Timeout")


def with_retry(fn, label: str, retries: int = 8):
    """Call fn(); on quota/transient errors back off exponentially (4s … 120s) and try again."""
    delay = 4.0
    for attempt in range(retries):
        try:
            return fn()
        except Exception as e:
            msg = str(e)
            if attempt == retries - 1 or not any(c in msg for c in TRANSIENT):
                raise
            print(f"    retry {attempt + 1} ({label}, {delay:.0f}s): {type(e).__name__} {msg[:70]}", flush=True)
            time.sleep(delay)
            delay = min(delay * 2, 120)
    raise RuntimeError("unreachable")


def synth(text: str, voice: str, model: str = DEFAULT_MODEL, style: str = STYLE) -> Path:
    """Return a cached WAV for (text, voice, model, style), calling the API only on a cache miss."""
    from google.genai import types

    CACHE.mkdir(parents=True, exist_ok=True)
    path = CACHE / f"{cache_key(text, voice, model, style)}.wav"
    if path.exists():
        return path
    config = types.GenerateContentConfig(
        response_modalities=["AUDIO"],
        speech_config=types.SpeechConfig(
            language_code="da-DK",
            voice_config=types.VoiceConfig(prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name=voice)),
        ),
    )
    contents = f"{style}:\n{text}" if style else text
    r = with_retry(lambda: client().models.generate_content(model=model, contents=contents, config=config), voice)
    data = r.candidates[0].content.parts[0].inline_data.data
    tmp = path.with_name(f"{path.stem}.{threading.get_ident()}.tmp")
    _write_wav(tmp, data)
    tmp.replace(path)
    return path


_cast = None


def load_cast() -> dict:
    """audio/cast.yaml: {model, default, roles: {who: voice}}; 'who' is a script speaker name."""
    global _cast
    if _cast is None:
        import yaml
        _cast = yaml.safe_load((AUDIO / "cast.yaml").read_text(encoding="utf-8"))
    return _cast


def segment_audio(seg: dict) -> tuple[str, str, str, str]:
    """(text to speak, voice, model, 16-char file key) for one script segment."""
    cast = load_cast()
    text = seg.get("say") or seg["da"].replace("**", "").replace("[[", "").replace("]]", "")
    for written, said in (cast.get("lexicon") or {}).items():   # abbreviations etc. the model misreads
        text = text.replace(written, said)
    voice = cast.get("roles", {}).get(seg.get("who", "narrator")) or cast["default"]
    model = cast.get("model", DEFAULT_MODEL)
    return text, voice, model, cache_key(text, voice, model)[:16]


def duration(wav_path: Path) -> float:
    with wave.open(str(wav_path)) as w:
        return w.getnframes() / w.getframerate()


def encode(wav_path: Path, out_path: Path, bitrate: str = "48k") -> Path:
    """WAV -> mono AAC (.m4a), trimming leading/trailing silence. Skips work if already encoded."""
    if out_path.exists() and out_path.stat().st_mtime >= wav_path.stat().st_mtime:
        return out_path
    out_path.parent.mkdir(parents=True, exist_ok=True)
    trim = ("silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.05,"
            "areverse,silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.25,areverse")
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav_path), "-af", trim,
         "-ac", "1", "-c:a", "aac", "-b:a", bitrate, "-movflags", "+faststart", str(out_path)],
        check=True,
    )
    return out_path
