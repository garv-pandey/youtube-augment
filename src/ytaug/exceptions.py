class YTAugError(Exception):
    """Base exception for all ytaug errors."""


class AuthError(YTAugError):
    """Authentication or authorization failures."""


class ResourceError(YTAugError):
    """Invalid or inaccessible resource (URL, playlist, video)."""


class ResourceNotFoundError(ResourceError):
    """Resource exists but is not accessible (private, deleted, not found)."""


class QuotaError(YTAugError):
    """YouTube Data API quota exceeded."""


class SystemRequirementError(YTAugError):
    """Missing system dependencies (ffmpeg, JS runtime)."""
