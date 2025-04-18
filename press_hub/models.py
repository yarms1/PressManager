from django.contrib import auth
from django.contrib.auth.models import AbstractUser
from django.db import models


class Topic(models.Model):
    name = models.CharField(max_length=23)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Redactor(AbstractUser):
    years_of_experience = models.IntegerField(default=0)
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="redactor_groups",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="redactor_permissions",
        blank=True
    )

    def __str__(self):
        return self.username


class Newspaper(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True)
    published_date = models.DateTimeField(auto_now_add=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    publishers = models.ManyToManyField(Redactor)

    def __str__(self):
        return self.title
