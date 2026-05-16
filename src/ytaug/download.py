import shutil
import platform
import yt_dlp
from pathlib import Path
from ytmm.exceptions import SystemRequirementError, YTMMError


def check_ffmpeg() -> bool:
    return shutil.which("ffmpeg") is not None


def get_ffmpeg_install_instructions() -> str:
    os_name = platform.system()
    instructions = {
        "Windows": "winget install ffmpeg",
        "Darwin": "brew install ffmpeg",
        "Linux": "sudo apt install ffmpeg (Debian/Ubuntu) or sudo dnf install ffmpeg (Fedora)",
    }
    return instructions.get(os_name, "See https://ffmpeg.org/download.html")


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
        "Windows": "winget install deno  OR  winget install OpenJS.NodeJS",
        "Darwin": "brew install deno  OR  brew install node",
        "Linux": "curl -fsSL https://deno.land/install.sh | sh  OR  See https://nodejs.org/en/download/package-manager",
    }
    return instructions.get(
        os_name, "See https://deno.land  OR  See https://nodejs.org"
    )


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
        raise YTMMError("Error in download_playlist") from e
