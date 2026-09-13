from typing import Dict, Any
from content_history.models import ContentItem

# Note: In a real Django REST Framework application, these would inherit from serializers.Serializer
# Here we define mock serializers that convert object to dict (similar to what our to_dict does).

class ContentItemSerializer:
    """
    Serializes a ContentItem to dictionary.
    """
    @staticmethod
    def serialize(item: ContentItem) -> Dict[str, Any]:
        return item.to_dict()

    @staticmethod
    def serialize_many(items: list[ContentItem]) -> list[Dict[str, Any]]:
        return [item.to_dict() for item in items]

class ImportReportSerializer:
    """
    Serializes an import report.
    """
    @staticmethod
    def serialize(report: Dict[str, Any]) -> Dict[str, Any]:
        # Basic validation could happen here
        return report
