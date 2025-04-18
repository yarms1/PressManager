from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import NewspaperForm, TopicForm, UserRegistrationForm
from .models import Topic, Newspaper, Redactor
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.contrib import messages


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
    topics = Topic.objects.all().order_by("name")
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
    newspapers = Newspaper.objects.all().order_by("-published_date")
    paginator = Paginator(newspapers, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    previous_page = page_obj.previous_page_number() if page_obj.has_previous() else None
    next_page = page_obj.next_page_number() if page_obj.has_next() else None
    last_page = paginator.num_pages

    return render(request, "press_hub/newspaper_list.html", {
        "page_obj": page_obj,
        "previous_page": previous_page,
        "next_page": next_page,
        "last_page": last_page
    })


def redactor_list(request: HttpRequest) -> HttpResponse:
    redactors = Redactor.objects.all().order_by("-years_of_experience")
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
    redactor = get_object_or_404(Redactor, pk=pk)
    return render(request, "press_hub/redactor_detail.html", {"redactor": redactor})


def newspaper_detail(request: HttpRequest, pk: int) -> HttpResponse:
    newspaper = get_object_or_404(Newspaper, pk=pk)
    publisher = newspaper.publishers.all()
    return render(request, "press_hub/newspaper_detail.html",
                  {"newspaper": newspaper, "publisher": publisher})


def staff_required(view_func):
    """Decorator to check if the user is staff"""
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden("You do not have permission to perform this action.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view


@staff_required
@login_required
def newspaper_create(request: HttpRequest) -> HttpResponse:
    if not request.user.is_staff:
        return HttpResponseForbidden("You do not have permission to create a newspaper.")

    if request.method == "POST":
        form = NewspaperForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("press_hub:newspaper-list")
    else:
        form = NewspaperForm()

    return render(request, "press_hub/newspaper_form.html", {"form": form})


@staff_required
@login_required
def newspaper_edit(request: HttpRequest, pk: int) -> HttpResponse:
    newspaper = get_object_or_404(Newspaper, pk=pk)

    if not request.user.is_staff:
        return HttpResponseForbidden("You do not have permission to edit this newspaper.")

    if request.method == "POST":
        form = NewspaperForm(request.POST, instance=newspaper)
        if form.is_valid():
            form.save()
            return redirect("press_hub:newspaper-detail", pk=newspaper.pk)
    else:
        form = NewspaperForm(instance=newspaper)

    return render(request, "press_hub/newspaper_form.html", {"form": form})


@staff_required
@login_required
def newspaper_delete(request: HttpRequest, pk: int) -> HttpResponse:
    newspaper = get_object_or_404(Newspaper, pk=pk)

    if not request.user.is_staff:
        return HttpResponseForbidden("You do not have permission to delete this newspaper.")

    if request.method == "POST":
        newspaper.delete()
        return redirect("press_hub:newspaper-list")

    return render(request, "press_hub/newspaper_confirm_delete.html", {"newspaper": newspaper})


@staff_required
@login_required
def topic_create(request: HttpRequest) -> HttpResponse:
    if not request.user.is_staff:
        return HttpResponseForbidden(
            "You do not have permission to create a newspaper.")

    if request.method == "POST":
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("press_hub:topic-list")
    else:
        form = TopicForm()

    return render(request, "press_hub/topic_form.html", {"form": form})


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been created successfully! You can now log in.")
            return redirect("press_hub:home")
    else:
        form = UserRegistrationForm()

    return render(request, "press_hub/register.html", {"form": form})
