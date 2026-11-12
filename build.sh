#!/usr/bin/env bash
# Usage: ./build.sh assets/voice.mp3
set -euo pipefail
AUDIO="${1:-assets/voice.mp3}"
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT/src"
python3 timeline.py                                  # renders frames in 150-frame chunks -> src/chunks
ls chunks/*.mp4 | sort | sed "s#^#file '$PWD/#; s#\$#'#" > chunks/list.txt
ffmpeg -y -v error -f concat -safe 0 -i chunks/list.txt -c copy ../out/video-silent.mp4
ffmpeg -y -v error -i ../out/video-silent.mp4 -i "$ROOT/$AUDIO" -c:v libx264 -crf 22 -preset medium -pix_fmt yuv420p \
  -c:a aac -b:a 192k -af apad -t 94.0 -movflags +faststart ../out/short.mp4
echo "Done: out/short.mp4"
