from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

class RecommendationService:
    def __init__(self, history_adapter, memory_adapter):
        self.history = history_adapter
        self.memory = memory_adapter

    def recommend_schedule(self, ideas: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Takes a list of ideas and returns them with recommended publishing dates,
        times, platforms, and content types based on history and spacing rules.
        """
        recommended_items = []
        base_date = datetime.now() + timedelta(days=1)

        for idx, idea in enumerate(ideas):
            # Recommend a date, adding spacing to avoid similar content too close
            # Simple mock logic: space items by 2 days
            proposed_date = base_date + timedelta(days=idx * 2)

            item = {
                "source_idea_id": idea.get("id"),
                "target_platform": idea.get("suggested_platform", "LinkedIn"),
                "content_type": idea.get("suggested_content_type", "Post"),
                "content_form": "Text",
                "priority": idea.get("priority", 0),
                "proposed_date": proposed_date,
                "sequence_order": idx,
                "series_grouping": idea.get("series_group_relation"),
                "relation_to_other_items": f"Item {idx} in planned sequence",
                "status": "planned"
            }
            recommended_items.append(item)

        return recommended_items

    def group_into_series(self, ideas: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Groups related ideas into series."""
        series_map = {}
        for idea in ideas:
            group = idea.get("series_group_relation", "Standalone")
            if group not in series_map:
                series_map[group] = []
            series_map[group].append(idea)
        return series_map
