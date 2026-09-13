from typing import List, Dict, Any, Optional
from datetime import datetime
from content_history.models import ContentItem, Platform
from content_history.connectors.base import BaseConnector

class WordPressConnector(BaseConnector):
    """
    Connector for importing content from a WordPress blog.
    Requires base URL and optionally auth credentials (username/app password).
    """

    def __init__(self):
        self.config: Dict[str, Any] = {}
        self.base_url = None
        self.username = None
        self.app_password = None

    @property
    def platform(self) -> Platform:
        return Platform.WORDPRESS

    def configure(self, config: Dict[str, Any]) -> None:
        self.config = config
        self.base_url = config.get("base_url")
        self.username = config.get("username")
        self.app_password = config.get("app_password")

    def is_configured(self) -> bool:
        return bool(self.base_url)

    def normalize_item(self, workspace_id: str, raw_data: Dict[str, Any]) -> ContentItem:
        # Example WP Post payload from WP-JSON API
        # { "id": 123, "date": "2023-01-01T12:00:00", "title": {"rendered": "Hello"}, "content": {"rendered": "<p>World</p>"}, "link": "https://example.com/hello" }

        external_id = str(raw_data.get("id", ""))
        title = raw_data.get("title", {}).get("rendered", "No Title")

        # In a real scenario, we might want to strip HTML tags from the body for text processing
        # using something like BeautifulSoup
        body = raw_data.get("content", {}).get("rendered", "")

        date_str = raw_data.get("date")
        created_at = None
        if date_str:
            try:
                created_at = datetime.fromisoformat(date_str)
            except ValueError:
                pass

        if not created_at:
            created_at = datetime.utcnow()

        source_url = raw_data.get("link", "")

        return ContentItem(
            workspace_id=workspace_id,
            platform=self.platform,
            external_id=external_id,
            title=title,
            body=body,
            source_url=source_url,
            created_at=created_at,
            import_metadata={"raw": raw_data}
        )

    def fetch_recent(self, workspace_id: str, limit: int = 100) -> List[ContentItem]:
        if not self.is_configured():
            raise ValueError("WordPressConnector is not fully configured (missing base_url).")

        # Mocking the response since external API access is unavailable
        print(f"Mock fetching up to {limit} recent WordPress posts from {self.base_url}")
        return []

    def fetch_by_id(self, workspace_id: str, external_id: str) -> Optional[ContentItem]:
        if not self.is_configured():
            raise ValueError("WordPressConnector is not fully configured (missing base_url).")

        # Mocking the response
        print(f"Mock fetching WordPress post {external_id} from {self.base_url}")
        return None
