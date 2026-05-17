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
        pass

    def test_get_ffmpeg_install_instructions_macos(self):
        pass

    def test_get_ffmpeg_install_instructions_linux(self):
        pass

    def test_get_ffmpeg_install_instructions_undefined(self):
        pass


class TestGetJsRuntime:
    def test_get_js_runtime_deno(self):
        pass

    def test_get_js_runtime_node(self):
        pass

    def test_get_js_runtime_none(self):
        pass


class TestGetJsRuntimeInstallInstructions:
    def test_windows(self):
        pass

    def test_macos(self):
        pass

    def test_linux(self):
        pass

    def test_unknown_os(self):
        pass


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
