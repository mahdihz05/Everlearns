from typing import Dict, Any, Optional
from abc import ABC, abstractmethod

class PatternLibraryAdapter(ABC):
    """Interface to consume visual research patterns."""

    @abstractmethod
    def get_pattern_context(self, pattern_id: str) -> Dict[str, Any]:
        """
        Retrieves visual constraints/styles defined by the research pattern.
        Returns a dictionary to be merged into pattern_library_context.
        """
        pass

class MockPatternLibraryAdapter(PatternLibraryAdapter):
    """Mock implementation for testing/fallback."""

    def get_pattern_context(self, pattern_id: str) -> Dict[str, Any]:
        if pattern_id == "minimalist_ad":
            return {
                "style_pattern": "flat design, negative space",
                "layout_pattern": "central subject, rule of thirds"
            }
        return {}


class MediaStorageAdapter(ABC):
    """Interface to integrate generated media with the project's media storage."""

    @abstractmethod
    def store_media(self, file_content: bytes, filename: str, metadata: Dict[str, Any]) -> str:
        """
        Stores the generated media and returns a persistent URI/path.
        Includes saving metadata like provider, dimensions, workspace.
        """
        pass

    @abstractmethod
    def register_metadata(self, media_uri: str, metadata: Dict[str, Any]) -> bool:
        """
        Updates or registers metadata for an existing stored media file.
        """
        pass

class MockMediaStorageAdapter(MediaStorageAdapter):
    """Mock implementation for storing media locally or simulating storage."""

    def store_media(self, file_content: bytes, filename: str, metadata: Dict[str, Any]) -> str:
        # In a real app, this might upload to S3 and save to a local DB model.
        # For now, we simulate success.
        print(f"MockMediaStorage: Stored {filename} with metadata {metadata}")
        return f"s3://mock-bucket/generated/{filename}"

    def register_metadata(self, media_uri: str, metadata: Dict[str, Any]) -> bool:
        print(f"MockMediaStorage: Registered metadata for {media_uri}")
        return True
