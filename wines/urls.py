from django.urls import path
from . import views

urlpatterns = [
    path("add_wine/", views.add_wine, name="add_wine"),
    path("buy_wines/", views.buy_wines, name="buy_wines"),
    path("update_wine/<int:wine_id>/", views.update_wine, name="update_wine"),
    path("delete_wine/<int:wine_id>/", views.delete_wine, name="delete_wine"),
    path("store/", views.store, name="store"),
    path("collection/", views.collection, name="collection"),
    path("cata/", views.cata, name="cata"),
    path("cart/", views.cart, name="cart"),
    path("add_to_cart/<int:wine_id>/", views.add_to_cart, name="add_to_cart"),
    path(
        "remove_from_cart/<int:wine_id>/",
        views.remove_from_cart,
        name="remove_from_cart",
    ),
    path("generate_wine/", views.generate_wine, name="generate_wine"),
    path("generate_wine_image/", views.generate_wine_image, name="generate_wine_image"),
]
