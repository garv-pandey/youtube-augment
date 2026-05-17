import shutil
import platform
import yt_dlp
from pathlib import Path
from ytaug.exceptions import SystemRequirementError, YTAugError


def check_ffmpeg() -> bool:
    return shutil.which("ffmpeg") is not None


def get_ffmpeg_install_instructions() -> str:
    os_name = platform.system()
    instructions = {
        "Windows": "winget install ffmpeg \nor check their website: https://ffmpeg.org",
        "Darwin": "brew install ffmpeg \nor check their website: https://ffmpeg.org",
        "Linux": "sudo apt install ffmpeg (Debian/Ubuntu) \nor sudo dnf install ffmpeg (Fedora) \nor check their website: https://ffmpeg.org",
    }
    return instructions.get(
        os_name, "check their website for download instructions \nhttps://ffmpeg.org"
    )


def get_js_runtime() -> tuple[str, dict]:
    """
    Checks for available JS runtimes and returns:
    - The runtime name
    - yt-dlp js_runtimes config dict

    Raises:
        SystemRequirementError if not js runtime found in system
    """
    for runtime in ("deno", "node"):
        full_path = shutil.which(runtime)
        if full_path:
            return runtime, {runtime: {"path": full_path}}

    raise SystemRequirementError("No JavaScript runtime found.")


def get_js_runtime_install_instructions() -> str:
    os_name = platform.system()
    instructions = {
        "Windows": "winget install deno  OR  winget install OpenJS.NodeJS \nor check their website: \nhttps://deno.com OR https://nodejs.org",
        "Darwin": "brew install deno  OR  brew install node \nor check their website: \nhttps://deno.com OR https://nodejs.org",
        "Linux": "curl -fsSL https://deno.land/install.sh | sh  OR  See https://nodejs.org/en/download/package-manager \nor check their website: \nhttps://deno.com OR https://nodejs.org",
    }
    return instructions.get(
        os_name,
        "check their website for download instructions \nhttps://deno.com OR  See https://nodejs.org",
    )


def get_playlist_info_dlp(url: str, js_runtime_config: dict) -> dict:
    """
    runtime: {"path": full_path}}
    """

    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": True,
        "js_runtimes": js_runtime_config,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
    except Exception as e:
        if "private" in str(e).lower():
            raise YTAugError("Provided playlist is private") from e

        raise YTAugError("Error in get_playlist_info_dlp") from e

    playlist_info = {
        "owner_channel_id": info.get("uploader_id"),
        "id": info.get("id"),
        "title": info.get("title"),
        "description": info.get("description"),
        "video_count": info.get("playlist_count") or len(info.get("entries")),
        "privacy_status": info.get("availability"),
        "is_playlist": info.get("_type") == "playlist",
    }
    if not playlist_info.get("is_playlist"):
        raise YTAugError("Provided URL is not a youtube palylist")

    return playlist_info


def download_playlist(playlist_url: str, target_path: Path, js_runtimes: dict) -> None:
    ydl_opts = {
        # "quiet": True,
        "format": "bestaudio/best",
        "outtmpl": str(target_path / "%(title)s.%(ext)s"),
        "js_runtimes": js_runtimes,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "m4a",
                "preferredquality": "192",
            }
        ],
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([playlist_url])
    except Exception as e:
        raise YTAugError("Error in download_playlist") from e
