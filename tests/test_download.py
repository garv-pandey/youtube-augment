import pytest
from unittest.mock import patch
from ytaug.download import (
    check_ffmpeg,
    check_js_runtime,
    download_playlist,
    get_playlist_info_dlp,
    get_ytdlp_js_runtime_config,
)
from ytaug.exceptions import YTAugError


class TestCheckFfmpeg:
    def test_ffmpeg_found(self):
        pass

    def test_ffmpeg_not_found(self):
        pass


# TestGetFfmpegInstallInstructions
# TestGetJsRuntimeInstallInstructions
# simple functions, doesnt require tests


class TestCheckJsRuntime:
    """check_js_runtime() — searches for deno, falls back to node."""

    def test_deno_found(self, mocker):
        mock_which = mocker.patch("ytaug.download.shutil.which")
        mock_which.return_value = "/usr/bin/deno"

        assert check_js_runtime() is True

    def test_deno_missing_node_found(self, mocker):
        mock_which = mocker.patch("ytaug.download.shutil.which")
        mock_which.side_effect = [None, "/usr/bin/node"]

        assert check_js_runtime() is True

    def test_none_found(self, mocker):
        mock_which = mocker.patch("ytaug.download.shutil.which")
        mock_which.return_value = None

        assert check_js_runtime() is False


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


class TestGetPlaylistInfoDlp:
    def test_standard_playlist(self):
        pass

    def test_missing_optional_fields(self):
        pass

    def test_video_count_from_entries_when_playlist_count_missing(self):
        pass

    def test_video_count_prefers_playlist_count(self):
        pass

    def test_private_playlist_raises_ytaugerror(self):
        pass

    def test_other_ytdlp_error_raises_ytaugerror(self):
        pass

    def test_not_a_playlist_raises_ytaugerror(self):
        pass

    def test_youtubedl_constructor_fails_raises_ytaugerror(self):
        pass


class TestDownloadPlaylist:
    def test_success(self):
        pass

    def test_failure_raises_ytaugerror(self):
        pass
