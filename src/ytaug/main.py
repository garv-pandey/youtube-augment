import typer
import traceback
from typing import Annotated, Optional
from pathlib import Path

# TODO: publish the app
from ytaug.download import (
    check_ffmpeg,
    get_js_runtime,
    get_ffmpeg_install_instructions,
    get_js_runtime_install_instructions,
    download_playlist,
)
from ytaug.auth import (
    check_client_secret,
    copy_client_secret,
    check_tokens,
    get_user_info,
    authenticate,
    get_credentials,
    auth_logout,
    TOKENS_PATH,
)
from ytaug.copy import (
    create_playlist,
    add_videos_to_playlist,
)
from ytaug.playlist import (
    is_youtube_playlist,
    get_playlist_info_dlp,
    get_video_ids,
)
from ytaug.exceptions import YTAugError, SystemRequirementError


app = typer.Typer(no_args_is_help=True)
auth_app = typer.Typer(no_args_is_help=True)
app.add_typer(
    auth_app, name="auth", help="Manage authentication for your YouTube account"
)


@app.command(help="Download audio from a YouTube playlist as m4a (192kbps)")
def download(
    playlist_url: Annotated[str, typer.Argument(help="YouTube playlist URL")],
    output: Annotated[
        Path,
        typer.Option("--output", "-o", help="Output directory for downloaded files"),
    ] = Path.cwd(),
):
    try:
        try:
            _, runtime_config = get_js_runtime()
        except SystemRequirementError:
            typer.echo(
                "Error: A JavaScript runtime (deno or node) is required but not found on your system."
            )
            typer.echo("Install one of the following:")
            typer.echo(get_js_runtime_install_instructions())
            raise typer.Exit(1)

        if not check_ffmpeg():
            typer.echo("Error: ffmpeg is required but not found on your system.")
            typer.echo(f"Install it using: {get_ffmpeg_install_instructions()}")
            raise typer.Exit(1)

        info = get_playlist_info_dlp(playlist_url, runtime_config)

        confirmed = typer.confirm(
            f'Download "{info["title"]}" ({info["video_count"]} tracks) to {output}?'
        )
        if not confirmed:
            typer.echo("Download cancelled.")
            raise typer.Exit(0)

        download_playlist(playlist_url, output, runtime_config)
        typer.echo("Download complete.")

    except typer.Exit:
        raise
    except YTAugError as e:
        typer.echo(f"App error: {e}")
        raise typer.Exit(1)
    except Exception as e:
        traceback.print_exc()
        typer.echo(f"Uncaught Exception: {e}")
        raise typer.Exit(1)


@app.command(help="Copy a YouTube playlist to your account")
def copy(
    playlist_url: Annotated[str, typer.Argument(help="YouTube playlist URL to copy")],
    name: Annotated[
        Optional[str],
        typer.Option("--name", "-n", help="Custom name for the new playlist"),
    ] = None,
    public: Annotated[
        bool,
        typer.Option(
            "--public", "-p", help="Make the new playlist public (default: private)"
        ),
    ] = False,
):
    try:
        # 1. Validate URL
        if not is_youtube_playlist(playlist_url):
            typer.echo("Error: Not a valid YouTube playlist URL.")
            raise typer.Exit(1)

        # 2. Check client_secret
        if not check_client_secret():
            typer.echo("Error: client secrets not found or invalid.")
            typer.echo("Run: ytaug auth login")
            raise typer.Exit(1)

        # 3. Check tokens
        if not check_tokens():
            typer.echo("Error: No valid authentication tokens.")
            typer.echo("Run: ytaug auth login")
            raise typer.Exit(1)

        # 4. Get JS runtime config for yt-dlp
        try:
            _, runtime_config = get_js_runtime()
        except SystemRequirementError:
            typer.echo(
                "Error: A JavaScript runtime (deno or node) is required but not found on your system."
            )
            typer.echo("Install one of the following:")
            typer.echo(get_js_runtime_install_instructions())
            raise typer.Exit(1)

        # 5. Fetch playlist info
        playlist_info = get_playlist_info_dlp(playlist_url, runtime_config)

        # 6. Show playlist details
        title = name or playlist_info["title"]
        video_count = playlist_info["video_count"]
        privacy = playlist_info["privacy_status"]
        typer.echo(f'Playlist: "{title}" ({video_count} videos) [{privacy}]')

        # 7. Confirm with user
        confirmed = typer.confirm(f'Create a copy of "{title}" in your account?')
        if not confirmed:
            typer.echo("Cancelled.")
            raise typer.Exit(0)

        # 8. Create playlist on user's account [API: 50 units]
        typer.echo("Creating playlist...")
        creds = get_credentials()
        new_playlist_id = create_playlist(
            credentials=creds,
            title=title,
            description=playlist_info["description"],
            is_public=public,
        )

        # 9. Extract video IDs from source playlist [yt-dlp: 0 units]
        typer.echo("Extracting video IDs...")
        video_ids = get_video_ids(playlist_url)

        # 10. Add videos to new playlist [API: 50 units per batch of 50]
        typer.echo("Adding videos...")
        add_videos_to_playlist(creds, new_playlist_id, video_ids)

        # 11. Show results
        typer.echo("Copy complete.")
        typer.echo(f"New playlist: https://youtube.com/playlist?list={new_playlist_id}")
        typer.echo(f"Added {video_count} videos.")

    except typer.Exit:
        raise
    except YTAugError as e:
        typer.echo(f"App error: {e}")
        raise typer.Exit(1)
    except Exception as e:
        traceback.print_exc()
        typer.echo(f"Uncaught Exception: {e}")
        raise typer.Exit(1)


@auth_app.command(help="Authenticate with your YouTube account")
def login(
    force: Annotated[
        bool,
        typer.Option("--force", "-f", help="Re-authenticate even if already logged in"),
    ] = False,
    no_browser: Annotated[
        bool,
        typer.Option(
            "--no-browser",
            "--headless",
            help="Print auth URL instead of opening a browser",
        ),
    ] = False,
):
    try:
        if force and check_tokens():
            auth_logout(delete_secrets=False, delete_tokens=True)

        # checking client_secret
        if not check_client_secret():
            typer.echo("Error: client secrets not found or invalid.")
            typer.echo('Your client_secret.json must be of type "Installed App".')
            typer.echo("")

            while True:
                path = typer.prompt("Path to client_secret.json")
                if Path(path).expanduser().exists():
                    copy_client_secret(Path(path))
                    typer.echo("client_secret.json saved.")
                    if check_client_secret():
                        break
                    typer.echo(
                        "Error: The provided file is not a valid TV-type client_secret.json."
                    )
                else:
                    typer.echo(f"Error: File not found: {path}")

        # checking tokens
        if not check_tokens():
            typer.echo("")
            typer.echo("Starting authentication...")
            creds = authenticate(open_browser=not no_browser)
            TOKENS_PATH.parent.mkdir(parents=True, exist_ok=True)
            TOKENS_PATH.write_text(creds.to_json())
            typer.echo("Authentication successful.")
        else:
            creds = get_credentials()
            user_info = get_user_info(creds)
            typer.echo(
                f"Currently logged in as: {user_info['name']} ({user_info['email']})"
            )
            if typer.confirm("Want to re-authenticate?"):
                auth_logout(delete_secrets=False, delete_tokens=True)
                typer.echo("Starting re-authentication...")
                creds = authenticate(open_browser=not no_browser)
                TOKENS_PATH.parent.mkdir(parents=True, exist_ok=True)
                TOKENS_PATH.write_text(creds.to_json())
                typer.echo("Authentication successful.")
            else:
                typer.echo("Login skipped.")

    except typer.Exit:
        raise
    except YTAugError as e:
        typer.echo(f"App error: {e}")
        raise typer.Exit(1)
    except Exception as e:
        traceback.print_exc()
        typer.echo(f"Uncaught Exception: {e}")
        raise typer.Exit(1)


@auth_app.command(help="Revoke authentication tokens and log out")
def logout(
    clean_all: Annotated[
        bool,
        typer.Option("--all", "-a", help="Also delete client secrets"),
    ] = False,
):
    try:
        if not check_tokens():
            typer.echo("Not logged in.")
            raise typer.Exit(0)

        creds = get_credentials()
        try:
            user_info = get_user_info(creds)
            typer.echo(
                f"Currently logged in as: {user_info['name']} ({user_info['email']})"
            )
        except YTAugError:
            typer.echo("Logged in (account info unavailable).")

        if typer.confirm("Want to logout?"):
            messages = auth_logout(delete_tokens=True, delete_secrets=clean_all)
            for msg in messages:
                typer.echo(msg)

    except typer.Exit:
        raise
    except YTAugError as e:
        typer.echo(f"App error: {e}")
        raise typer.Exit(1)
    except Exception as e:
        traceback.print_exc()
        typer.echo(f"Uncaught Exception: {e}")
        raise typer.Exit(1)


@auth_app.command(help="Show the currently authenticated user")
def whoami():
    try:
        if not check_tokens():
            typer.echo("Not logged in.")
            raise typer.Exit(0)

        creds = get_credentials()
        user_info = get_user_info(creds)
        typer.echo(
            f"Currently logged in as: {user_info['name']} ({user_info['email']})"
        )

    except typer.Exit:
        raise
    except YTAugError as e:
        typer.echo(f"App error: {e}")
        raise typer.Exit(1)
    except Exception as e:
        traceback.print_exc()
        typer.echo(f"Uncaught Exception: {e}")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
