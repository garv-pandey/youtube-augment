from os import path
import pytest
from unittest.mock import patch
from ytaug.download import (
    check_ffmpeg,
    download_playlist,
    get_ffmpeg_install_instructions,
    get_js_runtime,
    get_js_runtime_install_instructions,
    get_playlist_info_dlp,
)
from ytaug.exceptions import YTAugError, SystemRequirementError


class TestCheckFfmpeg:
    def test_ffmpeg_found(self):
        pass

    def test_ffmpeg_not_found(self):
        pass


class TestGetFfmpegInstallInstructions:
    def test_get_ffmpeg_install_instructions_windows(self):
        with patch("ytaug.download.platform.system", return_value="Windows"):
            assert (
                get_ffmpeg_install_instructions()
                == "winget install ffmpeg \nor check their website: https://ffmpeg.org"
            )

    def test_get_ffmpeg_install_instructions_macos(self):
        with patch("ytaug.download.platform.system", return_value="Darwin"):
            assert (
                get_ffmpeg_install_instructions()
                == "brew install ffmpeg \nor check their website: https://ffmpeg.org"
            )

    def test_get_ffmpeg_install_instructions_linux(self):
        with patch("ytaug.download.platform.system", return_value="Linux"):
            assert (
                get_ffmpeg_install_instructions()
                == "sudo apt install ffmpeg (Debian/Ubuntu) \nor sudo dnf install ffmpeg (Fedora) \nor check their website: https://ffmpeg.org"
            )

    def test_get_ffmpeg_install_instructions_undefined(self):
        with patch("ytaug.download.platform.system", return_value="unknown_abcd"):
            assert (
                get_ffmpeg_install_instructions()
                == "check their website for download instructions \nhttps://ffmpeg.org"
            )


class TestGetJsRuntime:
    def test_get_js_runtime_deno(self):
        pass

    def test_get_js_runtime_node(self):
        pass

    def test_get_js_runtime_none(self):
        pass


class TestGetJsRuntimeInstallInstructions:
    def test_windows(self):
        with patch("ytaug.download.platform.system", return_value="Windows"):
            assert (
                get_js_runtime_install_instructions()
                == "winget install deno  OR  winget install OpenJS.NodeJS \nor check their website: \nhttps://deno.com OR https://nodejs.org"
            )

    def test_macos(self):
        with patch("ytaug.download.platform.system", return_value="Darwin"):
            assert (
                get_js_runtime_install_instructions()
                == "brew install deno  OR  brew install node \nor check their website: \nhttps://deno.com OR https://nodejs.org"
            )

    def test_linux(self):
        with patch("ytaug.download.platform.system", return_value="Linux"):
            assert (
                get_js_runtime_install_instructions()
                == "curl -fsSL https://deno.land/install.sh | sh  OR  See https://nodejs.org/en/download/package-manager \nor check their website: \nhttps://deno.com OR https://nodejs.org"
            )

    def test_unknown_os(self):
        with patch("ytaug.download.platform.system", return_value="unknown_abcd"):
            assert (
                get_js_runtime_install_instructions()
                == "check their website for download instructions \nhttps://deno.com OR  See https://nodejs.org"
            )


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
