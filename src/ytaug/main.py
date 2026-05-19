from os import path
import typer
import traceback
from typing import Annotated
from pathlib import Path

from ytaug.download import (
    has_ffmpeg,
    get_ffmpeg_install_instructions,
    has_js_runtime,
    get_js_runtime_install_instructions,
    get_ytdlp_js_runtime_config,
    get_url_info_ytdlp,
    download_url_ytdlp,
    is_youtube_url,
)
from ytaug.exceptions import YTAugError

app = typer.Typer(no_args_is_help=True)


@app.command(help="Download audio from a YouTube playlist as m4a (192kbps)")
def download(
    url: Annotated[str, typer.Argument(help="YouTube video or playlist URL")],
    output: Annotated[
        Path,
        typer.Option("--output", "-o", help="Output directory for downloaded files"),
    ] = Path.cwd(),
):
    # check ffmpeg, js runtime and valid youtbe url
    if not has_js_runtime():
        typer.echo(
            "A JavaScript runtime (deno or node) is required but not found on your system."
        )
        typer.echo(get_js_runtime_install_instructions())
        raise typer.Exit(1)

    if not has_ffmpeg():
        typer.echo("ffmpeg is required but not found on your system.")
        typer.echo(get_ffmpeg_install_instructions())
        raise typer.Exit(1)

    if not is_youtube_url(url):
        typer.echo("Provided URL is not a valid youtube domain's URL")
        raise typer.Exit(1)

    try:
        # confirm info of video/playlist and download location
        info = get_url_info_ytdlp(
            url=url, js_runtime_config=get_ytdlp_js_runtime_config()
        )

        if info["type"] == "playlist":
            dest = Path(output, info["title"])
            confirm = typer.confirm(
                f'Download playlist: "{info["title"]}" ({info["video_count"]} tracks) → {dest}'
            )
        else:
            confirm = typer.confirm(f'Download video: "{info["title"]}" → {output}')
        if not confirm:
            typer.echo("Download cancelled.")
            raise typer.Exit(0)

        # download the files

        download_url_ytdlp(
            url=url,
            target_path=output,
            is_playlist=info["type"] == "playlist",
            js_runtime_config=get_ytdlp_js_runtime_config(),
        )
        typer.echo("Download complete.")

    except typer.Exit:
        raise
    except YTAugError as e:
        typer.echo(f"App error: {e}")
    except Exception as e:
        traceback.print_exc()
        typer.echo(f"Uncaught Exception: {e}")


if __name__ == "__main__":
    app()
