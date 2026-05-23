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
)
from ytaug.youtube import (
    extract_youtube_playlist_id,
    extract_youtube_video_id,
    get_youtube_playlist_url,
    get_youtube_video_url,
    is_youtube_domain,
    extract_youtube_video_or_playlist_id,
)
from ytaug.exceptions import YTAugError

# TODO: save unhandled exceptions in log
# TODO: print traceback of all errors except custom errors

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

    if not is_youtube_domain(url):
        typer.echo("Provided URL is not a valid youtube domain's URL")
        raise typer.Exit(1)

    # get the clean download_url
    video_id = extract_youtube_video_id(url)
    playlist_id = extract_youtube_playlist_id(url)

    try:
        if not video_id and not playlist_id:
            raise YTAugError(f"Unsupported url: {url}")

        # mix playlists are infinite and unviewable on youtube. dont support download for them
        if not video_id and (
            playlist_id.startswith("RD") or playlist_id.startswith("TLGG")  # type: ignore
        ):
            typer.echo("Cannot download mix playlists as they are infinite.")
            raise typer.Exit(1)

        download_url = (
            get_youtube_video_url(video_id)
            if video_id
            else get_youtube_playlist_url(playlist_id)  # type: ignore
        )

        # confirm info of video/playlist and download location
        info = get_url_info_ytdlp(
            url=download_url,  # type:ignore
            js_runtime_config=get_ytdlp_js_runtime_config(),
        )

        if info["type"] == "playlist":
            dest = Path(output, info["title"])
            confirm = typer.confirm(
                f'Download playlist: "{info["title"]}" ({info["video_count"]} tracks) → {dest}'
            )

        elif info["type"] == "video":
            confirm = typer.confirm(f'Download video: "{info["title"]}" → {output}')

        else:
            raise YTAugError("Unexpected 'type' found in url_info.")

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
        typer.echo(traceback.print_exception(e))
        typer.echo(f"Uncaught Exception: {e}")


if __name__ == "__main__":
    app()
