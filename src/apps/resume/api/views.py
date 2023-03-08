from django.shortcuts import get_object_or_404
from rest_framework import mixins
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from src.apps.resume.api.serializers import ResumeSerializer
from src.apps.resume.models import Resume


class ResumeViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, GenericViewSet):
    serializer_class = ResumeSerializer
    queryset = Resume.objects.all()

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        filter_kwargs = {"user": self.request.user}
        return get_object_or_404(queryset, **filter_kwargs)
