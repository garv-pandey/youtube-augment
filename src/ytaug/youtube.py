import urllib

from tests.conftest import YT_VIDEOS
import ytaug

# TODO: check how does yt_dlp handles infinite mix palylists whose id starts with RD
# TODO: check how does yt_dlp handles season based playlist url


def is_youtube_url(url: str | None) -> bool:
    """
    Check if a URL belongs to a YouTube domain.

    Args:
        url: The URL to check. Accepts standard YouTube, YouTube Music,
            mobile YouTube, and youtu.be short links.

    Returns:
        True if the URL is from a recognized YouTube domain, False otherwise.
    """
    if not url:
        return False

    parsed = urllib.parse.urlparse(url)
    print(parsed)
    domain = parsed.netloc or parsed.path.split("/")[0]
    domain = domain.lower()
    domain = domain.removeprefix("www.")

    return domain in ("youtube.com", "m.youtube.com", "music.youtube.com", "youtu.be")


def is_youtube_video(url: str | None) -> bool:
    """
    Check if a URL points to a YouTube video.

    A video in a playlist is considered a video and returns True.

    Args:
        url: The URL to check.

    Returns:
        True if the URL contains a video ID (v query parameter), False otherwise.
    """
    if not is_youtube_url(url):
        return False

    parsed = urllib.parse.urlparse(url)
    query_params = urllib.parse.parse_qs(parsed.query)
    return "v" in query_params


def is_youtube_playlist(url: str | None) -> bool:
    """
    Check if a URL points to a pure YouTube playlist.

    A video within a playlist is considered a video and returns False.
    Only URLs with a /playlist path and a list parameter but no v parameter
    are treated as playlists.

    Args:
        url: The URL to check.

    Returns:
        True if the URL is a standalone playlist URL, False otherwise.
    """
    if not is_youtube_url(url):
        return False

    parsed = urllib.parse.urlparse(url)
    query_params = urllib.parse.parse_qs(parsed.query)
    return (
        "list" in query_params
        and "v" not in query_params
        and parsed.path == "/playlist"
    )


def get_youtube_video_id(url: str | None) -> str | None:
    """
    Extract the video ID from a YouTube URL.

    Supports three URL formats:
    1. Standard watch URLs (?v=...)
    2. youtu.be short links (youtu.be/VIDEO_ID)
    3. Shorts URLs (/shorts/VIDEO_ID)

    Args:
        url: The YouTube URL potentially containing a video ID.

    Returns:
        The video ID string, or None if no video ID is found.
    """
    if not url:
        return None

    parsed = urllib.parse.urlparse(url)
    query_params = urllib.parse.parse_qs(parsed.query)
    ids = query_params.get("v")
    if ids:
        return ids[0]

    domain = (parsed.netloc or parsed.path.split("/")[0]).lower()
    domain = domain.removeprefix("www.")
    if domain == "youtu.be":
        path = parsed.path.strip("/")
        return path.split("/")[0] if path else None

    path_segments = parsed.path.strip("/").split("/")
    if len(path_segments) >= 2 and path_segments[0] == "shorts":
        return path_segments[1]

    return None


def get_youtube_playlist_id(url: str | None) -> str | None:
    """
    Extract the playlist ID from a YouTube URL.

    Works for both pure playlist URLs (/playlist?list=...) and
    video-in-playlist URLs (/watch?v=...&list=...).

    Args:
        url: The YouTube URL potentially containing a playlist ID.

    Returns:
        The playlist ID string, or None if no playlist ID is found.
    """
    if not url:
        return None

    parsed = urllib.parse.urlparse(url)
    query_params = urllib.parse.parse_qs(parsed.query)
    ids = query_params.get("list")
    return ids[0] if ids else None


def get_youtube_video_url(id: str) -> str:
    """
    Build a standard YouTube watch URL from a video ID.

    Args:
        id: The video ID to embed in the URL.

    Returns:
        A full YouTube watch URL string.
    """
    return f"https://www.youtube.com/watch?v={id}"


def get_youtube_playlist_url(id: str) -> str:
    """
    Build a standard YouTube playlist URL from a playlist ID.

    Args:
        id: The playlist ID to embed in the URL.

    Returns:
        A full YouTube playlist URL string.
    """
    return f"https://www.youtube.com/playlist?list={id}"

if __name__ == "__main__":
    from ytaug.tests.conftest.py import *
    url = YT_VIDEOS[0].["url"]
    print(url)
