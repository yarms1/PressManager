from django import forms
from .models import Topic, Redactor, Newspaper


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter topic name"}),
            "description": forms.Textarea(attrs={"class": "form-control", "placeholder": "Enter topic description"}),
        }


class RedactorForm(forms.ModelForm):
    class Meta:
        model = Redactor
        fields = ["first_name", "last_name", "email"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter first name"}),
            "last_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter last name"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Enter email address"}),
        }


class NewspaperForm(forms.ModelForm):
    class Meta:
        model = Newspaper
        fields = ["title", "published_date", "is_published", "topic", "redactor"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter newspaper title"}),
            "published_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "is_published": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "topic": forms.Select(attrs={"class": "form-select"}),
            "redactor": forms.Select(attrs={"class": "form-select"}),
        }
