from django.contrib import admin
from .models import ResearchSource, ResearchJob, ResearchItem, ResearchAnalysis

admin.site.register(ResearchSource)
admin.site.register(ResearchJob)
admin.site.register(ResearchItem)
admin.site.register(ResearchAnalysis)
