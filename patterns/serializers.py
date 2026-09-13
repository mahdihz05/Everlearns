from rest_framework import serializers
from .models import ContentPattern, PatternEvidence

class PatternEvidenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatternEvidence
        fields = '__all__'

class ContentPatternSerializer(serializers.ModelSerializer):
    evidence = PatternEvidenceSerializer(many=True, read_only=True)

    class Meta:
        model = ContentPattern
        fields = '__all__'
