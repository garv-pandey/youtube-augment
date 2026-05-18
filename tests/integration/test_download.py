import shutil
import pytest
from ytaug.download import (
    has_js_runtime,
    get_ytdlp_js_runtime_config,
    get_url_info_ytdlp,
)


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


@pytest.fixture(scope="class")  # default scope is function
# scope class means it is destroyed after every class's use
# main benefit of using fixture over lazy loading is sharing the cache and reducing overhead of loading the value every time
def real_js_config():
    """Discovers the actual Node/Deno runtime on the host OS exactly once for this class."""
    return get_ytdlp_js_runtime_config()


@pytest.mark.integration
class TestGetUrlInfoYtdlpIntegration:
    """Verifies yt-dlp successfully executes live network queries using host tools."""

    def test_extracts_live_video_metadata_successfully(self, real_js_config):
        """Verifies end-to-end network extraction for a permanent public YouTube video."""
        # "Me at the zoo" — the most stable, permanent public video on the platform
        target_url = "https://www.youtube.com/watch?v=jNQXAC9IVRw"

        # Act: Execute real network request using unmocked yt-dlp and the host JS engine
        result = get_url_info_ytdlp(target_url, real_js_config)

        # Assert: Verify the returned dictionary shape matches reality
        assert result["id"] == "jNQXAC9IVRw"
        assert result["title"] == "Me at the zoo"
        assert result["type"] != "playlist"

    def test_extracts_live_playlist_metadata_flat(self, real_js_config):
        """Verifies flat extraction reads a playlist wrapper without parsing individual tracks."""
        # A small, stable public playlist URL
        target_playlist = (
            "https://www.youtube.com/playlist?list=PLwivhteH3vK_S0yV2w3gCh_zM-2S_3N-Z"
        )

        # Act
        result = get_url_info_ytdlp(target_playlist, real_js_config)

        # Assert: Verify the playlist conditional structural mutations executed correctly
        assert result["type"] == "playlist"
        assert "id" in result
        assert "title" in result
        assert "video_count" in result
        assert isinstance(result["video_count"], int)
