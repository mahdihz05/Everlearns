import logging
from typing import Dict, Any, List
from content_history.models import WorkspaceContentHistory, Platform
from content_history.connectors.base import BaseConnector

logger = logging.getLogger(__name__)

class ImportPipeline:
    """
    Handles idempotent, workspace-scoped, duplicate-safe imports.
    Capable of reporting progress and handling failures gracefully.
    """

    def __init__(self, workspace_id: str, history_store: WorkspaceContentHistory):
        self.workspace_id = workspace_id
        self.history_store = history_store

    def run_import(self, connector: BaseConnector, limit: int = 100) -> Dict[str, Any]:
        """
        Runs the import for a given connector, capturing progress and results.
        Returns a summary report.
        """
        report = {
            "workspace_id": self.workspace_id,
            "platform": connector.platform.value,
            "total_fetched": 0,
            "new_items_added": 0,
            "duplicates_skipped": 0,
            "failures": 0,
            "errors": []
        }

        try:
            logger.info(f"Starting import for workspace {self.workspace_id} via {connector.platform.value}")
            items = connector.fetch_recent(self.workspace_id, limit=limit)
            report["total_fetched"] = len(items)

            for item in items:
                try:
                    # History store handles duplicate checking and adds the item
                    is_new = self.history_store.add_item(item)
                    if is_new:
                        report["new_items_added"] += 1
                        item.mark_completed()
                    else:
                        report["duplicates_skipped"] += 1
                except Exception as e:
                    report["failures"] += 1
                    report["errors"].append({"external_id": item.external_id, "error": str(e)})
                    item.mark_failed(str(e))

        except Exception as e:
            logger.error(f"Import pipeline failed for {connector.platform.value}: {str(e)}")
            report["errors"].append({"fatal": True, "error": str(e)})

        logger.info(f"Import completed: {report}")
        return report

    def get_progress(self) -> Dict[str, Any]:
        """
        In a real asynchronous environment (e.g. Celery), this would check the current job status.
        Here we just return the counts from our store.
        """
        return {
            "status": "idle",
            "total_items_in_history": len(self.history_store.get_items())
        }
