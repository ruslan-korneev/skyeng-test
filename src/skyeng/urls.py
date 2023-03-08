from django.contrib import admin
from django.urls import path, include

from src.apps.resume.api.views import ResumeViewSet

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/v1/resume/",
        ResumeViewSet.as_view({"get": "retrieve", "patch": "partial_update"}),
        name="resume-detail",
    ),
]
