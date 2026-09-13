import json
from .models import ContentPattern

def export_patterns_json(filepath: str):
    patterns = ContentPattern.objects.all()
    data = []
    for pattern in patterns:
        data.append({
            'name': pattern.name,
            'description': pattern.description,
            'category': pattern.category,
            'status': pattern.status,
            'tags': pattern.tags,
            'ai_consumable_representation': pattern.ai_consumable_representation,
        })
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
