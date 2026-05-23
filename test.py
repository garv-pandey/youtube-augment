import urllib.parse
from tests.conftest import (
    YT_PLAYLISTS,
    YT_SEASON_PLAYLISTS,
    YT_VIDEO_IN_MIX_PLAYLISTS,
    YT_VIDEO_IN_PLAYLISTS,
    YT_VIDEO_IN_SEASON_PLAYLISTS,
    YT_VIDEOS,
    YTM_VIDEOS,
    YTM_PLAYLISTS,
    YTM_VIDEO_IN_PLAYLISTS,
    YTM_MIX_PLAYLISTS,
    YTM_VIDEO_IN_MIX_PLAYLISTS,
)
from ytaug.youtube import is_youtube_domain, extract_youtube_video_or_playlist_id

if __name__ == "__main__":
    for obj in [
        YT_VIDEOS[0],
        YT_PLAYLISTS[0],
        YT_VIDEO_IN_PLAYLISTS[0],
        YT_VIDEO_IN_MIX_PLAYLISTS[0],
        *YT_SEASON_PLAYLISTS,
        *YT_VIDEO_IN_SEASON_PLAYLISTS,
        YTM_VIDEOS[0],
        YTM_PLAYLISTS[0],
        YTM_VIDEO_IN_PLAYLISTS[0],
        YTM_MIX_PLAYLISTS[0],
        YTM_VIDEO_IN_MIX_PLAYLISTS[0],
    ]:
        extract_youtube_video_or_playlist_id(obj["url"])
