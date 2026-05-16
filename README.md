# yt-aug — YouTube Augment

Download audio from YouTube playlists and copy playlists to your account — from the command line.

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

### `download <playlist_url>`

Downloads audio from a YouTube playlist. Extracts best available audio and converts to m4a at 192kbps via FFmpeg.

```bash
ytaug download "https://youtube.com/playlist?list=PL..." -o ~/Music
ytaug download "https://music.youtube.com/playlist?list=PL..."
```

Before downloading, ytaug will:
1. Check for a JS runtime and ffmpeg
2. Fetch the playlist metadata (name, track count)
3. Ask for confirmation

| Flag | Short | Description |
|------|-------|-------------|
| `--output` | `-o` | Output directory (default: current directory) |

### `copy <playlist_url>`

Creates a copy of a YouTube playlist in your account using the YouTube Data API. Requires authentication.

```bash
ytaug auth login
ytaug copy "https://youtube.com/playlist?list=PL..." --name "My Favorites" --public
```

| Flag | Short | Description |
|------|-------|-------------|
| `--name` | `-n` | Custom name for the new playlist (default: original title) |
| `--public` | `-p` | Make the new playlist public (default: private) |

### `auth`

Authentication commands for YouTube Data API access.

```bash
ytaug auth login --help
ytaug auth login
ytaug auth login --no-browser
ytaug auth logout --all
ytaug auth whoami
```

#### `auth login`

Authenticate with your YouTube account via OAuth2.

| Flag | Short | Description |
|------|-------|-------------|
| `--force` | `-f` | Re-authenticate even if already logged in |
| `--no-browser` | | Print auth URL instead of opening a browser (for headless environments) |

On first login, you'll be prompted for a `client_secret.json` file. This file contains your OAuth2 credentials and can be obtained from the [Google Cloud Console](https://console.cloud.google.com/).

#### `auth logout`

Revoke authentication tokens and log out.

| Flag | Short | Description |
|------|-------|-------------|
| `--all` | `-a` | Also delete the client secrets file |

#### `auth whoami`

Show the currently authenticated user's name and email.

## Examples

Download a playlist to a specific directory:
```bash
ytaug download "https://youtube.com/playlist?list=PL_abc123" -o ~/Music/playlists
```

Copy a public playlist as private:
```bash
ytaug copy "https://youtube.com/playlist?list=PL_abc123" --name "Road Trip"
```

## API Quota

The `copy` command uses the YouTube Data API v3, which has a daily quota of 10,000 units. Each operation costs:

| Operation | Cost |
|-----------|------|
| `playlists().insert` (create playlist) | 50 units |
| `playlistItems().insert` (add video) | 50 units per video |

## Authentication

To use the `copy` command, you need OAuth2 credentials:

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select existing)
3. Enable the **YouTube Data API v3**
4. Create credentials → **OAuth 2.0 Client IDs** → **Desktop app**
5. Download the JSON file as `client_secret.json`
6. Run `ytaug auth login` and provide the file path

## Development

```bash
# Install with dev dependencies
uv sync

# Run tests
uv run pytest

# Run linting
uv run ruff check .
```

## Architecture

```
src/ytaug/
├── main.py         Typer CLI entry point
├── download.py     yt-dlp wrapper (downloads, system checks)
├── copy.py         YouTube Data API operations
├── auth.py         OAuth2 authentication flow
├── playlist.py     URL parsing and playlist metadata
└── exceptions.py   YTAugError hierarchy
```

- `main.py` handles all CLI interaction (prompts, messages, exits)
- Library modules (`download.py`, `auth.py`, `copy.py`, `playlist.py`) are pure logic with no console output
- All library functions raise `YTAugError` subclasses on operational failure
