import pytest


@pytest.mark.unit
class TestIsYoutubeUrl:
    @pytest.mark.parametrize(
        "url",
        [
            "https://www.youtube.com/watch?v=abc",
            "https://youtube.com/watch?v=abc",
            "https://music.youtube.com/playlist?list=PL_abc",
            "https://m.youtube.com/watch?v=abc",
            "https://youtu.be/abc",
            "http://www.youtube.com/watch?v=abc",
            "youtube.com/watch?v=abc",
            "www.youtube.com/watch?v=abc",
            "YOUTUBE.COM/watch?v=abc",
            "https://YouTube.com/watch?v=abc",
        ],
    )
    def test_valid_youtube_urls(self, url):
        assert is_youtube_url(url) is True

    @pytest.mark.parametrize(
        "url",
        [
            "https://vimeo.com/123",
            "https://example.com",
            "https://evil.com?domain=youtube.com",
            "https://youtube.com.evil.com/",
            "https://youtube.comm/",
            None,
            "",
            "   ",
            "not-a-url",
            "youtube",
        ],
    )
    def test_invalid_urls(self, url):
        assert is_youtube_url(url) is False
