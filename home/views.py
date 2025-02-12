from django.shortcuts import render


def index(request):
    return render(request, "home/index.html")


def about(request):
    return render(request, "home/about.html")


def services(request):
    return render(request, "home/services.html")


def contact(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        email = request.POST.get("email")
        mensaje = request.POST.get("mensaje")
        return render(
            request,
            "home/success.html",
            {
                "nombre": nombre,
                "email": email,
                "mensaje": mensaje,
            },
        )

    return render(request, "home/contact.html")
