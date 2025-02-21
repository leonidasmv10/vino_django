import time
from django.shortcuts import redirect, render
from .models import Wine, Category
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from users.models import Profile
from django.contrib import messages
import random
from diffusers import StableDiffusionXLPipeline, StableDiffusionPipeline
import torch
from django.views.decorators.csrf import csrf_exempt
from .services import generate_text
import json
import base64
from io import BytesIO
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from datetime import timedelta
import uuid
from django.conf import settings
import os


prompt_normal = f"""
responde siempre con una matriz JSON que incluya las siguientes propiedades:

- "name" (texto): Un nombre suave, que no cause intimidación y débil, creativo de entre 25 y 35 caracteres.
- "description" (texto): Una descripción ingeniosa y evocadora.
- "category" (entero):
  - 1 = Tinto (Fuego)
  - 2 = Blanco (Nieve)
  - 3 = Rosado (Agua)
- "body", "aroma", "taste", "tannins", "acidity", "sweetness", "aging" (enteros del 1 al 5): Valores sensoriales del vino.
- "price" (decimal): Se calcula en función de las propiedades sensoriales.
- "total_score" (promedio de body, aroma, taste, tannins, acidity, sweetness y aging).

### **Reglas adicionales para asegurar la distribución correcta:**
1. **El nombre del vino debe reflejar su stats**:   
2. **El `total_score` debe estar forzado dentro de su rango, sin excepciones.**  
3. **Los valores sensoriales deben estar dentro de los rangos adecuados al `total_score` para mantener coherencia.**  
4. **El precio debe reflejar la calidad del vino, siendo más alto para `total_score` elevados.**  

Sé altamente creativo en la generación del nombre y la descripción.
"""

prompt_premium = f"""
responde siempre con una matriz JSON que incluya las siguientes propiedades:

- "name" (texto): Un nombre fuerte, creativo de entre 25 y 35 caracteres.
- "description" (texto): Una descripción ingeniosa y evocadora.
- "category" (entero): 
  - 1 = Tinto (Fuego)
  - 2 = Blanco (Nieve)
  - 3 = Rosado (Agua)
- "body", "aroma", "taste", "tannins", "acidity", "sweetness", "aging" (enteros del 5 al 8): Valores sensoriales del vino.
- "price" (decimal): Se calcula en función de las propiedades sensoriales.
- "total_score" (promedio de body, aroma, taste, tannins, acidity, sweetness y aging).

### **Reglas adicionales para asegurar la distribución correcta:**
1. **El nombre del vino debe reflejar su stats**:   
2. **El `total_score` debe estar forzado dentro de su rango, sin excepciones.**  
3. **Los valores sensoriales deben estar dentro de los rangos adecuados al `total_score` para mantener coherencia.**  
4. **El precio debe reflejar la calidad del vino, siendo más alto para `total_score` elevados.**  

Sé altamente creativo en la generación del nombre y la descripción.
"""


prompt_legendario = f"""
responde siempre con una matriz JSON que incluya las siguientes propiedades:

- "name" (texto): Un nombre muy fuerte y muy intimidante, creativo de entre 25 y 35 caracteres.
- "description" (texto): Una descripción ingeniosa y evocadora.
- "category" (entero):
  - 1 = Tinto (Fuego)
  - 2 = Blanco (Nieve)
  - 3 = Rosado (Agua)
- "body", "aroma", "taste", "tannins", "acidity", "sweetness", "aging" (enteros del 8 al 10): Valores sensoriales del vino.
- "price" (decimal): Se calcula en función de las propiedades sensoriales.
- "total_score" (promedio de body, aroma, taste, tannins, acidity, sweetness y aging).

### **Reglas adicionales para asegurar la distribución correcta:**
1. **El nombre del vino debe reflejar su stats**:   
2. **El `total_score` debe estar forzado dentro de su rango, sin excepciones.**  
3. **Los valores sensoriales deben estar dentro de los rangos adecuados al `total_score` para mantener coherencia.**  
4. **El precio debe reflejar la calidad del vino, siendo más alto para `total_score` elevados.**  

Sé altamente creativo en la generación del nombre y la descripción.
"""

# pipe = StableDiffusionXLPipeline.from_pretrained("stabilityai/stable-diffusion-xl-base-1.0", torch_dtype=torch.float16)
pipe = StableDiffusionPipeline.from_pretrained(
    "dreamlike-art/dreamlike-anime-1.0", torch_dtype=torch.float16, use_safetensors=True
)

# pipe = StableDiffusionPipeline.from_pretrained(
#     "dreamlike-art/dreamlike-diffusion-1.0", torch_dtype=torch.float16, use_safetensors=True
# )


pipe.to("cuda" if torch.cuda.is_available() else "cpu")

# Ruta donde se guardarán las imágenes
IMAGE_FOLDER = os.path.join(settings.MEDIA_ROOT, "generated_wine_images")

# Asegurar que la carpeta existe
os.makedirs(IMAGE_FOLDER, exist_ok=True)


@csrf_exempt
def generate_wine_image(request):
    if request.method == "POST":

        data = json.loads(request.body)  # Parseamos el JSON del cuerpo de la solicitud

        name = data["name"]
        description = data["description"]
        category_id = data["category"]

        # Buscar la categoría en la base de datos
        category = Category.objects.get(id=category_id)

        # prompt = """{wines.description}. Cold color palette, muted colors, 8k."""

        # **Eliminar imagen anterior**
        existing_images = os.listdir(IMAGE_FOLDER)
        for img_file in existing_images:
            os.remove(os.path.join(IMAGE_FOLDER, img_file))

        name = data["name"]
        description = data["description"]
        category_id = data["category"]
        # **Generar la nueva imagen con IA**
        prompt = f"""
                Wine name: {name}
                Category: {category.name}
                Visual elements: A bottle of wine, a glass of the same wine, realistic colors, showcasing the wine's unique characteristics. The bottle should always be included in the scene. 8k resolution, elegant and detailed.
        """

        print(prompt)
        image = pipe(prompt, num_inference_steps=50, output_type="pil").images[0]

        # **Guardar la imagen en el servidor**
        image_name = f"{uuid.uuid4().hex}.png"
        image_path = os.path.join(IMAGE_FOLDER, image_name)
        image.save(image_path, format="PNG")

        # **Obtener la URL de la imagen**
        image_url = f"{settings.MEDIA_URL}generated_wine_images/{image_name}"

        return JsonResponse({"image_url": image_url})

    return JsonResponse({"error": "Método no permitido"}, status=405)


@csrf_exempt
def generate_wine(request):
    if request.method == "POST":
        data = json.loads(request.body)  # Parseamos el JSON del cuerpo de la solicitud
        prompt = ""
        type_card = data["type_card"]
        category_id = data["category_id"]

        category = Category.objects.get(id=category_id)

        prompt = ""

        # Genera un vino super legendario aleatorio y

        # print(type_card)
        if type_card == "1":
            prompt = f"""
                Genera un vino {category.name} aleatorio y {prompt_normal} 
            """
        elif type_card == "2":
            prompt = f"""
                Genera un vino {category.name} premium aleatorio y {prompt_premium} 
            """
        else:
            prompt = f"""
                Genera un vino {category.name} super legendario aleatorio y {prompt_legendario} 
            """

        wine_generate = generate_text(prompt)
        clean_json_string = (
            wine_generate.replace("```json", "").replace("```", "").strip()
        )
        wine_data = json.loads(clean_json_string)

        return JsonResponse(wine_data)


import requests
from django.core.files.base import ContentFile


@login_required
def add_wine(request):
    if request.method == "POST" and request.user.is_superuser:
        name = request.POST["name"]
        description = request.POST["description"]
        category_id = request.POST["category"]
        price = request.POST["price"]
        image_url = request.POST["image_url_frontend"]
        cuerpo = request.POST["cuerpo"]
        aroma = request.POST["aroma"]
        sabor = request.POST["sabor"]
        taninos = request.POST["taninos"]
        acidez = request.POST["acidez"]
        dulzura = request.POST["dulzura"]
        vintage = request.POST["vintage"]

        category = Category.objects.get(id=category_id)

        # Si la URL de la imagen es relativa, agregar la base de la URL
        if image_url.startswith("/media/"):
            image_url = f"http://127.0.0.1:8000{image_url}"

        # Descargar la imagen generada desde la URL
        response = requests.get(image_url)
        if response.status_code != 200:
            return JsonResponse({"error": "No se pudo descargar la imagen"}, status=400)

        # Crear un nombre de archivo único
        image_name = os.path.basename(image_url) or f"wine_{name}.png"
        image_content = ContentFile(response.content, name=image_name)

        wine = Wine(
            name=name,
            description=description,
            category=category,
            price=price,
            # image=image,
            body=cuerpo,
            aroma=aroma,
            taste=sabor,
            tannins=taninos,
            acidity=acidez,
            sweetness=dulzura,
            aging=vintage,
        )
        wine.image.save(image_name, image_content)  # Guardar en `ImageField`
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
        wine.body = request.POST["cuerpo"]
        wine.aroma = request.POST["aroma"]
        wine.taste = request.POST["sabor"]
        wine.tannins = request.POST["taninos"]
        wine.acidity = request.POST["acidez"]
        wine.sweetness = request.POST["dulzura"]
        wine.aging = request.POST["vintage"]

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

    print(f"Category Filter: {category_filter}")

    # Filtrar los vinos del usuario
    if request.user.is_superuser:
        wines = Wine.objects.all()
    else:
        wines = profile.wines.all()

    # Filtrar por categoría si se selecciona una
    if category_filter not in [None, ""]:
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


def get_wines_from_cart(request):
    # Obtener los IDs de los vinos desde la cookie
    cart_cookie = request.COOKIES.get("cart", "{}")
    cart = json.loads(cart_cookie)

    # Verifica si hay vinos en el carrito para el usuario logueado
    user_id = str(request.user.id)  # Convertir el ID del usuario a string

    # Verificar si el usuario tiene vinos en el carrito
    if user_id in cart:
        # Obtener los IDs de los vinos que están en el carrito del usuario
        wine_ids = cart[user_id]

        # Obtener los objetos de vino correspondientes a esos IDs
        cart_items = Wine.objects.filter(id__in=wine_ids)

        # Calcular el precio total
        total_price = sum(item.price for item in cart_items)

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


def add_to_cart(request, wine_id):
    try:
        wine = Wine.objects.get(id=wine_id)  # Obtener el vino por su id
    except Wine.DoesNotExist:
        return HttpResponse("Vino no encontrado", status=404)

    # Obtener el carrito actual desde las cookies (si existe)
    cart = json.loads(request.COOKIES.get("cart", "{}"))
    wine_id_str = str(wine_id)

    # Verificar si el usuario tiene vinos en el carrito
    user_id = str(
        request.user.id
    )  # Convertir el id del usuario a string para usarlo como clave

    # Si el usuario ya tiene vinos en su carrito
    if user_id in cart:
        # Si el vino ya está en la lista del usuario, mostrar un mensaje
        if wine_id_str in cart[user_id]:
            messages.warning(request, f"El vino '{wine.name}' ya está en el carrito.")
        else:
            # Añadir el vino a la lista de vinos del usuario (sin duplicados)
            cart[user_id].append(wine_id_str)
            messages.success(request, f"Vino '{wine.name}' agregado al carrito.")
    else:
        # Si el usuario no tiene vinos en el carrito, crear una nueva lista con el vino
        cart[user_id] = [wine_id_str]
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
    cart_cookie = request.COOKIES.get("cart", "{}")
    cart = json.loads(cart_cookie)
    wine_id_str = str(wine_id)

    # Obtener el ID del usuario como cadena
    user_id = str(request.user.id)

    # Verificar si el usuario tiene vinos en el carrito
    if user_id in cart:
        # Si el vino está en la lista del carrito del usuario
        if wine_id_str in cart[user_id]:
            cart[user_id].remove(wine_id_str)  # Eliminar el vino de la lista
            # Si la lista queda vacía, eliminamos la clave del carrito
            if not cart[user_id]:
                del cart[user_id]
            messages.success(request, f"Vino '{wine.name}' eliminado del carrito.")
        else:
            # Si el vino no está en la lista, mostrar un mensaje de advertencia
            messages.warning(request, f"El vino '{wine.name}' no está en tu carrito.")
    else:
        # Si el usuario no tiene un carrito, mostrar un mensaje
        messages.warning(request, "Tu carrito está vacío.")

    # Establecer la cookie con los datos actualizados del carrito
    response = redirect("cart")  # Redirigir a la página del carrito
    response.set_cookie(
        "cart", json.dumps(cart), max_age=timedelta(days=30)
    )  # Cookie con duración de 30 días

    return response
