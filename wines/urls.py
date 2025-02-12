from django.urls import path
from . import views
urlpatterns = [
    path('store/', views.store, name='store'),
    path('collection/', views.collection, name='collection'),
    path('cata/', views.cata, name='cata'),
]