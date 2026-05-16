# ytaug (YouTube Augment)

Python 3.13+ required (see `pyproject.toml`).

## Project Structure

```
src/ytaug/
├── __init__.py      (package marker)
├── main.py          (Typer CLI entry point)
├── auth.py          (OAuth2 authentication flow)
├── copy.py          (YouTube Data API operations)
├── download.py      (pure logic: downloads, system checks, metadata)
├── exceptions.py    (YTAugError hierarchy)
└── playlist.py      (URL parsing and playlist metadata)
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

## CLI Commands (`ytaug`)

### `download` (implemented)
Downloads audio from a YouTube playlist URL.

1. Checks for JS runtime (deno/node) and ffmpeg, exits with install instructions if missing
2. Fetches playlist metadata (name, track count) from URL using yt-dlp
3. Shows interactive `[y/N]` confirmation via `typer.confirm()`
4. Downloads best audio → converts to m4a (192kbps) via FFmpeg

```bash
ytaug download <playlist_url> [--output <path>]
```

| Flag | Short | Description |
|------|-------|-------------|
| `--output` | `-o` | Output directory (default: current directory) |

### `copy`
Creates a copy of a YouTube playlist in the user's account. Uses YouTube Data API.

```bash
ytaug copy <playlist_url> [--name <name>] [--public]
```

| Flag | Short | Description |
|------|-------|-------------|
| `--name` | `-n` | Custom name for the new playlist |
| `--public` | `-p` | Make the new playlist public (default: private) |

### `auth`
Subcommands for authentication.

```bash
ytaug auth login [--force] [--no-browser]
ytaug auth logout [--all]
ytaug auth whoami
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
- Library modules (`download.py`, `auth.py`, `copy.py`, `playlist.py`) are pure logic with no console output
- All library functions raise `YTAugError` subclasses on operational failure

## Dev commands

Not yet established. When adding tooling:
- Use `ruff` for linting (faster than flake8)
- Use `pytest` for testing

## Notes

- Uses `uv` as package manager (see `uv.lock`)
- Entry point: `ytaug = "ytaug.main:app"` (console script)
- `client_secrets.json` contains YouTube OAuth2 credentials for the `copy`/`authorize` commands
