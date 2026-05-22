import pytest

from tests.conftest import (
    YT_PLAYLISTS,
    YT_SEASON_PLAYLISTS,
    YT_VIDEOS,
    YT_VIDEO_IN_MIX_PLAYLISTS,
    YT_VIDEO_IN_PLAYLISTS,
    YT_VIDEO_IN_SEASON_PLAYLISTS,
    YTM_MIX_PLAYLISTS,
    YTM_PLAYLISTS,
    YTM_VIDEOS,
    YTM_VIDEO_IN_MIX_PLAYLISTS,
    YTM_VIDEO_IN_PLAYLISTS,
)

from ytaug.youtube import (
    is_youtube_url,
    is_youtube_video,
    is_youtube_playlist,
    get_youtube_video_id,
    get_youtube_playlist_id,
    get_youtube_video_url,
    get_youtube_playlist_url,
)

# --- Composed lists from conftest data ---

_URLS_WITH_V_ID = [
    e
    for e in (
        YT_VIDEOS
        + YT_VIDEO_IN_PLAYLISTS
        + YT_VIDEO_IN_MIX_PLAYLISTS
        + YTM_VIDEOS
        + YTM_VIDEO_IN_PLAYLISTS
        + YTM_VIDEO_IN_MIX_PLAYLISTS
        + YT_VIDEO_IN_SEASON_PLAYLISTS
    )
    if "watch_videos" not in e["url"]
]

_URLS_WITHOUT_V_ID = (
    YT_PLAYLISTS
    + YT_SEASON_PLAYLISTS
    + [e for e in YT_VIDEO_IN_SEASON_PLAYLISTS if "watch_videos" in e["url"]]
    + YTM_PLAYLISTS
    + YTM_MIX_PLAYLISTS
)

_EDGE_NO_ID = [{"url": None}, {"url": ""}]

_PURE_PLAYLISTS = YT_PLAYLISTS + YTM_PLAYLISTS + YTM_MIX_PLAYLISTS

_NOT_PURE_PLAYLISTS = (
    YT_VIDEOS
    + YT_VIDEO_IN_PLAYLISTS
    + YT_VIDEO_IN_MIX_PLAYLISTS
    + YT_SEASON_PLAYLISTS
    + YT_VIDEO_IN_SEASON_PLAYLISTS
    + YTM_VIDEOS
    + YTM_VIDEO_IN_PLAYLISTS
    + YTM_VIDEO_IN_MIX_PLAYLISTS
)

_URLS_WITH_LIST_ID = (
    YT_PLAYLISTS
    + YT_VIDEO_IN_PLAYLISTS
    + YT_VIDEO_IN_MIX_PLAYLISTS
    + [e for e in YT_VIDEO_IN_SEASON_PLAYLISTS if "watch_videos" not in e["url"]]
    + YTM_PLAYLISTS
    + YTM_VIDEO_IN_PLAYLISTS
    + YTM_MIX_PLAYLISTS
    + YTM_VIDEO_IN_MIX_PLAYLISTS
)

_URLS_WITHOUT_LIST_ID = (
    YT_VIDEOS
    + YT_SEASON_PLAYLISTS
    + [e for e in YT_VIDEO_IN_SEASON_PLAYLISTS if "watch_videos" in e["url"]]
    + YTM_VIDEOS
)

_EDGE_NO_LIST = [{"url": None}, {"url": ""}]


@pytest.mark.unit
class TestIsYoutubeUrl:
    @pytest.mark.parametrize(
        "url",
        [
            "https://www.youtube.com/watch?v=abc",
            "https://youtube.com/watch?v=abc",
            "https://music.youtube.com/playlist?list=PL_abc",
            "https://m.youtube.com/watch?v=abc",
            "https://youtu.be/abc",
            "http://www.youtube.com/watch?v=abc",
            "youtube.com/watch?v=abc",
            "www.youtube.com/watch?v=abc",
            "YOUTUBE.COM/watch?v=abc",
            "https://YouTube.com/watch?v=abc",
        ],
    )
    def test_valid_youtube_urls(self, url):
        assert is_youtube_url(url) is True

    @pytest.mark.parametrize(
        "url",
        [
            "https://vimeo.com/123",
            "https://example.com",
            "https://evil.com?domain=youtube.com",
            "https://youtube.com.evil.com/",
            "https://youtube.comm/",
            None,
            "",
            "   ",
            "not-a-url",
            "youtube",
        ],
    )
    def test_invalid_urls(self, url):
        assert is_youtube_url(url) is False


@pytest.mark.unit
class TestIsYoutubeVideo:
    @pytest.mark.parametrize("entry", _URLS_WITH_V_ID)
    def test_valid_youtube_video_urls(self, entry):
        assert is_youtube_video(entry["url"]) is True

    @pytest.mark.parametrize("entry", [*_URLS_WITHOUT_V_ID, *_EDGE_NO_ID])
    def test_invalid_youtube_vidoe_urls(self, entry):
        assert is_youtube_video(entry["url"]) is False


@pytest.mark.unit
class TestIsYoutubePlaylist:
    @pytest.mark.parametrize("entry", _PURE_PLAYLISTS)
    def test_valid_playlist_url(self, entry):
        assert is_youtube_playlist(entry["url"]) is True

    @pytest.mark.parametrize("entry", [*_NOT_PURE_PLAYLISTS, *_EDGE_NO_ID])
    def test_invalid_playlist_url(self, entry):
        assert is_youtube_playlist(entry["url"]) is False


@pytest.mark.unit
class TestGetYoutubeVideoId:
    @pytest.mark.parametrize("entry", _URLS_WITH_V_ID)
    def test_returns_video_id(self, entry):
        assert get_youtube_video_id(entry["url"]) == entry["video_id"]

    @pytest.mark.parametrize("entry", [*_URLS_WITHOUT_V_ID, *_EDGE_NO_ID])
    def test_returns_none_when_no_video_id(self, entry):
        assert get_youtube_video_id(entry["url"]) is None


@pytest.mark.unit
class TestGetYoutubePlaylistId:
    @pytest.mark.parametrize("entry", _URLS_WITH_LIST_ID)
    def test_returns_playlist_id(self, entry):
        assert get_youtube_playlist_id(entry["url"]) == entry["playlist_id"]

    @pytest.mark.parametrize("entry", [*_URLS_WITHOUT_LIST_ID, *_EDGE_NO_LIST])
    def test_returns_none_when_no_playlist_id(self, entry):
        assert get_youtube_playlist_id(entry["url"]) is None


@pytest.mark.unit
class TestGetYoutubeVideoUrl:
    @pytest.mark.parametrize(
        "id, expected",
        [
            ("r-eKJIJXaqE", "https://www.youtube.com/watch?v=r-eKJIJXaqE"),
            ("abc", "https://www.youtube.com/watch?v=abc"),
            ("", "https://www.youtube.com/watch?v="),
        ],
    )
    def test_returns_url(self, id, expected):
        assert get_youtube_video_url(id) == expected


@pytest.mark.unit
class TestGetYoutubePlaylistUrl:
    @pytest.mark.parametrize(
        "id, expected",
        [
            (
                "PLp9koScqE_BHhGcIrUuGmeCPRakLF-eY8",
                "https://www.youtube.com/playlist?list=PLp9koScqE_BHhGcIrUuGmeCPRakLF-eY8",
            ),
            (
                "RDCLAK5uy_n38QBvlkETFzw_TX8Z7wfA733kKr2vo0o",
                "https://www.youtube.com/playlist?list=RDCLAK5uy_n38QBvlkETFzw_TX8Z7wfA733kKr2vo0o",
            ),
            ("", "https://www.youtube.com/playlist?list="),
        ],
    )
    def test_returns_url(self, id, expected):
        assert get_youtube_playlist_url(id) == expected
