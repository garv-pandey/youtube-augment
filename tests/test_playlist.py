import pytest
from unittest.mock import patch

from ytaug.exceptions import YTAugError
from ytaug.playlist import (
    extract_playlist_id,
    get_playlist_info_dlp,
    get_video_ids,
    is_youtube_playlist,
)


class TestIsYouTubePlaylist:
    """is_youtube_playlist() — checks if a URL is a YouTube/YouTube Music playlist."""

    def test_standard_playlist_url(self):
        assert (
            is_youtube_playlist("https://www.youtube.com/playlist?list=PL_abc123")
            is True
        )

    def test_music_playlist_url(self):
        assert (
            is_youtube_playlist("https://music.youtube.com/playlist?list=PL_abc123")
            is True
        )

    def test_no_subdomain_playlist_url(self):
        assert (
            is_youtube_playlist("https://youtube.com/playlist?list=PL_abc123") is True
        )

    def test_video_with_list_param_returns_false(self):
        assert (
            is_youtube_playlist("https://www.youtube.com/watch?v=abc&list=PL_abc")
            is False
        )

    def test_regular_video_url_returns_false(self):
        assert is_youtube_playlist("https://www.youtube.com/watch?v=abc") is False

    def test_non_youtube_domain_returns_false(self):
        assert is_youtube_playlist("https://vimeo.com/123") is False

    def test_playlist_path_no_list_param_returns_false(self):
        assert is_youtube_playlist("https://www.youtube.com/playlist") is False

    def test_root_url_returns_false(self):
        assert is_youtube_playlist("https://www.youtube.com/") is False

    def test_wrong_domain_playlist_returns_false(self):
        assert is_youtube_playlist("https://www.youtub.com/playlist?list=abc") is False

    def test_empty_string_returns_false(self):
        assert is_youtube_playlist("") is False

    def test_youtube_short_url_returns_false(self):
        assert is_youtube_playlist("https://youtu.be/abc") is False

    def test_youtube_short_url_with_list_returns_false(self):
        assert is_youtube_playlist("https://youtu.be/abc?list=PL_abc") is False

    def test_music_video_with_list_returns_false(self):
        assert (
            is_youtube_playlist("https://music.youtube.com/watch?v=abc&list=PL_abc")
            is False
        )


class TestExtractPlaylistId:
    """extract_playlist_id() — extracts the 'list' query param from a URL."""

    def test_standard_playlist(self):
        assert (
            extract_playlist_id("https://www.youtube.com/playlist?list=PL_abc123")
            == "PL_abc123"
        )

    def test_music_playlist(self):
        assert (
            extract_playlist_id("https://music.youtube.com/playlist?list=PL_music123")
            == "PL_music123"
        )

    def test_video_with_list_param(self):
        assert (
            extract_playlist_id("https://www.youtube.com/watch?v=abc&list=PL_xyz")
            == "PL_xyz"
        )

    def test_short_url_with_list_param(self):
        assert extract_playlist_id("https://youtu.be/abc?list=PL_short") == "PL_short"

    def test_multiple_list_params_returns_first(self):
        assert (
            extract_playlist_id(
                "https://www.youtube.com/playlist?list=PL_first&list=PL_second"
            )
            == "PL_first"
        )

    def test_none_youtube_domain_with_list_param(self):
        assert extract_playlist_id("https://vimeo.com/video?list=abc123") == "abc123"

    def test_no_list_param_raises_ytaugerror(self):
        with pytest.raises(YTAugError):
            extract_playlist_id("https://www.youtube.com/watch?v=abc")

    def test_no_query_params_raises_ytaugerror(self):
        with pytest.raises(YTAugError):
            extract_playlist_id("https://www.youtube.com/playlist")

    def test_empty_string_raises_ytaugerror(self):
        with pytest.raises(YTAugError):
            extract_playlist_id("")

    def test_root_url_raises_ytaugerror(self):
        with pytest.raises(YTAugError):
            extract_playlist_id("https://www.youtube.com/")


JS_RUNTIME = {"runtime": {"path": "/usr/bin/deno"}}
BASE_INFO = {
    "uploader_id": "@ChannelName",
    "id": "PL_abc123",
    "title": "My Playlist",
    "description": "A test playlist",
    "playlist_count": 10,
    "entries": [{"id": f"vid{i}"} for i in range(10)],
    "availability": "public",
    "_type": "playlist",
}


class TestGetPlaylistInfoDlp:
    """get_playlist_info_dlp() — fetches playlist metadata via yt-dlp."""

    def test_standard_playlist(self):
        with patch("ytaug.playlist.yt_dlp.YoutubeDL") as mock_ydl:
            mock_ydl.return_value.__enter__.return_value.extract_info.return_value = (
                BASE_INFO
            )

            result = get_playlist_info_dlp(
                "https://youtube.com/playlist?list=PL_abc123", JS_RUNTIME
            )

        assert result == {
            "owner_channel_id": "@ChannelName",
            "id": "PL_abc123",
            "title": "My Playlist",
            "description": "A test playlist",
            "video_count": 10,
            "privacy_status": "public",
            "is_playlist": True,
        }

    def test_missing_optional_fields(self):
        info = {
            "id": "PL_abc",
            "title": "Minimal",
            "playlist_count": 1,
            "entries": [{"id": "vid1"}],
            "_type": "playlist",
        }
        with patch("ytaug.playlist.yt_dlp.YoutubeDL") as mock_ydl:
            mock_ydl.return_value.__enter__.return_value.extract_info.return_value = (
                info
            )

            result = get_playlist_info_dlp(
                "https://youtube.com/playlist?list=PL_abc", JS_RUNTIME
            )

        assert result["owner_channel_id"] is None
        assert result["description"] is None
        assert result["privacy_status"] is None

    def test_video_count_from_entries_when_playlist_count_missing(self):
        info = {
            "id": "PL_abc",
            "title": "Test",
            "entries": [{"id": f"vid{i}"} for i in range(5)],
            "_type": "playlist",
        }
        with patch("ytaug.playlist.yt_dlp.YoutubeDL") as mock_ydl:
            mock_ydl.return_value.__enter__.return_value.extract_info.return_value = (
                info
            )

            result = get_playlist_info_dlp(
                "https://youtube.com/playlist?list=PL_abc", JS_RUNTIME
            )

        assert result["video_count"] == 5

    def test_video_count_prefers_playlist_count(self):
        info = dict(BASE_INFO)
        info["playlist_count"] = 10
        info["entries"] = [{"id": f"vid{i}"} for i in range(3)]
        with patch("ytaug.playlist.yt_dlp.YoutubeDL") as mock_ydl:
            mock_ydl.return_value.__enter__.return_value.extract_info.return_value = (
                info
            )

            result = get_playlist_info_dlp(
                "https://youtube.com/playlist?list=PL_abc", JS_RUNTIME
            )

        assert result["video_count"] == 10

    def test_private_playlist_raises_ytaugerror(self):
        with patch("ytaug.playlist.yt_dlp.YoutubeDL") as mock_ydl:
            mock_ydl.return_value.__enter__.return_value.extract_info.side_effect = (
                Exception("This playlist is private")
            )

            with pytest.raises(YTAugError, match="Provided playlist is private"):
                get_playlist_info_dlp(
                    "https://youtube.com/playlist?list=PL_abc", JS_RUNTIME
                )

    def test_other_ytdlp_error_raises_ytaugerror(self):
        with patch("ytaug.playlist.yt_dlp.YoutubeDL") as mock_ydl:
            mock_ydl.return_value.__enter__.return_value.extract_info.side_effect = (
                Exception("Network error")
            )

            with pytest.raises(YTAugError, match="Error in get_playlist_info_dlp"):
                get_playlist_info_dlp(
                    "https://youtube.com/playlist?list=PL_abc", JS_RUNTIME
                )

    def test_not_a_playlist_raises_ytaugerror(self):
        info = dict(BASE_INFO)
        info["_type"] = "video"
        with patch("ytaug.playlist.yt_dlp.YoutubeDL") as mock_ydl:
            mock_ydl.return_value.__enter__.return_value.extract_info.return_value = (
                info
            )

            with pytest.raises(
                YTAugError, match="Provided URL is not a youtube palylist"
            ):
                get_playlist_info_dlp("https://youtube.com/watch?v=abc", JS_RUNTIME)

    def test_youtubedl_constructor_fails_raises_ytaugerror(self):
        with patch("ytaug.playlist.yt_dlp.YoutubeDL") as mock_ydl_cls:
            mock_ydl_cls.side_effect = Exception("Init error")
            with pytest.raises(YTAugError, match="Error in get_playlist_info_dlp"):
                get_playlist_info_dlp(
                    "https://youtube.com/playlist?list=PL_abc", JS_RUNTIME
                )


class TestGetVideoIds:
    """get_video_ids() — extracts video IDs from a playlist via yt-dlp."""

    def test_multiple_entries(self):
        result = {"entries": [{"id": "vid1"}, {"id": "vid2"}, {"id": "vid3"}]}
        with patch("ytaug.playlist.yt_dlp.YoutubeDL") as mock_ydl:
            mock_ydl.return_value.__enter__.return_value.extract_info.return_value = (
                result
            )

            ids = get_video_ids("https://youtube.com/playlist?list=PL_abc")

        assert ids == ["vid1", "vid2", "vid3"]

    def test_single_entry(self):
        result = {"entries": [{"id": "vid1"}]}
        with patch("ytaug.playlist.yt_dlp.YoutubeDL") as mock_ydl:
            mock_ydl.return_value.__enter__.return_value.extract_info.return_value = (
                result
            )

            ids = get_video_ids("https://youtube.com/playlist?list=PL_abc")

        assert ids == ["vid1"]

    def test_no_entries_key(self):
        result = {"id": "PL_abc", "title": "Empty"}
        with patch("ytaug.playlist.yt_dlp.YoutubeDL") as mock_ydl:
            mock_ydl.return_value.__enter__.return_value.extract_info.return_value = (
                result
            )

            ids = get_video_ids("https://youtube.com/playlist?list=PL_abc")

        assert ids == []

    def test_entries_contain_none(self):
        result = {"entries": [{"id": "vid1"}, None, {"id": "vid3"}]}
        with patch("ytaug.playlist.yt_dlp.YoutubeDL") as mock_ydl:
            mock_ydl.return_value.__enter__.return_value.extract_info.return_value = (
                result
            )

            ids = get_video_ids("https://youtube.com/playlist?list=PL_abc")

        assert ids == ["vid1", "vid3"]

    def test_entries_missing_id(self):
        result = {"entries": [{"id": "vid1"}, {"foo": "bar"}, {"id": "vid3"}]}
        with patch("ytaug.playlist.yt_dlp.YoutubeDL") as mock_ydl:
            mock_ydl.return_value.__enter__.return_value.extract_info.return_value = (
                result
            )

            ids = get_video_ids("https://youtube.com/playlist?list=PL_abc")

        assert ids == ["vid1", "vid3"]

    def test_all_entries_invalid(self):
        result = {"entries": [None, {"foo": "bar"}, None]}
        with patch("ytaug.playlist.yt_dlp.YoutubeDL") as mock_ydl:
            mock_ydl.return_value.__enter__.return_value.extract_info.return_value = (
                result
            )

            ids = get_video_ids("https://youtube.com/playlist?list=PL_abc")

        assert ids == []

    def test_extract_info_error_raises_ytaugerror(self):
        with patch("ytaug.playlist.yt_dlp.YoutubeDL") as mock_ydl:
            mock_ydl.return_value.__enter__.return_value.extract_info.side_effect = (
                Exception("Network error")
            )

            with pytest.raises(YTAugError, match="Error in get_vidoe_ids"):
                get_video_ids("https://youtube.com/playlist?list=PL_abc")
