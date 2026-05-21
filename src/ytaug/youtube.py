import urllib


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


def is_youtube_video(url: str | None) -> bool:
    pass


def is_youtube_playlist(url: str | None) -> bool:
    pass


def get_youtube_playlist_id(url: str | None) -> str | None:
    pass


def get_youtube_video_id(url: str | None) -> str | None:
    pass


def get_youtube_video_url(id: str | None) -> str:
    pass


def get_youtube_playlist_url(id: str | None) -> str:
    pass
