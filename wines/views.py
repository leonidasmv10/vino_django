from django.shortcuts import redirect, render
from .models import Wine, Category
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


@login_required
def add_wine(request):
    if request.method == "POST":
        name = request.POST["name"]
        description = request.POST["description"]
        category_id = request.POST["category"]
        price = request.POST["price"]
        image = request.FILES["image"]
        category = Category.objects.get(id=category_id)
        wine = Wine(
            name=name,
            description=description,
            category=category,
            price=price,
            image=image,
        )
        wine.save()
        profile = request.user.profile
        profile.wines.add(wine)
        profile.save()
        return redirect("collection")

    categories = Category.objects.all()
    return render(
        request,
        "wines/add_wine.html",
        {
            "categories": categories,
        },
    )


@login_required
def update_wine(request, wine_id):
    wine = get_object_or_404(Wine, id=wine_id)
    categories = Category.objects.all()

    if request.method == "POST":
        # Aquí se procesa la actualización del vino
        wine.name = request.POST["name"]
        wine.description = request.POST["description"]
        wine.price = request.POST["price"]
        wine.category = Category.objects.get(id=request.POST["category"])

        # Si hay una nueva imagen, la actualizamos
        if "image" in request.FILES:
            wine.image = request.FILES["image"]

        wine.save()
        return redirect("collection")

    return render(
        request, "wines/update_wine.html", {"wine": wine, "categories": categories}
    )


@login_required
def delete_wine(request, wine_id):
    wine = get_object_or_404(Wine, id=wine_id)

    if request.method == "POST":
        wine.delete()
        return redirect("collection")

    return render(request, "wines/delete_confirmation.html", {"wine": wine})


@login_required
def store(request):
    return render(request, "wines/store.html")


@login_required
def generate_wine(request):
    return render(request, "wines/generate_wine.html")


@login_required
def collection(request):
    # Obtener el perfil del usuario
    profile = request.user.profile

    # Obtener todas las categorías
    categories = Category.objects.all()

    # Obtener los filtros de la solicitud (si existen)
    category_filter = request.GET.get("category", None)
    score_filter = request.GET.get("score", None)

    # Filtrar los vinos del usuario
    wines = profile.wines.all()

    # Filtrar por categoría si se selecciona una
    if category_filter:
        wines = wines.filter(category_id=category_filter)

    # Crear la lista de vinos con sus puntuaciones
    wines_with_scores = []
    for wine in wines:
        total_score = wine.total_score()
        wines_with_scores.append({"wine": wine, "total_score": total_score})

    # Filtrar por puntuación si se selecciona un rango
    if score_filter:
        wines_with_scores = [
            item
            for item in wines_with_scores
            if item["total_score"] >= int(score_filter)
        ]

    # Pasar al template los vinos, categorías y los filtros actuales
    print(category_filter)

    return render(
        request,
        "wines/collection.html",
        {
            "wines_with_scores": wines_with_scores,
            "categories": categories,
            "category_filter": category_filter,
            "score_filter": score_filter,
        },
    )


@login_required
def cata(request):
    return render(request, "wines/cata.html")
