from django.shortcuts import redirect, render
from .models import Wine, Category
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required


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
def collection(request):
    profile = request.user.profile
    wines = profile.wines.all()
    categories = Category.objects.all()

    wines_with_scores = [
        {"wine": wine, "total_score": wine.total_score()} for wine in wines
    ]

    return render(
        request,
        "wines/collection.html",
        {
            "wines_with_scores": wines_with_scores,
            "categories": categories,
        },
    )


@login_required
def cata(request):
    return render(request, "wines/cata.html")
