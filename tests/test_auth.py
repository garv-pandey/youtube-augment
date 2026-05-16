import json
import pytest
from unittest.mock import MagicMock, PropertyMock, patch
from ytmm.exceptions import YTMMError
from ytmm.auth import (
    check_client_secret,
    copy_client_secret,
    check_tokens,
    auth_logout,
)


class TestCheckClientSecret:
    """check_client_secret() — validates 'Installed App' client_secret.json"""

    @staticmethod
    def _valid_secret():
        return {
            "installed": {
                "client_id": "123.apps.googleusercontent.com",
                "client_secret": "G0CSP-xyz",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": ["http://localhost"],
            }
        }

    def test_file_does_not_exist(self, tmp_path):
        """Returns False when the file is not found."""
        nonexistent = tmp_path / "does_not_exist.json"
        assert check_client_secret(nonexistent) is False

    def test_invalid_json(self, tmp_path):
        """Returns False when the file contains malformed JSON."""
        path = tmp_path / "client_secret.json"
        path.write_text("not valid json")
        assert check_client_secret(path) is False

    def test_missing_installed_key(self, tmp_path):
        """Returns False when top-level 'installed' key is absent."""
        path = tmp_path / "client_secret.json"
        path.write_text(json.dumps({"web": {"client_id": "x"}}))
        assert check_client_secret(path) is False

    def test_missing_mandatory_field_client_secret(self, tmp_path):
        """Returns False when 'client_secret' is missing from installed data."""
        path = tmp_path / "client_secret.json"
        data = self._valid_secret()
        del data["installed"]["client_secret"]
        path.write_text(json.dumps(data))
        assert check_client_secret(path) is False

    def test_missing_mandatory_field_auth_uri(self, tmp_path):
        """Returns False when 'auth_uri' is missing."""
        path = tmp_path / "client_secret.json"
        data = self._valid_secret()
        del data["installed"]["auth_uri"]
        path.write_text(json.dumps(data))
        assert check_client_secret(path) is False

    def test_missing_mandatory_field_token_uri(self, tmp_path):
        """Returns False when 'token_uri' is missing."""
        path = tmp_path / "client_secret.json"
        data = self._valid_secret()
        del data["installed"]["token_uri"]
        path.write_text(json.dumps(data))
        assert check_client_secret(path) is False

    def test_missing_redirect_uris_key(self, tmp_path):
        """Returns False when 'redirect_uris' key is absent."""
        path = tmp_path / "client_secret.json"
        data = self._valid_secret()
        del data["installed"]["redirect_uris"]
        path.write_text(json.dumps(data))
        assert check_client_secret(path) is False

    def test_empty_redirect_uris(self, tmp_path):
        """Returns False when 'redirect_uris' is an empty list."""
        path = tmp_path / "client_secret.json"
        data = self._valid_secret()
        data["installed"]["redirect_uris"] = []
        path.write_text(json.dumps(data))
        assert check_client_secret(path) is False

    def test_valid(self, tmp_path):
        """Returns True for a complete, valid client secret."""
        path = tmp_path / "client_secret.json"
        path.write_text(json.dumps(self._valid_secret()))
        assert check_client_secret(path) is True


class TestCopyClientSecret:
    def test_copies_file_to_destination(self, tmp_path):
        """File exists at dest with same content after copy."""
        src = tmp_path / "source.json"
        src.write_text('{"client_id": "abc"}')
        dest = tmp_path / "config" / "client_secret.json"

        copy_client_secret(src, dest)

        assert dest.exists()
        assert dest.read_text() == src.read_text()

    def test_creates_parent_directories(self, tmp_path):
        """Parent of dest is created automatically."""
        src = tmp_path / "source.json"
        src.write_text("content")
        dest = tmp_path / "a" / "b" / "c" / "dest.json"

        copy_client_secret(src, dest)

        assert dest.exists()

    def test_source_not_found(self, tmp_path):
        """Raises YTMMError when source file does not exist."""
        nonexistent = tmp_path / "nope.json"
        dest = tmp_path / "dest.json"

        with pytest.raises(YTMMError):
            copy_client_secret(nonexistent, dest)

    def test_source_file_unchanged_after_copy(self, tmp_path):
        """Original source file is not modified by the copy."""
        src = tmp_path / "source.json"
        src.write_text("original content")
        dest = tmp_path / "dest.json"

        copy_client_secret(src, dest)

        assert src.read_text() == "original content"


class TestCheckTokens:
    """check_tokens() — validates OAuth tokens, refreshes if needed."""

    def test_file_not_found(self, tmp_path):
        """Returns False when the token file doesn't exist."""
        nonexistent = tmp_path / "does_not_exist.json"
        assert check_tokens(tokens_path=nonexistent) is False

    def test_load_raises(self, tmp_path):
        """Returns False when loading the token file fails."""
        path = tmp_path / "tokens.json"
        path.write_text("{}")

        with patch(
            "ytmm.auth.Credentials.from_authorized_user_file",
            side_effect=ValueError("bad file"),
        ):
            with patch("ytmm.auth.Request"):
                result = check_tokens(tokens_path=path)

        assert result is False

    def test_no_token_object(self, tmp_path):
        """Returns False when from_authorized_user_file returns None."""
        path = tmp_path / "tokens.json"
        path.write_text("{}")

        with patch(
            "ytmm.auth.Credentials.from_authorized_user_file", return_value=None
        ):
            with patch("ytmm.auth.Request"):
                result = check_tokens(tokens_path=path)

        assert result is False

    def test_valid_token(self, tmp_path):
        """Returns True when tokens are valid and not expired."""
        path = tmp_path / "tokens.json"
        path.write_text("{}")

        mock_creds = MagicMock()
        mock_creds.valid = True

        with patch(
            "ytmm.auth.Credentials.from_authorized_user_file",
            return_value=mock_creds,
        ):
            with patch("ytmm.auth.Request"):
                result = check_tokens(tokens_path=path)

        assert result is True

    def test_expired_refreshes(self, tmp_path):
        """Refreshes and returns True when tokens expired but refreshable."""
        path = tmp_path / "tokens.json"
        path.write_text("{}")

        mock_creds = MagicMock()
        mock_creds.expired = True
        mock_creds.refresh_token = "abc"
        mock_creds.to_json.return_value = '{"refreshed": true}'
        # .valid returns False on first access (enters refresh block),
        # then True on second access (simulates refresh flipping it)
        type(mock_creds).valid = PropertyMock(side_effect=[False, True])

        with patch(
            "ytmm.auth.Credentials.from_authorized_user_file",
            return_value=mock_creds,
        ):
            with patch("ytmm.auth.Request"):
                result = check_tokens(tokens_path=path)

        assert result is True
        mock_creds.refresh.assert_called_once()
        assert path.read_text() == '{"refreshed": true}'

    def test_refresh_raises(self, tmp_path):
        """Returns False when the refresh call itself fails."""
        path = tmp_path / "tokens.json"
        path.write_text("{}")

        mock_creds = MagicMock()
        mock_creds.valid = False
        mock_creds.expired = True
        mock_creds.refresh_token = "abc"
        mock_creds.refresh.side_effect = Exception("network error")

        with patch(
            "ytmm.auth.Credentials.from_authorized_user_file",
            return_value=mock_creds,
        ):
            with patch("ytmm.auth.Request"):
                result = check_tokens(tokens_path=path)

        assert result is False

    def test_no_refresh_token(self, tmp_path):
        """Returns False when tokens expired but no refresh_token."""
        path = tmp_path / "tokens.json"
        path.write_text("{}")

        mock_creds = MagicMock()
        mock_creds.valid = False
        mock_creds.expired = True
        mock_creds.refresh_token = None

        with patch(
            "ytmm.auth.Credentials.from_authorized_user_file",
            return_value=mock_creds,
        ):
            with patch("ytmm.auth.Request"):
                result = check_tokens(tokens_path=path)

        assert result is False

    def test_invalid_not_expired(self, tmp_path):
        """Returns False when tokens invalid for a non-expiry reason."""
        path = tmp_path / "tokens.json"
        path.write_text("{}")

        mock_creds = MagicMock()
        mock_creds.valid = False
        mock_creds.expired = False

        with patch(
            "ytmm.auth.Credentials.from_authorized_user_file",
            return_value=mock_creds,
        ):
            with patch("ytmm.auth.Request"):
                result = check_tokens(tokens_path=path)

        assert result is False


class TestAuthLogout:
    """auth_logout() — deletes token and/or client secret files."""

    def test_delete_tokens_file_exists(self, tmp_path):
        """Deletes tokens.json and returns confirmation."""
        tokens = tmp_path / "tokens.json"
        tokens.write_text("{}")

        messages = auth_logout(
            delete_tokens=True,
            delete_secrets=False,
            tokens_path=tokens,
        )

        assert messages == ["tokens.json removed."]
        assert not tokens.exists()

    def test_delete_tokens_file_missing(self, tmp_path):
        """Returns 'not found' message when tokens.json doesn't exist."""
        tokens = tmp_path / "tokens.json"

        messages = auth_logout(
            delete_tokens=True,
            delete_secrets=False,
            tokens_path=tokens,
        )

        assert messages == ["tokens.json not found."]

    def test_skip_tokens_delete_secrets(self, tmp_path):
        """Only deletes client_secret when delete_tokens=False."""
        tokens = tmp_path / "tokens.json"
        tokens.write_text("{}")
        secrets = tmp_path / "client_secret.json"
        secrets.write_text("{}")

        messages = auth_logout(
            delete_tokens=False,
            delete_secrets=True,
            tokens_path=tokens,
            client_secret_path=secrets,
        )

        assert messages == ["client_secret.json removed."]
        assert tokens.exists()
        assert not secrets.exists()

    def test_delete_both_present(self, tmp_path):
        """Deletes both files when both exist."""
        tokens = tmp_path / "tokens.json"
        tokens.write_text("{}")
        secrets = tmp_path / "client_secret.json"
        secrets.write_text("{}")

        messages = auth_logout(
            delete_tokens=True,
            delete_secrets=True,
            tokens_path=tokens,
            client_secret_path=secrets,
        )

        assert messages == [
            "tokens.json removed.",
            "client_secret.json removed.",
        ]
        assert not tokens.exists()
        assert not secrets.exists()

    def test_delete_both_missing(self, tmp_path):
        """Returns both 'not found' messages when neither file exists."""
        tokens = tmp_path / "tokens.json"
        secrets = tmp_path / "client_secret.json"

        messages = auth_logout(
            delete_tokens=True,
            delete_secrets=True,
            tokens_path=tokens,
            client_secret_path=secrets,
        )

        assert messages == [
            "tokens.json not found.",
            "client_secret.json not found.",
        ]

    def test_delete_nothing(self, tmp_path):
        """Returns empty list when both delete flags are False."""
        messages = auth_logout(
            delete_tokens=False,
            delete_secrets=False,
            tokens_path=tmp_path / "irrelevant.json",
        )

        assert messages == []


# authenticate() — no unit tests.
#   Relies on google_auth_oauthlib's browser-based OAuth flow
#   (InstalledAppFlow.from_client_secrets_file + run_local_server).
#   Testing it would mock the entire flow, verifying nothing real
#   about the OAuth handshake. Manual integration test covers this.

# get_credentials() — no unit tests.
#   Thin wrapper around Credentials.from_authorized_user_file.
#   The error-handling pattern (catch → YTMMError) is identical to
#   check_tokens (catch → False). No additional conditional logic
#   worth isolating.

# get_user_info() — no unit tests.
#   Thin wrapper around AuthorizedSession + HTTP GET + raise_for_status.
#   Same error-handling pattern as get_credentials. The logic is
#   identical to authenticate: library call → return/catch → YTMMError.
#   No branching, no data transformation, no business logic.

