import yt_dlp
from urllib.parse import urlparse, parse_qs
from ytmm.exceptions import YTMMError


def is_youtube_playlist(url: str) -> bool:
    """
    Checks if a given URL is a YouTube or YouTube Music playlist.

    Args:
        url: The string URL to check.

    Returns:
        bool: True if it's a playlist, False otherwise.
    """
    parsed_url = urlparse(url)

    # Check for standard YouTube and YouTube Music domains
    domain = parsed_url.netloc
    if domain not in ["www.youtube.com", "music.youtube.com", "youtube.com"]:
        return False

    # Extract query parameters (e.g., ?v=abc&list=xyz)
    query_params = parse_qs(parsed_url.query)
    # A URL is a playlist if it contains the 'list' parameter
    # AND (it's on the /playlist path OR it's a video within a playlist)
    if parsed_url.path == "/playlist" and "list" in query_params:
        return True

    return False


def extract_playlist_id(url: str) -> str:
    """
    Parses a YouTube/YouTube Music URL and extracts the 'list' ID.
    Handles main site, music subdomain, and short links.
    """

    parsed_url = urlparse(url)

    # Extract query
    query_params = parse_qs(parsed_url.query)
    playlist_id_list = query_params.get("list")

    if not playlist_id_list:
        raise YTMMError(f"couldent extract playlist_id for: {url}")
    # Return the first item if it exists, otherwise None
    return playlist_id_list[0]


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
            raise YTMMError("Provided playlist is private") from e

        raise YTMMError("Error in get_playlist_info_dlp") from e

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
        raise YTMMError("Provided URL is not a youtube palylist")

    return playlist_info


def get_video_ids(playlist_url) -> list[str]:
    """
    Uses yt-dlp to extract all video IDs from a playlist.
    Works for YouTube and YouTube Music (including Mixes).
    """

    ydl_opts = {
        "extract_flat": True,  # Do not download videos, just get metadata
        "quiet": True,  # Suppress terminal output
        "no_warnings": True,
        "ignoreerrors": True,  # Skip private/deleted videos in the list
    }

    video_ids = []

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            # extract_info returns a dict of the playlist metadata
            result = ydl.extract_info(playlist_url, download=False)

            if "entries" in result:
                for entry in result["entries"]:
                    if entry and "id" in entry:
                        video_ids.append(entry["id"])

        except Exception as e:
            raise YTMMError("Error in get_vidoe_ids") from e

    return video_ids


# def get_playlist_info_yt(playlist_url: str, credentials: Credentials):
#     """
#     Checks if a playlist is Public, Unlisted, or Private/Inaccessible.
#     """
#
#     youtube = discovery.build("youtube", "v3", credentials=credentials)
#
#     try:
#         request = youtube.playlists().list(
#             part="status,snippet,contentDetails", id=_extract_playlist_id(playlist_url)
#         )
#         response = request.execute()
#
#         if not response.get("items"):
#             return None
#
#         privacy_status = response["items"][0]["status"]["privacyStatus"]
#         title = response["items"][0]["snippet"]["title"]
#         description = response["items"][0]["snippet"]["description"]
#         video_count = response["items"][0]["contentDetails"]["itemCount"]
#
#         return {
#             "privacy_status": privacy_status,
#             "title": title,
#             "description": description,
#             "video_count": video_count,
#         }
#
#     except errors.HttpError as e:
#         print(e)
#         return None
