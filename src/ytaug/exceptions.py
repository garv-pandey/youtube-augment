class YTMMError(Exception):
    """Base exception for all ytmm errors."""


class AuthError(YTMMError):
    """Authentication or authorization failures."""


class ResourceError(YTMMError):
    """Invalid or inaccessible resource (URL, playlist, video)."""


class ResourceNotFoundError(ResourceError):
    """Resource exists but is not accessible (private, deleted, not found)."""


class QuotaError(YTMMError):
    """YouTube Data API quota exceeded."""


class SystemRequirementError(YTMMError):
    """Missing system dependencies (ffmpeg, JS runtime)."""
