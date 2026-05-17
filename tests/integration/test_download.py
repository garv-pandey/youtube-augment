import shutil
import pytest
from ytaug.download import check_js_runtime, get_ytdlp_js_runtime_config


@pytest.mark.integration
def test_check_js_runtime_mirrors_actual_os(self):
    """Validates check_js_runtime matches the true system state."""
    has_js_runtime = (
        shutil.which("deno") is not None or shutil.which("node") is not None
    )

    # Test the pure execution
    assert check_js_runtime() is has_js_runtime


@pytest.mark.integration
def test_get_ytdlp_js_runtime_config_mirrors_actual_os(self):
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
