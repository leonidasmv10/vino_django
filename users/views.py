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
            Profile.objects.create(user=user)
            messages.success(request, "¡Te has registrado con éxito!")
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


import requests
from django.http import JsonResponse


def enviar_mensaje(request):
    if request.method == "POST":
        url = "https://flask-test-9ao2.onrender.com/natural_language_processing/send_message"
        payload = {
            "message": "que es la ley de newton? y por que es tan famosa?",
            "base64": "",
        }
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()  # Lanza una excepción para códigos de estado HTTP 4xx/5xx
            data = response.json()
            print(data)
            return JsonResponse(data)
        except requests.exceptions.RequestException as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Método no permitido"}, status=405)
