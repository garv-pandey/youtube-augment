import shutil
import json
from pathlib import Path
from typing import Optional
from platformdirs import user_config_dir, user_data_dir
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request, AuthorizedSession

from ytaug.exceptions import YTAugError

CLIENT_SECRET_PATH = Path(user_config_dir("ytaug")) / "client_secret.json"
TOKENS_PATH = Path(user_data_dir("ytaug")) / "tokens.json"
SCOPES = [
    "https://www.googleapis.com/auth/youtube.force-ssl",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "openid",
]


def check_client_secret(client_secret_path: Optional[Path] = None) -> bool:
    """
    Validates that the client secret is a valid JSON for
    an 'Installed' (Desktop) application.
    """
    client_secret_path = client_secret_path or CLIENT_SECRET_PATH

    if not client_secret_path.exists():
        return False

    try:
        with client_secret_path.open("r") as f:
            data = json.load(f)
    # TODO: add the error to error_log
    except Exception as e:
        return False

    # 1. Check for the 'installed' top-level key
    if "installed" not in data:
        # If 'web' is here instead, they downloaded the wrong type
        return False

    installed_data = data["installed"]

    # 2. Check for mandatory OAuth2 fields
    # These are what the google-auth library needs to initiate the flow
    mandatory_keys = ["client_id", "client_secret", "auth_uri", "token_uri"]

    if not all(key in installed_data for key in mandatory_keys):
        return False

    # 3. Optional: Verify redirect_uris exists (Desktop apps usually have them)
    if "redirect_uris" not in installed_data or not installed_data["redirect_uris"]:
        return False

    return True


def copy_client_secret(
    src_path: Path, client_secret_path: Optional[Path] = None
) -> None:
    """
    Copies the user-provided client secret to the application's config directory.
    The file is stored in an XDG-compliant path (e.g., ~/.config/ytaug/client_secret.json).
    Existing files at the destination will be overwritten.
    Args:
        src_path: Path to the source client_secret.json file.
    Raises:
        FileNotFoundError: If the source file does not exist.
    """
    client_secret_path = client_secret_path or CLIENT_SECRET_PATH
    src_path = src_path.expanduser().resolve()
    try:
        client_secret_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_path, client_secret_path)
    except Exception as e:
        raise YTAugError("error in copy_client_secret") from e


def authenticate(
    client_secret_path: Optional[Path] = None,
    scopes: Optional[list[str]] = None,
    open_browser: bool = False,
) -> Credentials:
    """
    Runs the browser-based OAuth2 login flow to obtain fresh credentials.

    This should only be called when check_tokens() returns False (no tokens
    exist or they are invalid/revoked). Initiates the OAuth2 flow using the
    installed client secrets and saves the resulting credentials to TOKENS_PATH.

    Args:
        open_browser: If True, automatically opens the browser. If False,
            only prints the URL for manual login.

    Requires:
        CLIENT_SECRET_PATH to exist and contain valid "installed" app credentials.
    """
    client_secret_path = client_secret_path or CLIENT_SECRET_PATH
    scopes = scopes or SCOPES

    try:
        flow = InstalledAppFlow.from_client_secrets_file(client_secret_path, scopes)
        creds = flow.run_local_server(
            port=0,
            authorization_prompt_message="Open this URL in your browser: {url}",
            open_browser=open_browser,
            prompt="consent",
            access_type="offline",
        )
    except Exception as e:
        raise YTAugError("error in authenticate") from e

    return creds


def check_tokens(
    tokens_path: Optional[Path] = None, scopes: Optional[list[str]] = None
) -> bool:
    """
    Validates the local OAuth2 tokens and refreshes them if necessary.

    Checks for the existence of the token file, attempts to load it using
    the required scopes, and performs a refresh if the access token has expired.

    Returns:
        bool: True if tokens exist and are valid (or successfully refreshed),
              False otherwise.
    """
    tokens_path = tokens_path or TOKENS_PATH
    scopes = scopes or SCOPES

    if not tokens_path.exists():
        return False

    try:
        # 1. Load credentials from the XDG-compliant path
        tokens = Credentials.from_authorized_user_file(
            str(tokens_path), scopes
        )  # converts the json to Credentials object

        if not tokens or not tokens.valid:
            # 2. If expired but we have a refresh token, try to update it
            if tokens and tokens.expired and tokens.refresh_token:
                tokens.refresh(Request())

                # 3. Save the newly refreshed tokens back to disk immediately
                with open(tokens_path, "w") as f:
                    f.write(tokens.to_json())
            else:
                return False

        return tokens.valid

    # TODO:Add the error to error_log
    except Exception as e:
        return False


def get_credentials(
    tokens_path: Optional[Path] = None, scopes: Optional[list[str]] = None
) -> Credentials:
    """
    Lazily loads OAuth2 credentials from the token file.

    This defers loading until the credentials are actually needed,
    preventing crashes on commands that don't require authentication.
    """
    tokens_path = tokens_path or TOKENS_PATH
    scopes = scopes or SCOPES

    try:
        return Credentials.from_authorized_user_file(str(tokens_path), scopes)
    except Exception as e:
        raise YTAugError("error in get_credentials") from e


def get_user_info(credentials: Credentials) -> dict:
    """
    Fetches user profile data (email, name, picture) via Google's UserInfo API.

    Returns the user info dict on success, or None if tokens don't exist
    or the request fails.
    """
    try:
        auth_sess = AuthorizedSession(credentials)
        result = auth_sess.get("https://www.googleapis.com/oauth2/v3/userinfo")
        result.raise_for_status()
        return result.json()
    except Exception as e:
        raise YTAugError("error in get_user_info") from e


def auth_logout(
    delete_tokens: bool = True,
    delete_secrets: bool = False,
    tokens_path: Optional[Path] = None,
    client_secret_path: Optional[Path] = None,
) -> list[str]:
    client_secret_path = client_secret_path or CLIENT_SECRET_PATH
    tokens_path = tokens_path or TOKENS_PATH

    messages = []

    if delete_tokens:
        if tokens_path.exists():
            tokens_path.unlink()
            messages.append("tokens.json removed.")
        else:
            messages.append("tokens.json not found.")

    if delete_secrets:
        if client_secret_path.exists():
            client_secret_path.unlink()
            messages.append("client_secret.json removed.")
        else:
            messages.append("client_secret.json not found.")

    return messages
