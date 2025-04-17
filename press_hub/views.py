from django.shortcuts import render, redirect, get_object_or_404
from .models import Topic, Newspaper, Redactor
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User


def home(request: HttpRequest) -> HttpResponse:
    newspapers = Newspaper.objects.all().order_by('-published_date')[:5]
    total_newspapers = Newspaper.objects.count()
    total_redactors = Redactor.objects.count()

    return render(request, "press_hub/home.html", {
        "newspapers": newspapers,
        "total_newspapers": total_newspapers,
        "total_redactors": total_redactors
    })


def topic_list(request: HttpRequest) -> HttpResponse:
    topics = Topic.objects.all()
    paginator = Paginator(topics, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    previous_page = page_obj.previous_page_number() if page_obj.has_previous() else None
    next_page = page_obj.next_page_number() if page_obj.has_next() else None
    last_page = paginator.num_pages

    return render(request, "press_hub/topic_list.html", {
        'topics': page_obj,
        'previous_page': previous_page,
        'next_page': next_page,
        'last_page': last_page
    })


def newspaper_list(request: HttpRequest) -> HttpResponse:
    newspapers = Newspaper.objects.all().order_by('-published_date')
    paginator = Paginator(newspapers, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "press_hub/newspaper_list.html", {"page_obj": page_obj})


def redactor_list(request: HttpRequest) -> HttpResponse:
    redactors = Redactor.objects.all()
    paginator = Paginator(redactors, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    previous_page = page_obj.previous_page_number() if page_obj.has_previous() else None
    next_page = page_obj.next_page_number() if page_obj.has_next() else None
    last_page = paginator.num_pages

    return render(request, "press_hub/redactor_list.html", {
        "page_obj": page_obj,
        "previous_page": previous_page,
        "next_page": next_page,
        "last_page": last_page
    })


def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("press_hub:home")
            else:
                form.add_error(None, "Invalid credentials")
    else:
        form = AuthenticationForm()

    return render(request, "press_hub/login.html", {"form": form})


def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect("press_hub:home")


def topic_detail(request: HttpRequest, pk: int) -> HttpResponse:
    topic = get_object_or_404(Topic, pk=pk)
    return render(request, "press_hub/topic_detail.html", {"topic": topic})


def redactor_detail(request: HttpRequest, pk: int) -> HttpResponse:
    topic = get_object_or_404(Topic, pk=pk)
    return render(request, "press_hub/redactor_detail.html", {"topic": topic})
