from pathlib import Path
from typer.testing import CliRunner
from unittest.mock import MagicMock, patch
from ytaug.exceptions import SystemRequirementError
from ytaug.main import app

runner = CliRunner()


class TestDownloadCommand:
    """ytaug download — validates prereqs, confirms, downloads audio."""

    def test_missing_url(self):
        pass

    def test_ffmpeg_missing(self):
        pass

    def test_js_runtime_missing(self):
        pass

    def test_user_cancels_at_prompt(self):
        pass

    def test_success(self):
        pass

    def test_success_with_output_flag(self):
        pass
