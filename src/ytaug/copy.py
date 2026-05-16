from typing import Optional
from googleapiclient import discovery
from google.oauth2.credentials import Credentials

from ytaug.exceptions import YTAugError


def create_playlist(
    credentials: Credentials,
    title: str,
    description: Optional[str] = "",
    is_public: Optional[bool] = False,
    youtube=None,
) -> str:
    """
    Creates a new playlist on the authorized user's YouTube account.

    Returns:
        The ID of the newly created playlist if successful, else None.
    """
    try:
        if youtube is None:
            youtube = discovery.build("youtube", "v3", credentials=credentials)

    except Exception as e:
        raise YTAugError("Error in create_playlist") from e

    # 2. Define the privacy status string
    privacy_status = "public" if is_public else "private"

    # 3. Construct the request body
    # 'snippet' contains the metadata, 'status' contains privacy
    body = {
        "snippet": {
            "title": title,
            "description": description,
            "defaultLanguage": "en",
        },
        "status": {"privacyStatus": privacy_status},
    }

    try:
        # 4. Execute the insert request
        # We request 'snippet' and 'status' back in the response to confirm creation
        request = youtube.playlists().insert(part="snippet,status", body=body)
        response = request.execute()

    except Exception as e:
        raise YTAugError("Error in create_playlist") from e

    # 5. Return the new Playlist ID
    return response.get("id")


def add_videos_to_playlist(
    credentials: Credentials, playlist_id: str, video_ids: list[str], youtube=None
) -> int:
    """
    Adds a list of videos to a specified playlist.

    Quota Cost: 50 units per video.
    """
    try:
        if youtube is None:
            youtube = discovery.build("youtube", "v3", credentials=credentials)

    except Exception as e:
        raise YTAugError("error in add_videos_to_playlist") from e

    added_count = 0

    for v_id in video_ids:
        body = {
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {"kind": "youtube#video", "videoId": v_id},
            }
        }

        try:
            youtube.playlistItems().insert(part="snippet", body=body).execute()

        except Exception as e:
            raise YTAugError("error in add_videos_to_playlist") from e

        added_count += 1

    return added_count
