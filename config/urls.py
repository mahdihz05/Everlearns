from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from research.views import ResearchSourceViewSet, ResearchJobViewSet, ResearchItemViewSet
from patterns.views import ContentPatternViewSet

router = DefaultRouter()
router.register(r'sources', ResearchSourceViewSet)
router.register(r'jobs', ResearchJobViewSet)
router.register(r'items', ResearchItemViewSet)
router.register(r'patterns', ContentPatternViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v2/", include(router.urls)),
]
