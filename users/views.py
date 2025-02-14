from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegisterForm

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Profile


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "¡Bienvenido de nuevo!")
            return redirect("home")
        else:
            messages.error(request, "Nombre de usuario o contraseña incorrectos.")

    return render(request, "users/login.html")


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            if User.objects.filter(username=username).exists():
                messages.error(request, "El nombre de usuario ya está en uso.")
                return redirect("register")

            password_hash = make_password(password)
            user = User.objects.create(username=username, password=password_hash)
            user.save()
            return redirect("login")

    else:
        form = RegisterForm()

    return render(request, "users/register.html", {"form": form})


def ranking(request):
    return render(request, "users/ranking.html")


@login_required
def profile_view(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, "users/profile.html", {"profile": profile})
