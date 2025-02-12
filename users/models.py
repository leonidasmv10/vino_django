from django.db import models
from django.contrib.auth.models import User


class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    monedas = models.IntegerField(default=50)
    victorias = models.IntegerField(default=0)
    vinos = models.ManyToManyField("wines.Vino", blank=True)

    def __str__(self):
        return f"Perfil de {self.user.username}"

    def agregar_monedas(self, cantidad):
        self.monedas += cantidad
        self.save()

    def restar_monedas(self, cantidad):
        if self.monedas >= cantidad:
            self.monedas -= cantidad
            self.save()

    def agregar_victoria(self):
        self.victorias += 1
        self.save()

    def agregar_puntos(self, cantidad):
        self.puntos += cantidad
        self.save()
