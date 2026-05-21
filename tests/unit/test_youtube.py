import pytest

from ytaug.youtube import (
    is_youtube_url,
    is_youtube_video,
    is_youtube_playlist,
    get_youtube_video_id,
    get_youtube_playlist_id,
    get_youtube_video_url,
    get_youtube_playlist_url,
)

# TODO: find a better way to reuse urls instead of copy pasting
# TODO: add youtube shorts url tests as well


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
    @pytest.mark.parametrize(
        "url",
        [
            "https://www.youtube.com/watch?v=r-eKJIJXaqE",  # yt vid
            "https://www.youtube.com/watch?v=r-eKJIJXaqE&list=PLp9koScqE_BHhGcIrUuGmeCPRakLF-eY8&index=12"  # yt vid in playlist
            "https://www.youtube.com/watch?v=r-eKJIJXaqE&list=RDEMUQ4DWIcNHr2I0idrfXNfEw&start_radio=1",  # yt vid in mix playlist
            "https://music.youtube.com/watch?v=r-eKJIJXaqE",  # ytm vid
            "https://music.youtube.com/watch?v=r-eKJIJXaqE&list=PLp9koScqE_BHhGcIrUuGmeCPRakLF-eY8",  # ytm vid in playlist
            "https://music.youtube.com/watch?v=vMFnGUXVMZY&list=RDCLAK5uy_n38QBvlkETFzw_TX8Z7wfA733kKr2vo0o",  # ytm vid in mix/recomended playlist
        ],
    )
    def test_valid_youtube_video_urls(self, url):
        assert is_youtube_video(url) is True

    @pytest.mark.parametrize(
        "url",
        [
            "https://www.youtube.com/playlist?list=PLp9koScqE_BHhGcIrUuGmeCPRakLF-eY8",  # yt playlist
            "https://music.youtube.com/playlist?list=PLp9koScqE_BHhGcIrUuGmeCPRakLF-eY8",  # ytm playlist
            "https://music.youtube.com/playlist?list=RDCLAK5uy_n38QBvlkETFzw_TX8Z7wfA733kKr2vo0o",  # ytm mix/recomended playlist
            "",
            None,
        ],
    )
    def test_invalid_youtube_vidoe_urls(self, url):
        assert is_youtube_video(url) is False


@pytest.mark.unit
class TestIsYoutubePlaylist:
    @pytest.mark.parametrize(
        "url",
        [
            "https://www.youtube.com/playlist?list=PLp9koScqE_BHhGcIrUuGmeCPRakLF-eY8",  # yt playlist
            "https://music.youtube.com/playlist?list=PLp9koScqE_BHhGcIrUuGmeCPRakLF-eY8",  # ytm playlist
            "https://music.youtube.com/playlist?list=RDCLAK5uy_n38QBvlkETFzw_TX8Z7wfA733kKr2vo0o",  # ytm mix/recomended playlist
        ],
    )
    def test_valid_playlist_url(self, url):
        assert is_youtube_playlist(url) is True

    @pytest.mark.parametrize(
        "url",
        [
            "https://www.youtube.com/watch?v=r-eKJIJXaqE",  # yt vid
            "https://www.youtube.com/watch?v=r-eKJIJXaqE&list=PLp9koScqE_BHhGcIrUuGmeCPRakLF-eY8&index=12",  # yt vid in playlist
            "https://www.youtube.com/watch?v=r-eKJIJXaqE&list=RDEMUQ4DWIcNHr2I0idrfXNfEw&start_radio=1",  # yt vid in mix playlist
            "https://music.youtube.com/watch?v=r-eKJIJXaqE",  # ytm vid
            "https://music.youtube.com/watch?v=r-eKJIJXaqE&list=PLp9koScqE_BHhGcIrUuGmeCPRakLF-eY8",  # ytm vid in playlist
            "https://music.youtube.com/watch?v=vMFnGUXVMZY&list=RDCLAK5uy_n38QBvlkETFzw_TX8Z7wfA733kKr2vo0o",  # ytm vid in mix/recomended playlist
            "",
            None,
        ],
    )
    def test_invalid_playlist_url(self, url):
        assert is_youtube_playlist(url) is False


@pytest.mark.unit
class TestGetYoutubeVideoId:
    @pytest.mark.parametrize(
        "url, expected",
        [
            ("https://www.youtube.com/watch?v=r-eKJIJXaqE", "r-eKJIJXaqE"),  # yt vid
            (
                "https://www.youtube.com/watch?v=r-eKJIJXaqE&list=PLp9koScqE_BHhGcIrUuGmeCPRakLF-eY8&index=12",
                "r-eKJIJXaqE",
            ),  # yt vid in playlist
            (
                "https://www.youtube.com/watch?v=r-eKJIJXaqE&list=RDEMUQ4DWIcNHr2I0idrfXNfEw&start_radio=1",
                "r-eKJIJXaqE",
            ),  # yt vid in mix playlist
            ("https://music.youtube.com/watch?v=r-eKJIJXaqE", "r-eKJIJXaqE"),  # ytm vid
            (
                "https://music.youtube.com/watch?v=r-eKJIJXaqE&list=PLp9koScqE_BHhGcIrUuGmeCPRakLF-eY8",
                "r-eKJIJXaqE",
            ),  # ytm vid in playlist
            (
                "https://music.youtube.com/watch?v=vMFnGUXVMZY&list=RDCLAK5uy_n38QBvlkETFzw_TX8Z7wfA733kKr2vo0o",
                "vMFnGUXVMZY",
            ),  # ytm vid in mix/recomended playlist
        ],
    )
    def test_returns_video_id(self, url, expected):
        assert get_youtube_video_id(url) == expected

    @pytest.mark.parametrize(
        "url",
        [
            "https://www.youtube.com/playlist?list=PLp9koScqE_BHhGcIrUuGmeCPRakLF-eY8",  # yt playlist
            "https://music.youtube.com/playlist?list=PLp9koScqE_BHhGcIrUuGmeCPRakLF-eY8",  # ytm playlist
            "https://music.youtube.com/playlist?list=RDCLAK5uy_n38QBvlkETFzw_TX8Z7wfA733kKr2vo0o",  # ytm mix/recomended playlist
            None,
            "",
        ],
    )
    def test_returns_none_when_no_video_id(self, url):
        assert get_youtube_video_id(url) is None


@pytest.mark.unit
class TestGetYoutubePlaylistId:
    @pytest.mark.parametrize(
        "url, expected",
        [
            (
                "https://www.youtube.com/playlist?list=PLp9koScqE_BHhGcIrUuGmeCPRakLF-eY8",
                "PLp9koScqE_BHhGcIrUuGmeCPRakLF-eY8",
            ),  # yt playlist
            (
                "https://www.youtube.com/watch?v=r-eKJIJXaqE&list=PLp9koScqE_BHhGcIrUuGmeCPRakLF-eY8&index=12",
                "PLp9koScqE_BHhGcIrUuGmeCPRakLF-eY8",
            ),  # yt vid in playlist
            (
                "https://www.youtube.com/watch?v=r-eKJIJXaqE&list=RDEMUQ4DWIcNHr2I0idrfXNfEw&start_radio=1",
                "RDEMUQ4DWIcNHr2I0idrfXNfEw",
            ),  # yt vid in mix playlist
            (
                "https://music.youtube.com/playlist?list=PLp9koScqE_BHhGcIrUuGmeCPRakLF-eY8",
                "PLp9koScqE_BHhGcIrUuGmeCPRakLF-eY8",
            ),  # ytm playlist
            (
                "https://music.youtube.com/watch?v=r-eKJIJXaqE&list=PLp9koScqE_BHhGcIrUuGmeCPRakLF-eY8",
                "PLp9koScqE_BHhGcIrUuGmeCPRakLF-eY8",
            ),  # ytm vid in playlist
            (
                "https://music.youtube.com/playlist?list=RDCLAK5uy_n38QBvlkETFzw_TX8Z7wfA733kKr2vo0o",
                "RDCLAK5uy_n38QBvlkETFzw_TX8Z7wfA733kKr2vo0o",
            ),  # ytm mix playlist
            (
                "https://music.youtube.com/watch?v=vMFnGUXVMZY&list=RDCLAK5uy_n38QBvlkETFzw_TX8Z7wfA733kKr2vo0o",
                "RDCLAK5uy_n38QBvlkETFzw_TX8Z7wfA733kKr2vo0o",
            ),  # ytm vid in mix/recomended playlist
        ],
    )
    def test_returns_playlist_id(self, url, expected):
        assert get_youtube_playlist_id(url) == expected

    @pytest.mark.parametrize(
        "url",
        [
            "https://www.youtube.com/watch?v=r-eKJIJXaqE",  # yt vid
            "https://music.youtube.com/watch?v=r-eKJIJXaqE",  # ytm vid
            None,
            "",
        ],
    )
    def test_returns_none_when_no_playlist_id(self, url):
        assert get_youtube_playlist_id(url) is None


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


# mix video in paylist yt : https://www.youtube.com/watch?v=r-eKJIJXaqE&list=RDEMUQ4DWIcNHr2I0idrfXNfEw&start_radio=1
# mix playlist yt: cant get
# playlist yt: https://www.youtube.com/playlist?list=PLp9koScqE_BHhGcIrUuGmeCPRakLF-eY8
# video yt: https://www.youtube.com/watch?v=r-eKJIJXaqE
# video ytm: https://music.youtube.com/watch?v=r-eKJIJXaqE
# playlist ytm: https://music.youtube.com/playlist?list=PLp9koScqE_BHhGcIrUuGmeCPRakLF-eY8
# video in paylist ytm: https://music.youtube.com/watch?v=r-eKJIJXaqE&list=PLp9koScqE_BHhGcIrUuGmeCPRakLF-eY8
# recom playlist ytm: https://music.youtube.com/playlist?list=RDCLAK5uy_n38QBvlkETFzw_TX8Z7wfA733kKr2vo0o
# recom video in playlist ytm: https://music.youtube.com/watch?v=vMFnGUXVMZY&list=RDCLAK5uy_n38QBvlkETFzw_TX8Z7wfA733kKr2vo0o
# mix/radio playlists contains RD before the playlist id
# special browse/ abstract of ytm for playlists
