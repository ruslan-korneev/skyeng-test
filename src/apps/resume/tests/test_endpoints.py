import pytest
from model_bakery import baker
from rest_framework import status
from rest_framework.reverse import reverse

from src.apps.resume.models import Resume, ResumeStatus

baker.generators.add("djmoney.models.fields.MoneyField", lambda: "1000.00")


@pytest.mark.django_db
def test_get_resume(api_client, user):
    client = api_client()
    client.force_authenticate(user=user)
    response = client.get(reverse("resume-detail"))
    assert response.status_code == status.HTTP_404_NOT_FOUND
    resume = baker.make(Resume, user=user)
    response = client.get(reverse("resume-detail"))
    assert response.status_code == status.HTTP_200_OK
    assert response.data["title"] == resume.title


@pytest.fixture
def update_resume_data():
    return {
        "title": "Title",
        "status": ResumeStatus.OPEN_FOR_OFFERS,
        "grade": 1,
        "specialty": "backend",
        "salary": "1000.00",
        "education": "Some School",
        "experience": 2,
        "portfolio": "https://github.com/shaggy-axel",
        "email": "shaggybackend@gmail.com",
        "phone": "+381631256805",
    }


@pytest.mark.django_db
def test_update_resume(api_client, user, update_resume_data):
    client = api_client()
    client.force_authenticate(user=user)
    response = client.patch(
        reverse("resume-detail"), data=update_resume_data, format="json"
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND, response.data
    baker.make(Resume, user=user)
    response = client.patch(
        reverse("resume-detail"), data=update_resume_data, format="json"
    )
    assert response.status_code == status.HTTP_200_OK, response.data
    assert response.data == update_resume_data, response.data
