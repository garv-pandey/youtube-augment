import shutil
import pytest
from ytaug.download import (
    has_js_runtime,
    get_ytdlp_js_runtime_config,
    get_url_info_ytdlp,
    download_url_ytdlp,
)
from ytaug.exceptions import YTAugError


@pytest.mark.integration
def test_check_js_runtime_mirrors_actual_os():
    """Validates check_js_runtime matches the true system state."""
    js_runtime = shutil.which("deno") is not None or shutil.which("node") is not None

    # Test the pure execution
    assert has_js_runtime() is js_runtime


@pytest.mark.integration
def test_get_ytdlp_js_runtime_config_mirrors_actual_os():
    """Validates the gathered configuration dictionary mirrors the true system state."""
    real_deno = shutil.which("deno")
    real_node = shutil.which("node")

    config = get_ytdlp_js_runtime_config()

    # Dynamically assert based on what's physically on the disk
    if real_deno:
        assert "deno" in config
        assert config["deno"]["path"] == real_deno
    else:
        assert "deno" not in config

    if real_node:
        assert "node" in config
        assert config["node"]["path"] == real_node
    else:
        assert "node" not in config


# fixtures allow for lazy loading values and sharing between different scopes (function=default, class, module, session)
# pytest.skip will only skip the current test function within which the fixture envoked the skip
@pytest.fixture(scope="session")
def get_host_js_runtime():
    """Discovers the host system's JavaScript runtime (Node/Deno) safely at run-time.

    If no runtime is detected, it triggers a clean runtime skip for all dependent tests.
    """
    config = get_ytdlp_js_runtime_config()

    if not config:
        pytest.skip(
            "Environment Missing Prerequisite: A JS runtime (Node.js or Deno) is required."
        )

    return config


@pytest.fixture(scope="session")
def check_host_ffmpeg():
    """Ensures FFmpeg is available on the host system's execution PATH at run-time.

    If missing, it triggers a clean runtime skip for all dependent tests.
    """
    if shutil.which("ffmpeg") is None:
        pytest.skip(
            "Environment Missing Prerequisite: A system FFmpeg installation is required."
        )


@pytest.mark.integration
class TestGetUrlInfoYtdlpIntegration:
    """Verifies yt-dlp successfully executes live network queries using host tools."""

    def test_extracts_live_video_metadata_successfully(self, get_host_js_runtime):
        """Verifies end-to-end network extraction for a permanent public YouTube video."""
        # "Me at the zoo" — the most stable, permanent public video on the platform
        target_url = "https://www.youtube.com/watch?v=jNQXAC9IVRw"

        # Act: Execute real network request using unmocked yt-dlp and the host JS engine
        result = get_url_info_ytdlp(target_url, get_host_js_runtime)

        # Assert: Verify the returned dictionary shape matches reality
        assert result["id"] == "jNQXAC9IVRw"
        assert result["title"] == "Me at the zoo"
        assert result["type"] != "playlist"

    def test_extracts_live_playlist_metadata_flat(self, get_host_js_runtime):
        """Verifies flat extraction reads a playlist wrapper without parsing individual tracks."""
        # A small, stable public playlist URL
        target_playlist = (
            "https://www.youtube.com/playlist?list=PLQSoWXSpjA39U94TANpW67fxfYhm5CFFT"
            # technoblade's potato war
        )

        # Act
        result = get_url_info_ytdlp(target_playlist, get_host_js_runtime)

        # Assert: Verify the playlist conditional structural mutations executed correctly
        assert result["type"] == "playlist"
        assert "id" in result
        assert "title" in result
        assert "video_count" in result
        assert isinstance(result["video_count"], int)


@pytest.mark.integration
class TestDownloadUrlYtdlpIntegration:
    """Verifies end-to-end media downloading, directory structuring, and FFmpeg transcoding."""

    def test_download_single_video_converts_to_m4a(
        self, tmp_path, get_host_js_runtime, check_host_ffmpeg
    ):
        """Verifies a single video download writes an uncorrupted .m4a file directly to target directory."""
        # Use a very short public video to keep the GitHub runner or local test loop incredibly fast
        short_video_url = "https://www.youtube.com/watch?v=jNQXAC9IVRw"

        # Act: Execute the complete real download pipeline
        download_url_ytdlp(
            url=short_video_url,
            target_path=tmp_path,
            is_playlist=False,
            js_runtime_config=get_host_js_runtime,
        )

        # Assert: Look into the isolated tmp_path directory to ensure the final processed asset is there
        downloaded_files = list(tmp_path.glob("*.m4a"))

        assert len(downloaded_files) == 1
        assert downloaded_files[0].exists()
        assert (
            downloaded_files[0].stat().st_size > 0
        )  # Assures the file isn't an empty zero-byte placeholder
        assert "Me at the zoo" in downloaded_files[0].name

    def test_download_playlist_creates_nested_directory_structure(
        self, tmp_path, get_host_js_runtime, check_host_ffmpeg
    ):
        """Verifies a playlist download creates a nested folder named after the playlist title."""
        # A tiny public playlist containing 1 or 2 small audio tracks
        playlist_url = (
            "https://www.youtube.com/playlist?list=PLlAZKtV48pBYcKdtcTWrMH7EVJHodSr8C"
            # custom playlist for test
        )

        # Act
        download_url_ytdlp(
            url=playlist_url,
            target_path=tmp_path,
            is_playlist=True,
            js_runtime_config=get_host_js_runtime,
        )

        # Assert: Confirm that a playlist subfolder was dynamically spawned inside the tmp_path directory
        subdirectories = [d for d in tmp_path.iterdir() if d.is_dir()]
        assert len(subdirectories) >= 1

        # Dig into the created subfolder to verify that the children items were post-processed to m4a
        playlist_folder = subdirectories[0]
        m4a_tracks = list(playlist_folder.glob("*.m4a"))

        assert len(m4a_tracks) > 0
        assert all(track.stat().st_size > 0 for track in m4a_tracks)

    def test_download_private_video_raises_custom_exception(
        self, tmp_path, get_host_js_runtime, check_host_ffmpeg
    ):
        """Verifies that an inaccessible or missing URL maps gracefully into our custom YTAugError context."""
        # An explicit invalid/private target structure
        invalid_url = "https://www.youtube.com/watch?v=00000000000"

        # Assert that your internal try/except catch block captures the yt-dlp crash and converts it
        with pytest.raises(YTAugError) as exc_info:
            download_url_ytdlp(
                url=invalid_url,
                target_path=tmp_path,
                is_playlist=False,
                js_runtime_config=get_host_js_runtime,
            )

        # assert "Error in download_url_ytdlp" in str(exc_info.value)
