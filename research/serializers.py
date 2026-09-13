from rest_framework import serializers
from .models import ResearchSource, ResearchJob, ResearchItem

class ResearchSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResearchSource
        fields = '__all__'

class ResearchJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResearchJob
        fields = '__all__'

class ResearchItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResearchItem
        fields = '__all__'
