from django.urls import path
from . import views

urlpatterns = [
    path("add_wine/", views.add_wine, name="add_wine"),
    path("store/", views.store, name="store"),
    path("collection/", views.collection, name="collection"),
    path("cata/", views.cata, name="cata"),
]
