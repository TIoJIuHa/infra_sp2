from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(
        ("Электронная почта"),
        unique=True,
    )
    bio = models.TextField(
        verbose_name="Биография",
        blank=True,
    )

    ROLE_CHOICES = [
        ("user", "user"),
        ("moderator", "moderator"),
        ("admin", "admin"),
    ]

    role = models.CharField(
        verbose_name="Пользовательская роль",
        max_length=9,
        choices=ROLE_CHOICES,
        default="user",
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    @property
    def is_admin(self):
        return self.is_superuser or self.role == "admin"

    @property
    def is_moderator(self):
        return self.role == "moderator"

    @property
    def is_user(self):
        return self.role == "user"
