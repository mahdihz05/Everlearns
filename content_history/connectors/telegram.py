from typing import List, Dict, Any, Optional
from datetime import datetime
from content_history.models import ContentItem, Platform
from content_history.connectors.base import BaseConnector

class TelegramConnector(BaseConnector):
    """
    Connector for importing content from Telegram channels or groups.
    Requires bot token and chat ID.
    """

    def __init__(self):
        self.config: Dict[str, Any] = {}
        self.bot_token = None
        self.chat_id = None

    @property
    def platform(self) -> Platform:
        return Platform.TELEGRAM

    def configure(self, config: Dict[str, Any]) -> None:
        self.config = config
        self.bot_token = config.get("bot_token")
        self.chat_id = config.get("chat_id")

    def is_configured(self) -> bool:
        return bool(self.bot_token and self.chat_id)

    def normalize_item(self, workspace_id: str, raw_data: Dict[str, Any]) -> ContentItem:
        # Example Telegram message payload
        # { "message_id": 123, "text": "Hello", "date": 1672531200, "chat": {"id": -100...} }

        external_id = str(raw_data.get("message_id", ""))
        text = raw_data.get("text") or raw_data.get("caption", "")

        # Simple heuristic for title if not provided (first line of text)
        title = text.split('\n')[0][:50] + "..." if text else "No Title"

        timestamp = raw_data.get("date")
        created_at = datetime.fromtimestamp(timestamp) if timestamp else datetime.utcnow()

        # In a real app we'd construct a t.me/c/chat_id/message_id url
        source_url = f"https://t.me/c/{self.chat_id}/{external_id}"

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
            raise ValueError("TelegramConnector is not fully configured.")

        # Mocking the response since external API access is unavailable
        # In a real scenario, this would use requests to hit api.telegram.org/bot<token>/getUpdates or similar
        print(f"Mock fetching up to {limit} recent Telegram messages for chat {self.chat_id}")
        return []

    def fetch_by_id(self, workspace_id: str, external_id: str) -> Optional[ContentItem]:
        if not self.is_configured():
            raise ValueError("TelegramConnector is not fully configured.")

        # Mocking the response
        print(f"Mock fetching Telegram message {external_id} from chat {self.chat_id}")
        return None
