from typing import Dict, Any, List
from content_history.models import WorkspaceContentHistory, Platform
from content_history.api.serializers import ContentItemSerializer, ImportReportSerializer
from content_history.connectors.base import BaseConnector
from content_history.pipeline.import_pipeline import ImportPipeline

# Note: In a real Django setup, these would be DRF APIViews.
# Here we implement view controllers that return dict representations.

class ContentHistoryView:
    def __init__(self, history_store: WorkspaceContentHistory):
        self.history_store = history_store

    def list_history(self, platform_str: str = None) -> List[Dict[str, Any]]:
        """
        List history, optionally filtered by platform.
        """
        if platform_str:
            try:
                platform = Platform(platform_str.lower())
                items = self.history_store.get_items_by_platform(platform)
            except ValueError:
                return {"error": f"Invalid platform: {platform_str}"} # type: ignore
        else:
            items = self.history_store.get_items()

        return ContentItemSerializer.serialize_many(items)

    def inspect_item(self, public_id: str) -> Dict[str, Any]:
        """
        Inspect a specific item by its public ID.
        """
        for item in self.history_store.get_items():
            if item.public_id == public_id:
                return ContentItemSerializer.serialize(item)
        return {"error": "Item not found"}

    def get_import_status(self) -> Dict[str, Any]:
        """
        Show import statuses/errors across the history.
        """
        items = self.history_store.get_items()

        failed = [item for item in items if item.import_status.value == "failed"]
        completed = [item for item in items if item.import_status.value == "completed"]

        return {
            "total_items": len(items),
            "completed_count": len(completed),
            "failed_count": len(failed),
            "errors": [{"public_id": item.public_id, "error": item.error_message} for item in failed]
        }

class ImportTriggerView:
    def __init__(self, history_store: WorkspaceContentHistory):
        self.history_store = history_store

    def trigger_import(self, connector: BaseConnector, limit: int = 100) -> Dict[str, Any]:
        """
        Trigger an import for a specific connector.
        """
        pipeline = ImportPipeline(self.history_store.workspace_id, self.history_store)
        report = pipeline.run_import(connector, limit=limit)
        return ImportReportSerializer.serialize(report)
