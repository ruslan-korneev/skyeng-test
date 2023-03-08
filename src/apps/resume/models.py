from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from djmoney.models.fields import MoneyField

User = get_user_model()


class ResumeStatus(models.IntegerChoices):
    OPEN_TO_WORK = 0, "Open to work"
    OPEN_FOR_OFFERS = 1, "Open for offers"
    HAS_A_JOB = 2, "Has a job"


class Resume(models.Model):
    title = models.CharField(max_length=64)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.PositiveSmallIntegerField(
        choices=ResumeStatus.choices, default=ResumeStatus.OPEN_TO_WORK
    )
    # не понял, что именно означает поле grade, но думаю это число)
    grade = models.PositiveSmallIntegerField()
    specialty = models.CharField(max_length=32)
    salary = MoneyField(max_digits=14, decimal_places=2, default_currency="USD")
    # education я бы сделал educations: m2m -> model Eduction(title, start, end, description)
    education = models.CharField(max_length=64)
    experience = models.PositiveSmallIntegerField(_("Years of experience"))
    portfolio = models.URLField(_("Link to github account"))
    email = models.EmailField()
    phone = models.CharField(
        max_length=32
    )  # i would use django phonenumber field, there's validations e.t.c
