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


# supported url examples:
# video only:-  https://www.youtube.com/watch?v=0PAEqgfAts4
# playlist only:- https://www.youtube.com/playlist?list=PLQSoWXSpjA39U94TANpW67fxfYhm5CFFT
# video in playlist:- https://www.youtube.com/watch?v=0PAEqgfAts4&list=PLQSoWXSpjA39U94TANpW67fxfYhm5CFFT&index=2&t=36s
# video in mix playlist:- https://www.youtube.com/watch?v=ZjPB3a2t1vk&list=RDZjPB3a2t1vk&start_radio=1
# season based playlist:- https://www.youtube.com/show/VLPLQw_XrMliWVa1cUis273NsyXIvH5DW6o2?season=AllEpisodes&sbp=CgtBbGxFcGlzb2RlcxoAKgt5Um1PV2NXZFFBb0AB

# Unsupported url examples:
# mix playlist:- https://music.youtube.com/playlist?list=RDATmba11fjz9y3mcE
# mix playlist:- https://music.youtube.com/playlist?list=TLGGZzPOc7XL31kyMzA1MjAyNg
# legacy playlist url:- https://www.youtube.com/watch_videos?video_ids=yRmOWcWdQAo%2ClsbcN9-jU1Y%2ChRSGxw2AQnk%2C1BVJzaXv3rk%2CQ-nWA0WeF98&type=0&title=Roman+History+%E2%80%A2+Top+episodes+for+you


def extract_youtube_video_and_playlist_id(url: str) -> dict[str, str | None]:
    result = {"video_id": None, "playlist_id": None}

    parsed = urllib.parse.urlparse(url)

    # /show contains only playlist_id
    # season based playlist urls, 'path=/show'
    if parsed.path.startswith("/show"):
        # path='/show/VLPLQw_XrMliWVYdCBZ-ZJcv5nvUrjQPmjyY' -> PLQw_XrMliWVYdCBZ-ZJcv5nvUrjQPmjyY
        val = parsed.path.split("/")[-1]
        val = val.removeprefix("VL")
        result["playlist_id"] = val  # type:ignore

    # /playlist contains only playlist_id
    elif parsed.path == "/playlist":
        # query='list=PLMlRYqqqM5rrjeaJuVaC6MWN7e7fSXGJt' -> PLMlRYqqqM5rrjeaJuVaC6MWN7e7fSXGJt
        val = parsed.query.removeprefix("list=")
        result["playlist_id"] = val  # type:ignore

    # /watch contain both video_id or (video_id+playlist_id)
    elif parsed.path == "/watch":
        query_dict = urllib.parse.parse_qs(parsed.query)

        result["video_id"] = query_dict["v"][0]
        if "list" in query_dict:
            playlist_id = query_dict["list"][0]

            # filter out mix playlist ids
            if not playlist_id.startswith("RD") and not playlist_id.startswith("TLGG"):
                result["playlist_id"] = query_dict["list"][0]

    return result  # type:ignore


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
