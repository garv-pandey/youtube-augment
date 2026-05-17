import typer
import traceback
from typing import Annotated
from pathlib import Path

# TODO: publish the app
from ytaug.download import (
    check_ffmpeg,
    get_ytdlp_js_runtime_config,
    get_ffmpeg_install_instructions,
    get_js_runtime_install_instructions,
    download_playlist,
    get_playlist_info_dlp,
)
from ytaug.exceptions import YTAugError

app = typer.Typer(no_args_is_help=True)


@app.command(help="Download audio from a YouTube playlist as m4a (192kbps)")
def download(
    playlist_url: Annotated[str, typer.Argument(help="YouTube playlist URL")],
    output: Annotated[
        Path,
        typer.Option("--output", "-o", help="Output directory for downloaded files"),
    ] = Path.cwd(),
):
    try:
        runtime_config = get_ytdlp_js_runtime_config()
        if not runtime_config:
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


if __name__ == "__main__":
    app()
