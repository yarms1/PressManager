from django.urls import path
from . import views

app_name = "press_hub"

urlpatterns = [
    path("", views.home, name="home"),
    path("topics/", views.topic_list, name="topic-list"),
    path("newspapers/", views.newspaper_list, name="newspaper-list"),
    path("redactors/", views.redactor_list, name="redactor-list"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("topics/<int:pk>/", views.topic_detail, name="topic-detail"),
    path("redactors/<int:pk>/", views.redactor_detail, name="redactor-detail"),
]