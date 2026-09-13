import json
from .models import ResearchItem, ResearchSource

def export_research_items_json(source: ResearchSource, filepath: str):
    items = ResearchItem.objects.filter(source=source)
    data = []
    for item in items:
        data.append({
            'id': str(item.id),
            'original_content': item.original_content,
            'reference_url': item.reference_url,
            'external_id': item.external_id,
            'analysis_state': item.analysis_state,
        })
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
