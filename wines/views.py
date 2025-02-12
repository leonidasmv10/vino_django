from django.shortcuts import render
from .models import Vino
from django.core.files.storage import default_storage


def add_wine(request):
    if request.method == "POST":
        nombre = request.POST["nombre"]
        descripcion = request.POST["descripcion"]
        precio = request.POST["precio"]
        imagen = request.FILES["imagen"]

        vino = Vino(
            nombre=nombre, descripcion=descripcion, precio=precio, imagen=imagen
        )
        vino.save()
        return render(request, "wines/collection.html")
    return render(request, "wines/add_wine.html")


def store(request):
    return render(request, "wines/store.html")


def collection(request):
    return render(request, "wines/collection.html")


def cata(request):
    return render(request, "wines/cata.html")
