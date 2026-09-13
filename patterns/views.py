from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import ContentPattern
from .serializers import ContentPatternSerializer

class ContentPatternViewSet(viewsets.ModelViewSet):
    queryset = ContentPattern.objects.all()
    serializer_class = ContentPatternSerializer

    def get_queryset(self):
        queryset = ContentPattern.objects.all()

        # Filtering intended for AI consumption / downstream use
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category=category)

        status = self.request.query_params.get('status', None)
        if status:
            queryset = queryset.filter(status=status)

        return queryset

    @action(detail=True, methods=['post'])
    def promote(self, request, pk=None):
        pattern = self.get_object()
        from .services import promote_pattern
        if promote_pattern(pattern):
            return Response({'status': 'promoted'})
        return Response({'status': 'already promoted or invalid state'}, status=400)
