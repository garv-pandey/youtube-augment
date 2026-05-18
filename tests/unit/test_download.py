import pytest
from pathlib import Path
from ytaug.download import (
    download_url_ytdlp,
    has_js_runtime,
    is_youtube_url,
    get_url_info_ytdlp,
    get_ytdlp_js_runtime_config,
)
from ytaug.exceptions import YTAugError


# TestHasFfmpeg
# TestGetFfmpegInstallInstructions
# TestGetJsRuntimeInstallInstructions
# simple functions, doesnt require tests


@pytest.mark.unit
class TestHasJsRuntime:
    """check_js_runtime() — searches for deno, falls back to node."""

    def test_deno_found(self, mocker):
        mock_which = mocker.patch("ytaug.download.shutil.which")
        mock_which.return_value = "/usr/bin/deno"

        assert has_js_runtime() is True

    def test_deno_missing_node_found(self, mocker):
        mock_which = mocker.patch("ytaug.download.shutil.which")
        mock_which.side_effect = [None, "/usr/bin/node"]

        assert has_js_runtime() is True

    def test_node_missing_deno_found(self, mocker):
        mock_which = mocker.patch("ytaug.download.shutil.which")
        mock_which.side_effect = ["/usr/bin/deno", None]

        assert has_js_runtime() is True

    def test_none_found(self, mocker):
        mock_which = mocker.patch("ytaug.download.shutil.which")
        mock_which.return_value = None

        assert has_js_runtime() is False


@pytest.mark.unit
class TestGetYtdlpJsRuntimeConfig:
    """get_ytdlp_js_runtime_config() — collects all found JS runtimes into a dict."""

    def test_returns_both_runtimes(self, mocker):
        mock_which = mocker.patch("ytaug.download.shutil.which")
        mock_which.side_effect = ["/usr/bin/deno", "/usr/bin/node"]

        config = get_ytdlp_js_runtime_config()
        assert config == {
            "deno": {"path": "/usr/bin/deno"},
            "node": {"path": "/usr/bin/node"},
        }

    def test_returns_only_deno(self, mocker):
        mock_which = mocker.patch("ytaug.download.shutil.which")
        mock_which.side_effect = ["/usr/bin/deno", None]

        assert get_ytdlp_js_runtime_config() == {"deno": {"path": "/usr/bin/deno"}}

    def test_returns_only_node(self, mocker):
        mock_which = mocker.patch("ytaug.download.shutil.which")
        mock_which.side_effect = [None, "/usr/bin/node"]

        assert get_ytdlp_js_runtime_config() == {"node": {"path": "/usr/bin/node"}}

    def test_returns_empty_dict_when_none_found(self, mocker):
        mock_which = mocker.patch("ytaug.download.shutil.which")
        mock_which.return_value = None

        assert get_ytdlp_js_runtime_config() == {}


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
class TestGetUrlInfoYtdlp:
    """get_url_info_ytdlp() — extracts metadata from URLs via yt-dlp."""

    def test_returns_video_info(self, mocker):
        mock_ydl = mocker.patch("ytaug.download.yt_dlp.YoutubeDL")
        mock_instance = mock_ydl.return_value.__enter__.return_value
        # __enter__.return_value maps to "with ... as ydl" is actual code
        mock_instance.extract_info.return_value = {
            "_type": "video",
            "title": "Test Video",
            "id": "abc123",
        }

        result = get_url_info_ytdlp("https://youtube.com/watch?v=abc123", {})

        assert result == {"type": "video", "title": "Test Video", "id": "abc123"}

    def test_returns_playlist_info(self, mocker):
        mock_ydl = mocker.patch("ytaug.download.yt_dlp.YoutubeDL")
        mock_instance = mock_ydl.return_value.__enter__.return_value
        mock_instance.extract_info.return_value = {
            "_type": "playlist",
            "title": "Test Playlist",
            "id": "PL_abc",
            "playlist_count": 10,
        }

        result = get_url_info_ytdlp("https://youtube.com/playlist?list=PL_abc", {})

        assert result == {
            "type": "playlist",
            "title": "Test Playlist",
            "id": "PL_abc",
            "video_count": 10,
        }

    def test_raises_on_private(self, mocker):
        mock_ydl = mocker.patch("ytaug.download.yt_dlp.YoutubeDL")
        mock_instance = mock_ydl.return_value.__enter__.return_value
        mock_instance.extract_info.side_effect = Exception("This video is private")

        with pytest.raises(YTAugError, match="Provided url is private"):
            get_url_info_ytdlp("https://youtube.com/watch?v=abc", {})

    def test_raises_on_other_error(self, mocker):
        mock_ydl = mocker.patch("ytaug.download.yt_dlp.YoutubeDL")
        mock_instance = mock_ydl.return_value.__enter__.return_value
        mock_instance.extract_info.side_effect = Exception("Network error")

        with pytest.raises(YTAugError):
            get_url_info_ytdlp("https://youtube.com/watch?v=abc", {})


@pytest.mark.unit
class TestDownloadUrlYtdlp:
    """download_url_ytdlp() — downloads audio from a URL via yt-dlp."""

    def test_sets_playlist_subfolder(self, mocker, tmp_path):
        mock_ydl = mocker.patch("ytaug.download.yt_dlp.YoutubeDL")

        download_url_ytdlp(
            "https://youtube.com/playlist?list=PL_abc",
            tmp_path,
            is_playlist=True,
            js_runtime_config={"deno": {"path": "/usr/bin/deno"}},
        )

        # gets the first passed argument to the mock which is ydl_opts
        call_args = mock_ydl.call_args[0][0]
        outtmpl = call_args["outtmpl"]
        assert "%(playlist_title)s" in outtmpl
        assert outtmpl.startswith(str(tmp_path))

    def test_raises_on_failure(self, mocker, tmp_path):
        mock_ydl = mocker.patch("ytaug.download.yt_dlp.YoutubeDL")
        mock_ydl.return_value.__enter__.return_value.download.side_effect = Exception(
            "yt-dlp error"
        )

        with pytest.raises(YTAugError):
            download_url_ytdlp(
                "https://youtube.com/watch?v=abc",
                tmp_path,
                is_playlist=False,
                js_runtime_config={},
            )
