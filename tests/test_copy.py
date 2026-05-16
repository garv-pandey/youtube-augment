import pytest
from unittest.mock import MagicMock, patch
from ytmm.copy import add_videos_to_playlist, create_playlist
from ytmm.exceptions import YTMMError


class TestAddVideosToPlaylist:
    """add_videos_to_playlist() — adds videos to a YouTube playlist via API."""

    def test_adds_all_videos(self):
        youtube = MagicMock()
        youtube.playlistItems.return_value.insert.return_value.execute.return_value = {}

        result = add_videos_to_playlist(
            credentials=MagicMock(),
            playlist_id="PL_abc123",
            video_ids=["vid1", "vid2", "vid3"],
            youtube=youtube,
        )

        assert result == 3
        assert youtube.playlistItems.return_value.insert.call_count == 3
        for i, vid in enumerate(["vid1", "vid2", "vid3"]):
            _, kwargs = youtube.playlistItems.return_value.insert.call_args_list[i]
            assert kwargs["body"]["snippet"]["resourceId"]["videoId"] == vid

    def test_single_video(self):
        youtube = MagicMock()
        youtube.playlistItems.return_value.insert.return_value.execute.return_value = {}

        result = add_videos_to_playlist(
            credentials=MagicMock(),
            playlist_id="PL_abc",
            video_ids=["vid1"],
            youtube=youtube,
        )

        assert result == 1
        youtube.playlistItems.return_value.insert.assert_called_once()

    def test_insert_failure_raises_ytmmerror(self):
        youtube = MagicMock()
        youtube.playlistItems.return_value.insert.return_value.execute.side_effect = (
            Exception("API error")
        )

        with pytest.raises(YTMMError):
            add_videos_to_playlist(
                credentials=MagicMock(),
                playlist_id="PL_abc",
                video_ids=["vid1"],
                youtube=youtube,
            )

    def test_discovery_failure_raises_ytmmerror(self):
        with patch("ytmm.copy.discovery.build", side_effect=Exception("Network error")):
            with pytest.raises(YTMMError):
                add_videos_to_playlist(
                    credentials=MagicMock(),
                    playlist_id="PL_abc",
                    video_ids=["vid1"],
                )


class TestCreatePlaylist:
    """create_playlist() — creates a YouTube playlist via API."""

    def test_success_returns_playlist_id(self):
        youtube = MagicMock()
        youtube.playlists.return_value.insert.return_value.execute.return_value = {
            "id": "PL_abc123"
        }

        result = create_playlist(
            credentials=MagicMock(),
            title="My Playlist",
            youtube=youtube,
        )

        assert result == "PL_abc123"

    def test_sets_privacy_private_by_default(self):
        youtube = MagicMock()
        youtube.playlists.return_value.insert.return_value.execute.return_value = {
            "id": "PL_abc"
        }

        create_playlist(
            credentials=MagicMock(),
            title="Test",
            youtube=youtube,
        )

        _, kwargs = youtube.playlists.return_value.insert.call_args
        assert kwargs["body"]["status"]["privacyStatus"] == "private"

    def test_sets_privacy_public(self):
        youtube = MagicMock()
        youtube.playlists.return_value.insert.return_value.execute.return_value = {
            "id": "PL_abc"
        }

        create_playlist(
            credentials=MagicMock(),
            title="Test",
            is_public=True,
            youtube=youtube,
        )

        _, kwargs = youtube.playlists.return_value.insert.call_args
        assert kwargs["body"]["status"]["privacyStatus"] == "public"

    def test_success_without_description(self):
        youtube = MagicMock()
        youtube.playlists.return_value.insert.return_value.execute.return_value = {
            "id": "PL_abc"
        }

        create_playlist(
            credentials=MagicMock(),
            title="Test",
            description="",
            youtube=youtube,
        )

        _, kwargs = youtube.playlists.return_value.insert.call_args
        assert kwargs["body"]["snippet"]["description"] == ""

    def test_api_error_raises_ytmmerror(self):
        youtube = MagicMock()
        youtube.playlists.return_value.insert.return_value.execute.side_effect = (
            Exception("API error")
        )

        with pytest.raises(YTMMError):
            create_playlist(
                credentials=MagicMock(),
                title="Test",
                youtube=youtube,
            )

    def test_discovery_failure_raises_ytmmerror(self):
        with patch("ytmm.copy.discovery.build", side_effect=Exception("Network error")):
            with pytest.raises(YTMMError):
                create_playlist(
                    credentials=MagicMock(),
                    title="Test",
                )
