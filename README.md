# Shor's Algorithm Short (1080x1920, 30 fps)

"Quantum Computers Don't Break Encryption the Way You Think" — one continuous, fade-free animated YouTube Short
rendered 100% in Python (Pillow + numpy) and encoded with ffmpeg. Animation is synced to a single ElevenLabs voiceover.

## Requirements
- Python 3.10+, `pip install -r requirements.txt`
- ffmpeg
- Fonts (Linux paths used in `src/lib2.py`): Liberation Serif Bold, Inter Bold, DejaVu Sans Mono Bold

## Build
```bash
pip install -r requirements.txt
# put your voiceover at assets/voice.mp3 (not committed)
./build.sh assets/voice.mp3     # -> out/short.mp4
cd src && python3 thumbnail.py  # -> out/thumbnail.png / .jpg
```
Resumable: finished chunks in `src/chunks` are skipped. Delete that folder to re-render everything.

## Layout
| File | Role |
|---|---|
| `src/lib2.py` | Canvas (2x supersampling + glow pass), colors, easing, primitives |
| `src/kit.py` | Icons, captions, HUD chapter bar, helpers |
| `src/scenes_a.py` | Scenes 1-7 (myth, collapse, RSA, number, primes, years, Shor) |
| `src/scenes_b.py` | Scenes 8-18 (loop ring, laptop, spiral to wave, interference, bank, qubits, harvest, standards, key, finale) |
| `src/timeline.py` | Scene schedule (times in seconds from the audio), slide/zoom transitions, chunked renderer |
| `src/peek.py` | Contact sheet for QA: `python3 peek.py ../out/sheet.png 1.0 5.0 12.0` |
| `src/thumbnail.py` | Static 1080x1920 thumbnail |

## Syncing to new audio
All beats use absolute timestamps from the mp3 (measured with `ffmpeg -af silencedetect`). For a new
voiceover, re-measure the pauses and update the times in `scenes_*.py` and the `SC` list in `timeline.py`.
Sync is per phrase, not per word.
