import pytest
from unittest.mock import patch
from ytmm.download import (
    check_ffmpeg,
    download_playlist,
    get_ffmpeg_install_instructions,
    get_js_runtime,
    get_js_runtime_install_instructions,
)
from ytmm.exceptions import YTMMError, SystemRequirementError


class TestCheckFfmpeg:
    def test_ffmpeg_found(self):
        with patch("ytmm.download.shutil.which", return_value="/usr/bin/ffmpeg"):
            assert check_ffmpeg() is True

    def test_ffmpeg_not_found(self):
        with patch("ytmm.download.shutil.which", return_value=None):
            assert check_ffmpeg() is False


class TestGetFfmpegInstallInstructions:
    def test_get_ffmpeg_install_instructions_windows(self):
        with patch("ytmm.download.platform.system", return_value="Windows"):
            assert get_ffmpeg_install_instructions() == "winget install ffmpeg"

    def test_get_ffmpeg_install_instructions_macos(self):
        with patch("ytmm.download.platform.system", return_value="Darwin"):
            assert get_ffmpeg_install_instructions() == "brew install ffmpeg"

    def test_get_ffmpeg_install_instructions_linux(self):
        with patch("ytmm.download.platform.system", return_value="Linux"):
            assert (
                get_ffmpeg_install_instructions()
                == "sudo apt install ffmpeg (Debian/Ubuntu) or sudo dnf install ffmpeg (Fedora)"
            )

    def test_get_ffmpeg_install_instructions_undefined(self):
        with patch("ytmm.download.platform.system", return_value=None):
            assert (
                get_ffmpeg_install_instructions()
                == "See https://ffmpeg.org/download.html"
            )


class TestGetJsRuntime:
    def test_get_js_runtime_deno(self):
        with patch("ytmm.download.shutil.which", return_value="/usr/bin/deno"):
            name, config = get_js_runtime()
            assert name == "deno"
            assert config == {"deno": {"path": "/usr/bin/deno"}}

    def test_get_js_runtime_node(self):
        with patch(
            "ytmm.download.shutil.which",
            side_effect=[None, "/temp/test/parent_dir/node"],
        ):
            name, config = get_js_runtime()
            assert name == "node"
            assert config == {"node": {"path": "/temp/test/parent_dir/node"}}

    def test_get_js_runtime_none(self):
        with patch("ytmm.download.shutil.which", return_value=None):
            with pytest.raises(SystemRequirementError):
                get_js_runtime()


class TestGetJsRuntimeInstallInstructions:
    def test_windows(self):
        with patch("ytmm.download.platform.system", return_value="Windows"):
            result = get_js_runtime_install_instructions()
            assert result == "winget install deno  OR  winget install OpenJS.NodeJS"

    def test_macos(self):
        with patch("ytmm.download.platform.system", return_value="Darwin"):
            result = get_js_runtime_install_instructions()
            assert result == "brew install deno  OR  brew install node"

    def test_linux(self):
        with patch("ytmm.download.platform.system", return_value="Linux"):
            result = get_js_runtime_install_instructions()
            assert (
                result
                == "curl -fsSL https://deno.land/install.sh | sh  OR  See https://nodejs.org/en/download/package-manager"
            )

    def test_unknown_os(self):
        with patch("ytmm.download.platform.system", return_value="FreeBSD"):
            result = get_js_runtime_install_instructions()
            assert result == "See https://deno.land  OR  See https://nodejs.org"


class TestDownloadPlaylist:
    """download_playlist() — downloads audio via yt-dlp."""

    def test_success(self, tmp_path):
        with patch("ytmm.download.yt_dlp.YoutubeDL") as mock_ydl:
            mock_ydl.return_value.__enter__.return_value.download.return_value = None

            download_playlist(
                "https://youtube.com/playlist?list=PLxyz",
                tmp_path,
                {"deno": {"path": "/usr/bin/deno"}},
            )

            mock_ydl.return_value.__enter__.return_value.download.assert_called_once_with(
                ["https://youtube.com/playlist?list=PLxyz"]
            )

    def test_failure_raises_ytmmerror(self, tmp_path):
        with patch("ytmm.download.yt_dlp.YoutubeDL") as mock_ydl:
            mock_ydl.return_value.__enter__.return_value.download.side_effect = (
                Exception("yt-dlp error")
            )

            with pytest.raises(YTMMError):
                download_playlist(
                    "https://youtube.com/playlist?list=PLxyz",
                    tmp_path,
                    {"deno": {"path": "/usr/bin/deno"}},
                )
