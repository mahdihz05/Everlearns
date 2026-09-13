from rest_framework import viewsets
from .models import ResearchSource, ResearchJob, ResearchItem
from .serializers import ResearchSourceSerializer, ResearchJobSerializer, ResearchItemSerializer

class ResearchSourceViewSet(viewsets.ModelViewSet):
    queryset = ResearchSource.objects.all()
    serializer_class = ResearchSourceSerializer

class ResearchJobViewSet(viewsets.ModelViewSet):
    queryset = ResearchJob.objects.all()
    serializer_class = ResearchJobSerializer

class ResearchItemViewSet(viewsets.ModelViewSet):
    queryset = ResearchItem.objects.all()
    serializer_class = ResearchItemSerializer
