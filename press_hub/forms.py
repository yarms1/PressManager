from django import forms
from django.contrib.auth.models import User
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
        exclude = ["published_date"]
        fields = ["title", "published_date", "topic", "publishers"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter newspaper title"}),
            "topic": forms.Select(attrs={"class": "form-select"}),
            "publishers": forms.Select(attrs={"class": "form-select"}),
        }


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]

        if commit:
            user.save()
        return user
