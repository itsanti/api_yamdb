from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    MODER = 'moderator'
    ADMIN = 'admin'
    ROLE_CHOICES = (
        (USER, 'user'),
        (MODER, 'moderator'),
        (ADMIN, 'admin'),
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        blank=False
    )
    bio = models.TextField(
        default='Здесь будет ваша биография.'
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=USER,
    )

    @property
    def is_moderator(self):
        return bool(self.role == User.MODER)

    @property
    def is_admin(self):
        return bool(self.is_superuser or (self.role == self.ADMIN))
