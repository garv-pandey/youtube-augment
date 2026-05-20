# yt-aug — YouTube Augment

Download audio from YouTube videos and playlists — from the command line.

## Install

```bash
pip install yt-aug
```

Requires Python 3.13+.

## System Requirements

yt-aug uses `yt-dlp` under the hood, which needs the following installed on your machine:

| Binary | Purpose | Windows | macOS | Linux |
|--------|---------|---------|-------|-------|
| `ffmpeg` | Audio extraction/conversion | `winget install ffmpeg` | `brew install ffmpeg` | `sudo apt install ffmpeg` |
| `deno` or `node` (≥ 20) | JS runtime for YouTube challenge solving | `winget install deno` | `brew install deno` | `curl -fsSL https://deno.land/install.sh \| sh` |

## Usage

### `download <url>`

Downloads audio from a YouTube video or playlist. Extracts best available audio and converts to m4a at 192kbps via FFmpeg.

```bash
ytaug download "https://youtube.com/watch?v=..." -o ~/Music
ytaug download "https://youtube.com/playlist?list=PL..." -o ~/Music
ytaug download "https://music.youtube.com/playlist?list=PL..."
```

Before downloading, ytaug will:
1. Check for a JS runtime and ffmpeg
2. Fetch the URL metadata (title, type, track count for playlists)
3. Ask for confirmation

For playlists, files are organized into a subfolder named after the playlist.

| Flag | Short | Description |
|------|-------|-------------|
| `--output` | `-o` | Output directory (default: current directory) |

## Development

```bash
# Install with dev dependencies
uv sync

# Run tests
uv run pytest

# Run unit tests only
uv run pytest tests/unit

# Run integration tests only (requires JS runtime + ffmpeg + network)
uv run pytest tests/integration -m integration
```

## Architecture

```
src/ytaug/
├── main.py         Typer CLI entry point (orchestration + user I/O)
├── download.py     yt-dlp wrapper (system checks, URL validation, metadata, downloads)
└── exceptions.py   YTAugError hierarchy
```

- `main.py` handles all CLI interaction (prompts, messages, exits)
- `download.py` is pure logic with no console output
- All library functions raise `YTAugError` subclasses on operational failure
