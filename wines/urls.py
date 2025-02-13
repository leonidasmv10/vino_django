from django.urls import path
from . import views

urlpatterns = [
    path("add_wine/", views.add_wine, name="add_wine"),
    path("generate_wine/", views.generate_wine, name="generate_wine"),
    path("update_wine/<int:wine_id>/", views.update_wine, name="update_wine"),
    path("delete_wine/<int:wine_id>/", views.delete_wine, name="delete_wine"),
    path("store/", views.store, name="store"),
    path("collection/", views.collection, name="collection"),
    path("cata/", views.cata, name="cata"),
]
