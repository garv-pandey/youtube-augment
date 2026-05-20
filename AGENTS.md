# ytaug (YouTube Augment)

Python 3.13+ required (see `pyproject.toml`).

## Project Structure

```
src/ytaug/
├── __init__.py      (package marker)
├── main.py          (Typer CLI entry point — orchestration + user I/O)
├── download.py      (pure logic: system checks, URL validation, metadata, downloads)
└── exceptions.py    (YTAugError hierarchy)

tests/
├── unit/
│   └── test_download.py   (unit tests with mocks)
└── integration/
    ├── __init__.py
    └── test_download.py   (live tests against real YouTube URLs)
```

## Dependencies

| Package | Purpose |
|---------|---------|
| `typer` | CLI framework |
| `yt-dlp` | Video/audio download engine |
| `yt-dlp-ejs` | EJS challenge solver scripts (required for YouTube) |

Dev dependencies:
| Package | Purpose |
|---------|---------|
| `pytest` | Test runner |
| `pytest-mock` | Mocking (`mocker` fixture) |

## System Requirements

The following must be installed on the user's machine:

| Binary | Purpose | Windows | macOS | Linux |
|--------|---------|---------|-------|-------|
| `ffmpeg` | Audio extraction/conversion | `winget install ffmpeg` | `brew install ffmpeg` | `sudo apt install ffmpeg` |
| `deno` or `node` | JS runtime for YouTube challenge solving (deno is default, node ≥ 20 required) | `winget install deno` / `winget install OpenJS.NodeJS` | `brew install deno` / `brew install node` | `curl -fsSL https://deno.land/install.sh \| sh` / See [nodejs.org](https://nodejs.org/en/download/package-manager) |

## CLI Commands (`ytaug`)

### `download` (implemented)
Downloads audio from a YouTube URL (video or playlist).

1. Checks for JS runtime and ffmpeg, exits with install instructions if missing
2. Validates the URL is from a YouTube domain
3. Fetches metadata (title, type, track count for playlists) using yt-dlp
4. Shows interactive `[y/N]` confirmation with download destination
5. Downloads best audio → organizes playlists into subfolders → converts to m4a (192kbps) via FFmpeg

```bash
ytaug download <url> [--output <path>]
```

| Flag | Short | Description |
|------|-------|-------------|
| `--output` | `-o` | Output directory (default: current directory) |

## Architecture

- `main.py` handles all CLI interaction (prompts, messages, exits), orchestrates checks
- `download.py` is a pure logic module (no console output) with functions:
  - `has_ffmpeg()` → `bool`
  - `has_js_runtime()` → `bool`
  - `get_ffmpeg_install_instructions()` → `str`
  - `get_js_runtime_install_instructions()` → `str`
  - `get_ytdlp_js_runtime_config()` → `dict` (yt-dlp `js_runtimes` format)
  - `is_youtube_url(url)` → `bool`
  - `get_url_info_ytdlp(url, js_runtime_config)` → `dict` (title, type, id, video_count)
  - `download_url_ytdlp(url, target_path, is_playlist, js_runtime_config)` → `None`
- yt-dlp is configured with: `format: bestaudio/best`, `js_runtimes: {runtime: {path: ...}}`, `FFmpegExtractAudio` postprocessor
- All library functions raise `YTAugError` on operational failure

## Dev commands

```bash
uv run pytest                  # full suite (unit + integration)
uv run pytest tests/unit       # unit tests only
uv run pytest -m integration   # integration tests only
uv run ruff check .
```

## Notes

- Uses `uv` as package manager (see `uv.lock`)
- Entry point: `ytaug = "ytaug.main:app"` (console script)
- Integration tests require a JS runtime + ffmpeg on the system
- Integration tests marked with `@pytest.mark.integration`
