from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager


class User(AbstractUser):
    """Custom user model"""
    email = models.EmailField(unique=True, max_length=150, verbose_name="email address",
                              help_text="Required. Add a valid email address.")
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    tg_chat_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="Tg chat ID",
                                  help_text="Required. Add a valid tg chat ID.")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def save(self, *args, **kwargs):
        if not self.username and self.email:
            self.username = self.email
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["email"]

    def __str__(self):
        return self.email
