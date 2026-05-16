# ytmm (YouTube Music Manager)

Python 3.13+ required (see `pyproject.toml`).

## Project Structure

```
src/ytmm/
├── __init__.py      (package marker)
├── download.py      (pure logic: downloads, system checks, metadata)
└── main.py          (Typer CLI entry point)
```

## Dependencies

| Package | Purpose |
|---------|---------|
| `typer` | CLI framework |
| `yt-dlp` | Video/audio download engine |
| `yt-dlp-ejs` | EJS challenge solver scripts (required for YouTube) |

## System Requirements

The following must be installed on the user's machine:

| Binary | Purpose | Windows | macOS | Linux |
|--------|---------|---------|-------|-------|
| `ffmpeg` | Audio extraction/conversion | `winget install ffmpeg` | `brew install ffmpeg` | `sudo apt install ffmpeg` |
| `deno` or `node` | JS runtime for YouTube challenge solving (deno is default, node ≥ 20 required) | `winget install deno` / `winget install OpenJS.NodeJS` | `brew install deno` / `brew install node` | `curl -fsSL https://deno.land/install.sh \| sh` / See [nodejs.org](https://nodejs.org/en/download/package-manager) |

## CLI Commands (`ytmm`)

### `download` (implemented)
Downloads audio from a YouTube playlist URL.

1. Checks for JS runtime (deno/node) and ffmpeg, exits with install instructions if missing
2. Fetches playlist metadata (name, track count) from URL using yt-dlp
3. Shows interactive `[y/N]` confirmation via `typer.confirm()`
4. Downloads best audio → converts to m4a (192kbps) via FFmpeg

```bash
ytmm download <playlist_url> [--output <path>]
```

| Flag | Short | Description |
|------|-------|-------------|
| `--output` | `-o` | Output directory (default: current directory) |

### `copy`
Creates a copy of a YouTube playlist in the user's account. Uses YouTube Data API.

```bash
ytmm copy <playlist_url> [--name <name>] [--public]
```

| Flag | Short | Description |
|------|-------|-------------|
| `--name` | `-n` | Custom name for the new playlist |
| `--public` | `-p` | Make the new playlist public (default: private) |

### `auth`
Subcommands for authentication.

```bash
ytmm auth login [--force] [--no-browser]
ytmm auth logout [--all]
ytmm auth whoami
```

| Command | Description |
|---------|-------------|
| `login` | Authenticate with your YouTube account |
| `logout` | Revoke authentication tokens and log out |
| `whoami` | Show the currently authenticated user |

| Flag | Short | Description |
|------|-------|-------------|
| `--force` | `-f` | Skip confirmation for re-authentication |
| `--no-browser` / `--headless` | | Print auth URL instead of opening a browser |
| `--all` | `-a` | Also delete client secrets on logout |

## Architecture

- `main.py` handles all CLI interaction (prompts, messages, exits)
- `download.py` is a pure logic module (no console output) with functions:
  - `check_ffmpeg()` → `bool`
  - `check_js_runtime()` → `str | None`
  - `get_js_runtime_config()` → `dict` (yt-dlp `js_runtimes` format)
  - `get_playlist_info(url)` → `Tuple[str, int]` (name, count) or `ValueError`
  - `download_playlist(url, path)` → `bool`
- yt-dlp is configured with: `format: bestaudio/best`, `js_runtimes: {runtime: {path: ...}}`, `FFmpegExtractAudio` postprocessor

## Dev commands

Not yet established. When adding tooling:
- Use `ruff` for linting (faster than flake8)
- Use `pytest` for testing

## Notes

- Uses `uv` as package manager (see `uv.lock`)
- Entry point: `ytmm = "ytmm.main:app"` (console script)
- `client_secrets.json` contains YouTube OAuth2 credentials for the `copy`/`authorize` commands
