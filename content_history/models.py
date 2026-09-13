import uuid
from datetime import datetime
from typing import Optional, Dict, Any, List
from enum import Enum


class Platform(Enum):
    TELEGRAM = "telegram"
    LINKEDIN = "linkedin"
    WORDPRESS = "wordpress"
    UNKNOWN = "unknown"


class ImportStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class ContentItem:
    def __init__(
        self,
        workspace_id: str,
        platform: Platform,
        external_id: str,
        title: Optional[str] = None,
        body: Optional[str] = None,
        source_url: Optional[str] = None,
        author: Optional[str] = None,
        media_references: Optional[List[Dict[str, Any]]] = None,
        created_at: Optional[datetime] = None,
        import_metadata: Optional[Dict[str, Any]] = None,
        analysis_metadata: Optional[Dict[str, Any]] = None,
        public_id: Optional[str] = None,
    ):
        self.public_id = public_id or str(uuid.uuid4())
        self.workspace_id = workspace_id
        self.platform = platform
        self.external_id = external_id

        # Content
        self.title = title
        self.body = body
        self.source_url = source_url
        self.author = author
        self.media_references = media_references or []

        # Timestamps
        self.created_at = created_at or datetime.utcnow()
        self.imported_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

        # Metadata
        self.import_metadata = import_metadata or {}
        self.analysis_metadata = analysis_metadata or {}

        # Status
        self.import_status = ImportStatus.PENDING
        self.error_message = None

        # Provenance
        self.provenance = {
            "source": platform.value,
            "external_id": external_id,
            "imported_at": self.imported_at.isoformat()
        }

    def mark_completed(self):
        self.import_status = ImportStatus.COMPLETED
        self.updated_at = datetime.utcnow()

    def mark_failed(self, error: str):
        self.import_status = ImportStatus.FAILED
        self.error_message = error
        self.updated_at = datetime.utcnow()

    def update_analysis(self, metadata: Dict[str, Any]):
        self.analysis_metadata.update(metadata)
        self.updated_at = datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "public_id": self.public_id,
            "workspace_id": self.workspace_id,
            "platform": self.platform.value,
            "external_id": self.external_id,
            "title": self.title,
            "body": self.body,
            "source_url": self.source_url,
            "author": self.author,
            "media_references": self.media_references,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "imported_at": self.imported_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "import_metadata": self.import_metadata,
            "analysis_metadata": self.analysis_metadata,
            "import_status": self.import_status.value,
            "error_message": self.error_message,
            "provenance": self.provenance
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ContentItem":
        item = cls(
            workspace_id=data["workspace_id"],
            platform=Platform(data["platform"]),
            external_id=data["external_id"],
            title=data.get("title"),
            body=data.get("body"),
            source_url=data.get("source_url"),
            author=data.get("author"),
            media_references=data.get("media_references", []),
            created_at=datetime.fromisoformat(data["created_at"]) if data.get("created_at") else None,
            import_metadata=data.get("import_metadata", {}),
            analysis_metadata=data.get("analysis_metadata", {}),
            public_id=data.get("public_id"),
        )
        item.imported_at = datetime.fromisoformat(data["imported_at"])
        item.updated_at = datetime.fromisoformat(data["updated_at"])
        item.import_status = ImportStatus(data["import_status"])
        item.error_message = data.get("error_message")
        item.provenance = data.get("provenance", {})
        return item


class WorkspaceContentHistory:
    """
    Represents the aggregate history for a workspace.
    For this assignment, we use a simple in-memory representation.
    """
    def __init__(self, workspace_id: str):
        self.workspace_id = workspace_id
        self.items: Dict[str, ContentItem] = {}  # external_id -> ContentItem

    def add_item(self, item: ContentItem) -> bool:
        """Returns True if newly added, False if updated/duplicate"""
        key = f"{item.platform.value}:{item.external_id}"
        is_new = key not in self.items
        self.items[key] = item
        return is_new

    def get_items(self) -> List[ContentItem]:
        return list(self.items.values())

    def get_items_by_platform(self, platform: Platform) -> List[ContentItem]:
        return [item for item in self.items.values() if item.platform == platform]
