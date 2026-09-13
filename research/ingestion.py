import json
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from research.models import ResearchSource, ResearchJob, ResearchItem, ProcessingState

class IngestionAdapter(ABC):
    """
    Base interface for ingesting content from different sources.
    """
    def __init__(self, source: ResearchSource):
        self.source = source
        self.credentials_required = []

    @abstractmethod
    def fetch_data(self) -> List[Dict[str, Any]]:
        """
        Fetch raw data from the platform.
        Returns a list of raw items.
        """
        pass

    @abstractmethod
    def normalize_item(self, raw_item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize a raw item into a structured format containing at minimum:
        - original_content
        - reference_url (optional)
        - external_id (optional)
        """
        pass

    def run_ingestion(self, job: ResearchJob):
        """
        Runs the full ingestion flow for a given job.
        """
        try:
            job.state = ProcessingState.IN_PROGRESS
            job.save()

            raw_data = self.fetch_data()
            for raw_item in raw_data:
                normalized = self.normalize_item(raw_item)
                ResearchItem.objects.create(
                    job=job,
                    source=self.source,
                    original_content=normalized.get('original_content', ''),
                    reference_url=normalized.get('reference_url'),
                    external_id=normalized.get('external_id')
                )

            job.state = ProcessingState.COMPLETED
            job.save()
        except Exception as e:
            job.state = ProcessingState.FAILED
            job.error_metadata = {"error": str(e)}
            job.save()

class TelegramAdapter(IngestionAdapter):
    def __init__(self, source: ResearchSource):
        super().__init__(source)
        self.credentials_required = ['telegram_api_id', 'telegram_api_hash']

    def fetch_data(self) -> List[Dict[str, Any]]:
        # TODO: Implement actual MTProto or Bot API integration when credentials are provided
        return []

    def normalize_item(self, raw_item: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'original_content': raw_item.get('text', ''),
            'external_id': str(raw_item.get('id', '')),
        }

class LinkedInAdapter(IngestionAdapter):
    def __init__(self, source: ResearchSource):
        super().__init__(source)
        self.credentials_required = ['linkedin_access_token']

    def fetch_data(self) -> List[Dict[str, Any]]:
        # TODO: Implement LinkedIn API integration
        return []

    def normalize_item(self, raw_item: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'original_content': raw_item.get('text', ''),
            'reference_url': raw_item.get('url', ''),
        }

class WordPressAdapter(IngestionAdapter):
    def __init__(self, source: ResearchSource):
        super().__init__(source)
        self.credentials_required = ['wp_api_url']

    def fetch_data(self) -> List[Dict[str, Any]]:
        # TODO: Implement WordPress REST API integration
        return []

    def normalize_item(self, raw_item: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'original_content': raw_item.get('content', {}).get('rendered', ''),
            'reference_url': raw_item.get('link', ''),
            'external_id': str(raw_item.get('id', '')),
        }

class ManualJSONImporter(IngestionAdapter):
    def __init__(self, source: ResearchSource, json_data: str):
        super().__init__(source)
        self.json_data = json_data

    def fetch_data(self) -> List[Dict[str, Any]]:
        try:
            data = json.loads(self.json_data)
            if isinstance(data, list):
                return data
            return [data]
        except json.JSONDecodeError:
            return []

    def normalize_item(self, raw_item: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'original_content': raw_item.get('content', ''),
            'reference_url': raw_item.get('url', ''),
            'external_id': raw_item.get('id', ''),
        }

def start_ingestion_pipeline(job: ResearchJob, json_data: str = None):
    """
    Factory / Orchestrator for kicking off ingestion.
    """
    platform = job.source.platform
    if platform == 'TELEGRAM_CHANNEL' or platform == 'TELEGRAM_GROUP':
        adapter = TelegramAdapter(job.source)
    elif platform == 'LINKEDIN':
        adapter = LinkedInAdapter(job.source)
    elif platform == 'WORDPRESS':
        adapter = WordPressAdapter(job.source)
    elif platform == 'MANUAL' and json_data:
        adapter = ManualJSONImporter(job.source, json_data)
    else:
        raise ValueError(f"Unsupported platform or missing parameters: {platform}")

    adapter.run_ingestion(job)
