import shutil
import platform
import yt_dlp
import urllib
from pathlib import Path
from ytaug.exceptions import YTAugError

# TODO: handle playlist does not exist:"https://www.youtube.com/playlist?list=PLwivhteH3vK_S0yV2w3gCh_zM-2S_3N-Z"
# TODO: handle no internet connection error


def has_ffmpeg() -> bool:
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


def has_js_runtime() -> bool:
    """
    Checks for available JS runtimes in order of preference.

    Returns:
        True if at least one runtime is available, False otherwise.
    """
    for runtime in ("deno", "node"):
        full_path = shutil.which(runtime)
        if full_path:
            return True
    return False


def get_ytdlp_js_runtime_config() -> dict:
    """
    Returns a yt-dlp js_runtimes config dict with all found JS runtimes.

    Returns:
        dict in js_runtimes format, e.g. {"deno": {"path": "/usr/bin/deno"}}.
        Empty dict if no runtime found.
    """
    config = {}
    for runtime in ("deno", "node"):
        path = shutil.which(runtime)
        if path:
            config[runtime] = {"path": path}
    return config


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


def is_youtube_url(url: str | None) -> bool:
    if not url:
        return False

    try:
        parsed = urllib.parse.urlparse(url)
    except Exception:
        return False

    domain = parsed.netloc or parsed.path.split("/")[0]
    domain = domain.lower()
    domain = domain.removeprefix("www.")

    return domain in ("youtube.com", "m.youtube.com", "music.youtube.com", "youtu.be")


def get_url_info_ytdlp(url: str, js_runtime_config: dict) -> dict:
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
            raise YTAugError("Provided url is private") from e

        raise YTAugError("Error in get_url_info_ytdlp") from e

    url_info = {
        "type": info.get("_type"),
        "title": info.get("title"),
        "id": info.get("id"),
    }
    if (url_info.get("type")) == "playlist":
        url_info["video_count"] = info.get("playlist_count")

    return url_info


def download_url_ytdlp(
    url: str, target_path: Path, is_playlist: bool, js_runtime_config: dict
) -> None:
    ydl_opts = {
        # "quiet": True,
        "format": "bestaudio/best",
        "outtmpl": str(target_path / "%(title)s.%(ext)s"),
        "js_runtimes": js_runtime_config,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "m4a",
                "preferredquality": "192",
            }
        ],
    }
    if is_playlist:
        ydl_opts["outtmpl"] = str(
            target_path / "%(playlist_title)s" / "%(title)s.%(ext)s"
        )

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        raise YTAugError("Error in download_url_ytdlp") from e


if __name__ == "__main__":
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": True,
        "js_runtimes": get_ytdlp_js_runtime_config,
    }
    url = None

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        print(info)
