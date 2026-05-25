import pytest

from tests.conftest import (
    YT_VIDEOS,
    YT_PLAYLISTS,
    YT_VIDEO_IN_PLAYLISTS,
    YT_VIDEO_IN_MIX_PLAYLISTS,
    YT_SEASON_PLAYLISTS,
    YT_VIDEO_IN_SEASON_PLAYLISTS,
    YTM_VIDEOS,
    YTM_PLAYLISTS,
    YTM_VIDEO_IN_PLAYLISTS,
    YTM_MIX_PLAYLISTS,
    YTM_VIDEO_IN_MIX_PLAYLISTS,
    EDGE_URLS,
)

from ytaug.youtube import (
    is_youtube_domain,
    extract_youtube_video_and_playlist_id,
    get_youtube_video_url,
    get_youtube_playlist_url,
)


@pytest.mark.unit
class TestIsYoutubeDomain:
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
        assert is_youtube_domain(url) is True

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
        assert is_youtube_domain(url) is False

    test_urls = []


@pytest.mark.unit
class TestExtractYoutubeVideoOrPlaylistId:
    test_url_objs = [
        *YT_VIDEOS,
        *YT_PLAYLISTS,
        *YT_VIDEO_IN_PLAYLISTS,
        *YT_VIDEO_IN_MIX_PLAYLISTS,
        *YT_SEASON_PLAYLISTS,
        *YT_VIDEO_IN_SEASON_PLAYLISTS,
        *YTM_VIDEOS,
        *YTM_PLAYLISTS,
        *YTM_VIDEO_IN_PLAYLISTS,
        *YTM_MIX_PLAYLISTS,
        *YTM_VIDEO_IN_MIX_PLAYLISTS,
        *EDGE_URLS,
    ]

    @pytest.mark.parametrize("url_obj", test_url_objs)
    def test_extract_youtube_video_and_playlist_id(self, url_obj):
        url = url_obj["url"]

        result = extract_youtube_video_and_playlist_id(url)
        assert url_obj["video_id"] == result["video_id"]
        assert url_obj["playlist_id"] == result["playlist_id"]


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
