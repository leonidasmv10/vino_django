import time
from django.shortcuts import redirect, render
from .models import Wine, Category
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from users.models import Profile
from django.contrib import messages
import random
from diffusers import StableDiffusionXLPipeline
import torch
from django.views.decorators.csrf import csrf_exempt
from .services import generate_text
import json
import base64
from io import BytesIO

pipe = StableDiffusionXLPipeline.from_pretrained("stabilityai/stable-diffusion-xl-base-1.0", torch_dtype=torch.float16)
pipe.to("cuda")

@csrf_exempt
def generate_wine_image(request):
    if request.method == "POST":
        prompt = """
                Legado del Dragón Escarlata wine bottle. 
                A bottle of intense red wine with notes of wild blackberry and a smoky touch reminiscent of a dragon's breath atop a snowy mountain.
                Robust body with an elegant tannic structure that lingers on the palate.
                Cold color palette, muted colors, 8k.
        """

        image = pipe(prompt, num_inference_steps=50, output_type="pil").images[0]

        

        image_io = BytesIO()
        image.save(image_io, format="PNG")
        image_base64 = base64.b64encode(image_io.getvalue()).decode("utf-8")

        return JsonResponse({"image_base64": image_base64})

@csrf_exempt
def generate_wine(request):
    if request.method == "POST":
        prompt = """
        Genera un vino aleatorio y responde con un JSON que incluya estas propiedades:
        {
            "name": "Nombre del vino",
            "description": "Descripción del vino",
            "category": 1,
            "body": 5,
            "aroma": 6,
            "taste": 7,
            "tannins": 5,
            "acidity": 4,
            "sweetness": 3,
            "aging": 8,
            "price": 25.99
        }
        """

        wine_generate = generate_text(prompt)
        clean_json_string = (
            wine_generate.replace("```json", "").replace("```", "").strip()
        )
        wine_data = json.loads(clean_json_string)

        return JsonResponse(wine_data)


@login_required
def add_wine(request):
    if request.method == "POST" and request.user.is_superuser:
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

    if request.method == "POST" and request.user.is_superuser:

        wine.name = request.POST["name"]
        wine.description = request.POST["description"]
        wine.price = request.POST["price"]
        wine.category = Category.objects.get(id=request.POST["category"])

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
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == "POST":
        if request.user.is_superuser:
            wine.delete()
        else:
            profile.wines.remove(wine)
        return redirect("collection")

    return render(request, "wines/delete_confirmation.html", {"wine": wine})


@login_required
def store(request):
    return render(request, "wines/store.html")


@login_required
def buy_wines(request):
    profile = Profile.objects.get(user=request.user)
    all_wines = list(Wine.objects.exclude(id__in=profile.wines.all()))

    # cost_per_box = request.GET.get("cost", 10)
    cost_per_box = 10
    cost_per_box = int(cost_per_box)

    print(profile.coins)

    if profile.coins < cost_per_box:
        messages.error(request, "No tienes suficientes monedas para generar cartas.")
        return redirect("store")

    if len(all_wines) < 3:
        messages.warning(request, "No hay suficientes vinos disponibles para asignar.")
        return redirect("store")

    selected_wines = random.sample(all_wines, 3)
    profile.wines.add(*selected_wines)
    profile.subtract_coins(cost_per_box)
    return render(
        request, "wines/generate_wine.html", {"selected_wines": selected_wines}
    )


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
    if request.user.is_superuser:
        wines = Wine.objects.all()
    else:
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


from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Wine
import json


def get_wines_from_cart(request):
    # Obtener los IDs de los vinos desde la cookie
    cart_cookie = request.COOKIES.get("cart", "{}")
    cart = json.loads(cart_cookie)

    # Verifica si hay vinos en el carrito
    if cart:
        # Obtener los vinos basados en los IDs en el carrito
        wine_ids = list(cart.keys())
        cart_items = Wine.objects.filter(id__in=wine_ids)

        # Calcular el precio total
        total_price = sum(item.price * cart[str(item.id)] for item in cart_items)

        return cart_items, total_price
    else:
        return [], 0


def cart(request):
    # Obtener los vinos desde el carrito
    cart_items, total_price = get_wines_from_cart(request)

    context = {
        "cart_items": cart_items,
        "total_price": total_price,
    }
    return render(request, "wines/cart.html", context)


from django.http import HttpResponse
import json
from datetime import timedelta


def add_to_cart(request, wine_id):
    try:
        wine = Wine.objects.get(id=wine_id)  # Obtener el vino por su id
    except Wine.DoesNotExist:
        return HttpResponse("Vino no encontrado", status=404)

    # Obtener el carrito actual desde las cookies (si existe)
    cart = json.loads(request.COOKIES.get("cart", "{}"))
    wine_id_str = str(wine_id)
    # Verificar si el vino ya está en el carrito
    if wine_id_str in cart:
        # Si ya está en el carrito, mostrar un mensaje
        messages.warning(request, f"El vino '{wine.name}' ya está en el carrito.")
    else:
        # Si no está, agregarlo al carrito y mostrar el mensaje de éxito
        cart[wine_id_str] = 1
        messages.success(request, f"Vino '{wine.name}' agregado al carrito.")

    # Establecer la cookie con los datos actualizados del carrito
    response = redirect("collection")  # Redirigir a la página de colección
    response.set_cookie(
        "cart", json.dumps(cart), max_age=timedelta(days=30)
    )  # Cookie con duración de 30 días

    return response


def remove_from_cart(request, wine_id):
    try:
        wine = Wine.objects.get(id=wine_id)  # Obtener el vino por su id
    except Wine.DoesNotExist:
        return HttpResponse("Vino no encontrado", status=404)

    # Obtener el carrito actual desde las cookies (si existe)
    cart = json.loads(request.COOKIES.get("cart", "{}"))
    wine_id_str = str(wine_id)

    # Verificar si el vino está en el carrito
    if wine_id_str in cart:
        # Si el vino está en el carrito, eliminarlo
        del cart[wine_id_str]
        messages.success(request, f"Vino '{wine.name}' eliminado del carrito.")
    else:
        # Si no está en el carrito, mostrar un mensaje de advertencia
        messages.warning(request, f"El vino '{wine.name}' no está en el carrito.")

    # Establecer la cookie con los datos actualizados del carrito
    response = redirect("cart")  # Redirigir a la página del carrito
    response.set_cookie(
        "cart", json.dumps(cart), max_age=timedelta(days=30)
    )  # Cookie con duración de 30 días

    return response
