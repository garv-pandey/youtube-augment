class YTAugError(Exception):
    """Base exception for all ytaug errors."""


class SystemRequirementError(YTAugError):
    """Missing system dependencies (ffmpeg, JS runtime)."""
