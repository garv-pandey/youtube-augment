from typing import Annotated
import urllib.parse


# TODO: check how does yt_dlp handles infinite mix palylists whose id starts with RD
# TODO: check how does yt_dlp handles season based playlist url

# yt_video : path = /watch, query = video id
# yt_palylist: path = /playlist, query = playlist id
# yt video in playlist : path =  /watch, query = video id
# yt video in mix playlist: path = /watch, query = video id
# yt season playlist: path = /show/playlist_id
# yt video in season playlist: path = /watch_videos, query = video_ids=[video's id]%...
# for all ytm urls, path = /watch for videos and video in playlist, /query is id of video
# for all ytm urls, path = /playlist for all mix and regular playlist, /querys in id of playlist


def is_youtube_domain(url: str | None) -> bool:
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


def extract_youtube_video_and_playlist_id(
    url: str,
) -> dict[str, str | None]:
    result: dict[str, str | None] = {"video_id": None, "playlist_id": None}
    parsed = urllib.parse.urlparse(url)
    """
    for pure playlist url, extract playlist_id
    for pure video and video in playlist url, extract only video_id
    """

    # all season based playlist urls
    if parsed.path.startswith("/show"):
        # path='/show/VLPLQw_XrMliWVYdCBZ-ZJcv5nvUrjQPmjyY' -> PLQw_XrMliWVYdCBZ-ZJcv5nvUrjQPmjyY
        val = parsed.path.split("/")[-1]
        val = val.removeprefix("VL")
        result["playlist_id"] = val

    # only few videos in season based playlist have weird url,
    # those videos contain 'path=/watch_videos', unique from all
    elif parsed.path.startswith("/watch_videos"):
        # query='video_ids=yRmOWcWdQAo%2ClsbcN9-jU1Y%2ChRSGxw2AQnk%2C1BVJzaXv3rk%2CQ-nWA0WeF98&type=0&title=Roman+History+%E2%80%A2+Top+episodes+for+you'
        # -> yRmOWcWdQAo
        val = parsed.query.split("%", 1)[0]
        val = val.removeprefix("video_ids=")
        result["video_id"] = val

    # regular playlist url, path='/playlist'
    elif parsed.path.startswith("/playlist"):
        # query='list=PLMlRYqqqM5rrjeaJuVaC6MWN7e7fSXGJt' -> PLMlRYqqqM5rrjeaJuVaC6MWN7e7fSXGJt
        val = parsed.query.removeprefix("list=")

        # mix playlists are infinite and unviewable on youtube
        # dont support download for them
        # their ids start with RD
        if val.startswith("RD"):
            print(parsed)
            print("mix playlists are infinite and cannot be downloaded")
            return result

        result["playlist_id"] = val
        print(val)

    # video, video in playlist 'path = /watch'
    else:
        # query='v=kPkT0jMjEu8&list=RDATmba11fjz9y3mcE' -> RDATmba11fjz9y3mcE

        val = parsed.query
        val = val.split("&", 1)[0]
        val = val.removeprefix("v=")

        result["video_id"] = val

    return result


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
