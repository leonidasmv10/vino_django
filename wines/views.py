from django.shortcuts import redirect, render
from .models import Vino
from django.core.files.storage import default_storage


def add_wine(request):
    if request.method == "POST":
        nombre = request.POST["nombre"]
        descripcion = request.POST["descripcion"]
        precio = request.POST["precio"]
        # imagen = request.FILES["imagen"]

        vino = Vino(
            nombre=nombre, descripcion=descripcion, precio=precio, imagen="test"
        )
        vino.save()
        return redirect("collection")
    return render(request, "wines/add_wine.html")


def store(request):
    return render(request, "wines/store.html")


# def collection(request):
#     vinos = Vino.objects.all()
#     return render(request, "wines/collection.html", {"vinos": vinos})


def collection(request):
    vinos = Vino.objects.all()
    categorias = Vino.objects.values_list(
        "categoria", flat=True
    ).distinct()  # Obtener el poder máximo de los vinos

    return render(
        request,
        "wines/collection.html",
        {
            "vinos": vinos,
            "categorias": categorias,
        },
    )


def cata(request):
    return render(request, "wines/cata.html")
