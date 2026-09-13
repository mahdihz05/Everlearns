from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from content_history.models import ContentItem, Platform


class BaseConnector(ABC):
    """
    Base interface for all platform connectors to ensure consistent data ingestion.
    """

    @property
    @abstractmethod
    def platform(self) -> Platform:
        """Returns the platform this connector handles."""
        pass

    @abstractmethod
    def configure(self, config: Dict[str, Any]) -> None:
        """
        Configure the connector with necessary credentials and settings.
        Since we might not have real credentials, this stores what's provided.
        """
        pass

    @abstractmethod
    def is_configured(self) -> bool:
        """Returns True if the connector has minimum required configuration to run."""
        pass

    @abstractmethod
    def fetch_recent(self, workspace_id: str, limit: int = 100) -> List[ContentItem]:
        """
        Fetch recent content from the source and normalize it to ContentItem objects.
        """
        pass

    @abstractmethod
    def fetch_by_id(self, workspace_id: str, external_id: str) -> Optional[ContentItem]:
        """
        Fetch a specific item by its external ID and normalize it.
        """
        pass

    def normalize_item(self, workspace_id: str, raw_data: Dict[str, Any]) -> ContentItem:
        """
        Helper method that should be implemented or overridden by subclasses
        to convert raw platform data into a standard ContentItem.
        """
        raise NotImplementedError("Subclasses must implement normalize_item")
