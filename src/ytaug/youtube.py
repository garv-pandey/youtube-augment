from typing import Annotated
import urllib.parse
from ytaug.exceptions import YTAugError


# TODO: way for user to request for Unsupported urls


def is_youtube_domain(url: str) -> bool:
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
    domain = parsed.netloc or parsed.path.split("/")[0]
    domain = domain.lower()
    domain = domain.removeprefix("www.")

    return domain in ("youtube.com", "m.youtube.com", "music.youtube.com", "youtu.be")


def extract_youtube_video_id(url: str) -> str | None:
    """
    extracts video_id from video and video_in_playlist urls
    """

    parsed = urllib.parse.urlparse(url)

    # only few videos in season based playlist have weird url,
    # they contain 'path=/watch_videos', unique from all
    if parsed.path == "/watch_videos":
        # query='video_ids=yRmOWcWdQAo%2ClsbcN9-jU1Y%2ChRSGxw2AQnk%2C1BVJzaXv3rk%2CQ-nWA0WeF98&type=0&title=Roman+History+%E2%80%A2+Top+episodes+for+you'
        # -> yRmOWcWdQAo
        val = parsed.query.split("%", 1)[0]
        val = val.removeprefix("video_ids=")
        return val

    # video and video in playlist, 'path = /watch'
    if parsed.path == "/watch":
        # query='v=kPkT0jMjEu8&list=RDATmba11fjz9y3mcE' -> RDATmba11fjz9y3mcE

        val = parsed.query
        val = val.split("&", 1)[0]
        val = val.removeprefix("v=")
        return val

    return None


def extract_youtube_playlist_id(url: str) -> str | None:
    """
    extracts playlist_id from urls.
    does not extracts playlist_id from video_in_playlist urls,
    only pure playlist only urls
    """

    parsed = urllib.parse.urlparse(url)

    # season based playlist urls, 'path=/show'
    if parsed.path.startswith("/show"):
        # path='/show/VLPLQw_XrMliWVYdCBZ-ZJcv5nvUrjQPmjyY' -> PLQw_XrMliWVYdCBZ-ZJcv5nvUrjQPmjyY
        val = parsed.path.split("/")[-1]
        val = val.removeprefix("VL")
        return val

    # regular playlist url, path='/playlist'
    if parsed.path == "/playlist":
        # query='list=PLMlRYqqqM5rrjeaJuVaC6MWN7e7fSXGJt' -> PLMlRYqqqM5rrjeaJuVaC6MWN7e7fSXGJt
        val = parsed.query.removeprefix("list=")
        return val

    return None


def get_youtube_playlist_url(playlist_id: str) -> str:
    """
    Build a standard YouTube playlist URL from a playlist ID.

    Args:
        playlist_id: The playlist ID to embed in the URL.

    Returns:
        A full YouTube playlist URL string.
    """
    return f"https://www.youtube.com/playlist?list={playlist_id}"


def get_youtube_video_url(video_id: str) -> str:
    """
    Build a standard YouTube video URL from a video ID.

    Args:
        video_id: The video ID to embed in the URL.

    Returns:
        A full YouTube video URL string.
    """
    return f"https://www.youtube.com/watch?v={video_id}"
