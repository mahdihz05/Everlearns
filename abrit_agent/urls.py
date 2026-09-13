from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WorkspaceViewSet, AgentSessionViewSet, ToolCallViewSet

router = DefaultRouter()
router.register(r'workspaces', WorkspaceViewSet)
router.register(r'sessions', AgentSessionViewSet)
router.register(r'tool-calls', ToolCallViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
