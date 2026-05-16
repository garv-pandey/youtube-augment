from pathlib import Path
from typer.testing import CliRunner
from unittest.mock import MagicMock, patch
from ytaug.exceptions import SystemRequirementError
from ytaug.main import app

runner = CliRunner()


class TestDownloadCommand:
    """ytaug download — validates prereqs, confirms, downloads audio."""

    def test_missing_url(self):
        result = runner.invoke(app, ["download"])
        assert result.exit_code != 0

    def test_ffmpeg_missing(self):
        with patch("ytaug.main.check_ffmpeg", return_value=False):
            with patch("ytaug.main.get_js_runtime", return_value=("deno", {})):
                result = runner.invoke(
                    app, ["download", "https://youtube.com/playlist?list=PL_abc"]
                )
        assert result.exit_code == 1
        assert "ffmpeg" in result.stdout

    def test_js_runtime_missing(self):
        with patch("ytaug.main.get_js_runtime", side_effect=SystemRequirementError):
            result = runner.invoke(
                app, ["download", "https://youtube.com/playlist?list=PL_abc"]
            )
        assert result.exit_code == 1
        assert "JavaScript runtime" in result.stdout

    def test_user_cancels_at_prompt(self):
        info = {"title": "My Mix", "video_count": 12}
        with patch("ytaug.main.check_ffmpeg", return_value=True):
            with patch("ytaug.main.get_js_runtime", return_value=("deno", {})):
                with patch("ytaug.main.get_playlist_info_dlp", return_value=info):
                    with patch("ytaug.main.typer.confirm", return_value=False):
                        result = runner.invoke(
                            app,
                            ["download", "https://youtube.com/playlist?list=PL_abc"],
                        )
        assert result.exit_code == 0
        assert "cancelled" in result.stdout.lower()

    def test_success(self):
        info = {"title": "My Mix", "video_count": 12}
        with patch("ytaug.main.check_ffmpeg", return_value=True):
            with patch("ytaug.main.get_js_runtime", return_value=("deno", {})):
                with patch("ytaug.main.get_playlist_info_dlp", return_value=info):
                    with patch("ytaug.main.typer.confirm", return_value=True):
                        with patch("ytaug.main.download_playlist") as mock_dl:
                            result = runner.invoke(
                                app,
                                [
                                    "download",
                                    "https://youtube.com/playlist?list=PL_abc",
                                ],
                            )
        assert result.exit_code == 0
        assert "complete" in result.stdout.lower()
        mock_dl.assert_called_once()

    def test_success_with_output_flag(self):
        info = {"title": "My Mix", "video_count": 3}
        with patch("ytaug.main.check_ffmpeg", return_value=True):
            with patch("ytaug.main.get_js_runtime", return_value=("deno", {})):
                with patch("ytaug.main.get_playlist_info_dlp", return_value=info):
                    with patch("ytaug.main.typer.confirm", return_value=True):
                        with patch("ytaug.main.download_playlist") as mock_dl:
                            result = runner.invoke(
                                app,
                                [
                                    "download",
                                    "https://youtube.com/playlist?list=PL_abc",
                                    "-o",
                                    "/tmp/music",
                                ],
                            )
        assert result.exit_code == 0
        assert "complete" in result.stdout.lower()
        mock_dl.assert_called_once_with(
            "https://youtube.com/playlist?list=PL_abc", Path("/tmp/music"), {}
        )


class TestCopyCommand:
    """ytaug copy — validates URL, auth, prereqs, then copies playlist."""

    def test_invalid_url(self):
        with patch("ytaug.main.is_youtube_playlist", return_value=False):
            result = runner.invoke(app, ["copy", "https://example.com"])
        assert result.exit_code == 1
        assert "Not a valid" in result.stdout

    def test_no_client_secret(self):
        with patch("ytaug.main.is_youtube_playlist", return_value=True):
            with patch("ytaug.main.check_client_secret", return_value=False):
                result = runner.invoke(
                    app, ["copy", "https://youtube.com/playlist?list=PL_abc"]
                )
        assert result.exit_code == 1
        assert "client secrets" in result.stdout.lower()

    def test_no_tokens(self):
        with patch("ytaug.main.is_youtube_playlist", return_value=True):
            with patch("ytaug.main.check_client_secret", return_value=True):
                with patch("ytaug.main.check_tokens", return_value=False):
                    result = runner.invoke(
                        app, ["copy", "https://youtube.com/playlist?list=PL_abc"]
                    )
        assert result.exit_code == 1
        assert "authentication" in result.stdout.lower()

    def test_js_runtime_missing(self):
        with patch("ytaug.main.is_youtube_playlist", return_value=True):
            with patch("ytaug.main.check_client_secret", return_value=True):
                with patch("ytaug.main.check_tokens", return_value=True):
                    with patch(
                        "ytaug.main.get_js_runtime", side_effect=SystemRequirementError
                    ):
                        result = runner.invoke(
                            app, ["copy", "https://youtube.com/playlist?list=PL_abc"]
                        )
        assert result.exit_code == 1
        assert "JavaScript runtime" in result.stdout

    def test_user_cancels_at_prompt(self):
        info = {
            "title": "Test",
            "video_count": 5,
            "description": "desc",
            "privacy_status": "public",
        }
        with patch("ytaug.main.is_youtube_playlist", return_value=True):
            with patch("ytaug.main.check_client_secret", return_value=True):
                with patch("ytaug.main.check_tokens", return_value=True):
                    with patch("ytaug.main.get_js_runtime", return_value=("deno", {})):
                        with patch(
                            "ytaug.main.get_playlist_info_dlp", return_value=info
                        ):
                            with patch("ytaug.main.typer.confirm", return_value=False):
                                result = runner.invoke(
                                    app,
                                    [
                                        "copy",
                                        "https://youtube.com/playlist?list=PL_abc",
                                    ],
                                )
        assert result.exit_code == 0
        assert "cancelled" in result.stdout.lower()

    def test_success(self):
        info = {
            "title": "Test",
            "video_count": 3,
            "description": "desc",
            "privacy_status": "public",
        }
        with patch("ytaug.main.is_youtube_playlist", return_value=True):
            with patch("ytaug.main.check_client_secret", return_value=True):
                with patch("ytaug.main.check_tokens", return_value=True):
                    with patch("ytaug.main.get_js_runtime", return_value=("deno", {})):
                        with patch(
                            "ytaug.main.get_playlist_info_dlp", return_value=info
                        ):
                            with patch("ytaug.main.typer.confirm", return_value=True):
                                with patch("ytaug.main.get_credentials"):
                                    with patch(
                                        "ytaug.main.create_playlist",
                                        return_value="PL_new",
                                    ):
                                        with patch(
                                            "ytaug.main.get_video_ids",
                                            return_value=["v1", "v2", "v3"],
                                        ):
                                            with patch(
                                                "ytaug.main.add_videos_to_playlist"
                                            ) as mock_add:
                                                result = runner.invoke(
                                                    app,
                                                    [
                                                        "copy",
                                                        "https://youtube.com/playlist?list=PL_abc",
                                                    ],
                                                )
        assert result.exit_code == 0
        assert "complete" in result.stdout.lower()
        mock_add.assert_called_once()

    def test_success_with_flags(self):
        info = {
            "title": "Original",
            "video_count": 2,
            "description": "desc",
            "privacy_status": "public",
        }
        with patch("ytaug.main.is_youtube_playlist", return_value=True):
            with patch("ytaug.main.check_client_secret", return_value=True):
                with patch("ytaug.main.check_tokens", return_value=True):
                    with patch("ytaug.main.get_js_runtime", return_value=("deno", {})):
                        with patch(
                            "ytaug.main.get_playlist_info_dlp", return_value=info
                        ):
                            with patch("ytaug.main.typer.confirm", return_value=True):
                                with patch("ytaug.main.get_credentials"):
                                    with patch(
                                        "ytaug.main.create_playlist"
                                    ) as mock_create:
                                        with patch(
                                            "ytaug.main.get_video_ids",
                                            return_value=["v1", "v2"],
                                        ):
                                            with patch(
                                                "ytaug.main.add_videos_to_playlist"
                                            ):
                                                result = runner.invoke(
                                                    app,
                                                    [
                                                        "copy",
                                                        "https://youtube.com/playlist?list=PL_abc",
                                                        "-n",
                                                        "Renamed",
                                                        "--public",
                                                    ],
                                                )
        assert result.exit_code == 0
        _, kwargs = mock_create.call_args
        assert kwargs["title"] == "Renamed"
        assert kwargs["is_public"] is True


class TestAuthLoginCommand:
    """ytaug auth login — OAuth2 authentication flow."""

    def test_first_time_login(self):
        mock_creds = MagicMock()
        mock_creds.to_json.return_value = '{"token": "abc"}'

        with patch("ytaug.main.check_client_secret", return_value=True):
            with patch("ytaug.main.check_tokens", return_value=False):
                with patch("ytaug.main.authenticate", return_value=mock_creds):
                    with patch("ytaug.main.TOKENS_PATH") as mock_path:
                        mock_path.parent.mkdir.return_value = None
                        mock_path.write_text.return_value = None
                        result = runner.invoke(app, ["auth", "login"])
        assert result.exit_code == 0
        assert "Authentication successful" in result.stdout
        mock_path.write_text.assert_called_once_with('{"token": "abc"}')

    def test_already_logged_in_skips(self):
        with patch("ytaug.main.check_client_secret", return_value=True):
            with patch("ytaug.main.check_tokens", return_value=True):
                with patch("ytaug.main.get_credentials"):
                    with patch(
                        "ytaug.main.get_user_info",
                        return_value={"name": "Test User", "email": "test@user.com"},
                    ):
                        with patch("ytaug.main.typer.confirm", return_value=False):
                            result = runner.invoke(app, ["auth", "login"])
        assert result.exit_code == 0
        assert "Test User" in result.stdout
        assert "Login skipped" in result.stdout

    def test_force_flag_reauthenticates(self):
        mock_creds = MagicMock()
        mock_creds.to_json.return_value = "{}"

        with patch("ytaug.main.check_client_secret", return_value=True):
            with patch("ytaug.main.check_tokens", side_effect=[True, False]):
                with patch("ytaug.main.auth_logout"):
                    with patch("ytaug.main.authenticate", return_value=mock_creds):
                        with patch("ytaug.main.TOKENS_PATH") as mock_path:
                            mock_path.parent.mkdir.return_value = None
                            mock_path.write_text.return_value = None
                            result = runner.invoke(app, ["auth", "login", "--force"])
        assert result.exit_code == 0
        assert "Authentication successful" in result.stdout

    def test_no_browser_flag(self):
        mock_creds = MagicMock()
        mock_creds.to_json.return_value = "{}"

        with patch("ytaug.main.check_client_secret", return_value=True):
            with patch("ytaug.main.check_tokens", return_value=False):
                with patch("ytaug.main.authenticate") as mock_auth:
                    mock_auth.return_value = mock_creds
                    with patch("ytaug.main.TOKENS_PATH") as mock_path:
                        mock_path.parent.mkdir.return_value = None
                        mock_path.write_text.return_value = None
                        result = runner.invoke(app, ["auth", "login", "--no-browser"])
        assert result.exit_code == 0
        mock_auth.assert_called_once_with(open_browser=False)

    def test_prompts_for_client_secret(self):
        mock_creds = MagicMock()
        mock_creds.to_json.return_value = "{}"

        with patch("ytaug.main.check_client_secret", side_effect=[False, True]):
            with patch("ytaug.main.Path") as mock_path:
                mock_path.return_value.expanduser.return_value.exists.return_value = (
                    True
                )
                with patch("ytaug.main.typer.prompt", return_value="/fake/secret.json"):
                    with patch("ytaug.main.copy_client_secret"):
                        with patch("ytaug.main.check_tokens", return_value=False):
                            with patch(
                                "ytaug.main.authenticate", return_value=mock_creds
                            ):
                                with patch("ytaug.main.TOKENS_PATH") as tp:
                                    tp.parent.mkdir.return_value = None
                                    tp.write_text.return_value = None
                                    result = runner.invoke(app, ["auth", "login"])
        assert result.exit_code == 0
        assert "client_secret.json saved" in result.stdout


class TestAuthLogoutCommand:
    """ytaug auth logout — revoke tokens and log out."""

    def test_not_logged_in(self):
        with patch("ytaug.main.check_tokens", return_value=False):
            result = runner.invoke(app, ["auth", "logout"])
        assert result.exit_code == 0
        assert "Not logged in" in result.stdout

    def test_logout_success(self):
        with patch("ytaug.main.check_tokens", return_value=True):
            with patch("ytaug.main.get_credentials"):
                with patch(
                    "ytaug.main.get_user_info",
                    return_value={"name": "User", "email": "u@example.com"},
                ):
                    with patch("ytaug.main.typer.confirm", return_value=True):
                        with patch(
                            "ytaug.main.auth_logout", return_value=["Tokens deleted."]
                        ) as mock_logout:
                            result = runner.invoke(app, ["auth", "logout"])
        assert result.exit_code == 0
        assert "Tokens deleted" in result.stdout
        mock_logout.assert_called_once_with(delete_tokens=True, delete_secrets=False)

    def test_logout_with_all_flag(self):
        with patch("ytaug.main.check_tokens", return_value=True):
            with patch("ytaug.main.get_credentials"):
                with patch(
                    "ytaug.main.get_user_info",
                    return_value={"name": "User", "email": "u@example.com"},
                ):
                    with patch("ytaug.main.typer.confirm", return_value=True):
                        with patch(
                            "ytaug.main.auth_logout", return_value=["Tokens deleted."]
                        ) as mock_logout:
                            result = runner.invoke(app, ["auth", "logout", "--all"])
        assert result.exit_code == 0
        mock_logout.assert_called_once_with(delete_tokens=True, delete_secrets=True)


class TestAuthWhoamiCommand:
    """ytaug auth whoami — show current user."""

    def test_not_logged_in(self):
        with patch("ytaug.main.check_tokens", return_value=False):
            result = runner.invoke(app, ["auth", "whoami"])
        assert result.exit_code == 0
        assert "Not logged in" in result.stdout

    def test_shows_user_info(self):
        with patch("ytaug.main.check_tokens", return_value=True):
            with patch("ytaug.main.get_credentials"):
                with patch(
                    "ytaug.main.get_user_info",
                    return_value={"name": "Jane", "email": "j@example.com"},
                ):
                    result = runner.invoke(app, ["auth", "whoami"])
        assert result.exit_code == 0
        assert "Jane" in result.stdout
        assert "j@example.com" in result.stdout
