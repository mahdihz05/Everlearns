from typing import List, Dict, Any, Optional
from datetime import datetime
from content_history.models import ContentItem, Platform
from content_history.connectors.base import BaseConnector

class LinkedInConnector(BaseConnector):
    """
    Connector for importing content from LinkedIn profiles or company pages.
    Requires an access token and an author/organization urn.
    """

    def __init__(self):
        self.config: Dict[str, Any] = {}
        self.access_token = None
        self.author_urn = None

    @property
    def platform(self) -> Platform:
        return Platform.LINKEDIN

    def configure(self, config: Dict[str, Any]) -> None:
        self.config = config
        self.access_token = config.get("access_token")
        self.author_urn = config.get("author_urn")

    def is_configured(self) -> bool:
        return bool(self.access_token and self.author_urn)

    def normalize_item(self, workspace_id: str, raw_data: Dict[str, Any]) -> ContentItem:
        # Example LinkedIn post payload from UgcPosts API
        # { "id": "urn:li:share:123", "specificContent": {"com.linkedin.ugc.ShareContent": {"shareCommentary": {"text": "Hello"}}}, "created": {"time": 1672531200000} }

        external_id = raw_data.get("id", "")

        # Extract text (highly dependent on the specific LinkedIn API version/endpoint)
        try:
            text = raw_data["specificContent"]["com.linkedin.ugc.ShareContent"]["shareCommentary"]["text"]
        except KeyError:
            text = ""

        title = text.split('\n')[0][:50] + "..." if text else "No Title"

        timestamp_ms = raw_data.get("created", {}).get("time")
        created_at = datetime.fromtimestamp(timestamp_ms / 1000.0) if timestamp_ms else datetime.utcnow()

        source_url = f"https://www.linkedin.com/feed/update/{external_id}"

        return ContentItem(
            workspace_id=workspace_id,
            platform=self.platform,
            external_id=external_id,
            title=title,
            body=text,
            source_url=source_url,
            created_at=created_at,
            import_metadata={"raw": raw_data}
        )

    def fetch_recent(self, workspace_id: str, limit: int = 100) -> List[ContentItem]:
        if not self.is_configured():
            raise ValueError("LinkedInConnector is not fully configured.")

        # Mocking the response since external API access is unavailable
        print(f"Mock fetching up to {limit} recent LinkedIn posts for {self.author_urn}")
        return []

    def fetch_by_id(self, workspace_id: str, external_id: str) -> Optional[ContentItem]:
        if not self.is_configured():
            raise ValueError("LinkedInConnector is not fully configured.")

        # Mocking the response
        print(f"Mock fetching LinkedIn post {external_id}")
        return None
