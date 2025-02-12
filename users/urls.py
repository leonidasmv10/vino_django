from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("profile/", views.profile_view, name="profile"),
    path("login/", views.login_view, name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", views.register, name="register"),
    path("ranking/", views.ranking, name="ranking"),
    path("enviar_mensaje/", views.enviar_mensaje, name="enviar_mensaje"),
]
