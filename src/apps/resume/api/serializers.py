from rest_framework import serializers

from src.apps.resume.models import Resume


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = (
            "title",
            "status",
            "grade",
            "specialty",
            "salary",
            "education",
            "experience",
            "portfolio",
            "email",
            "phone",
        )
