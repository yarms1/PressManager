from django.contrib import admin
from .models import Topic, Redactor, Newspaper

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("name",)

@admin.register(Redactor)
class RedactorAdmin(admin.ModelAdmin):
    list_display = ("username", "years_of_experience")
    search_fields = ("username",)

@admin.register(Newspaper)
class NewspaperAdmin(admin.ModelAdmin):
    list_display = ("title", "published_date", "topic")
    list_filter = ("published_date", "topic")
    search_fields = ("title",)
